'''
Inputs from dilepton analyzers = limit curves for a range of widths
This class computes the 2D limit contours for the mDM vs mZ' plot.
'''
import numpy as np 
import re
import os
import sys
import ROOT
from width_functions import gamma_axial_total, gamma_vector_total
from pprint import pprint
import math

class DileptonConverter:
	def __init__(self, scenario):
		self._scenario = scenario
		if not self._scenario in ["V2", "A2"]:
			raise ValueError("Unknown scenario {}".format(self._scenario))

		if self._scenario == "V2":
			self._gq = 0.25
			self._gl = 0.1
			self._gDM = 1.0
			self._vtype = "vector"
		elif self._scenario == "A2":
			self._gq = 0.25
			self._gl = 0.1
			self._gDM = 1.0
			self._vtype = "axial"

		# Load precomputed model cross sections
		#self.load_reference_xs("reference_xs.txt")
		self._ref_xsbrl = {}
		self._ref_xsbrl["V2"] = self.load_ref_xs("xs_V2.dat")
		self._ref_xsbrl["A2"] = self.load_ref_xs("xs_A2.dat")

		# Initialize dilepton limit object to None
		self._xslimit_vs_mmed_widthdict = None # dict {width: {mmed: xs*BR(single lepton) limit}}

		self._limit_mmeds = []
		self._mdms = []		

	def load_obs_lllimits(self, input_path_dict):
		# input_path_dict = {0.01: path_to_0.01_limits, ...}
		# Limits files contain (mass, limit) pairs, one per mass
		# Returns dict {width: TGraph}
		
		if self._xslimit_vs_mmed_widthdict:
			raise ValueError("Attempt to load dilepton limits more than once!")

		self._xslimit_vs_mmed_widthdict = {}
		for width, path in input_path_dict.iteritems():
			data = np.loadtxt(path, dtype=float)
			mmeds = data[:,0]
			limits = data[:,1] * 1928 * 3
			self._xslimit_vs_mmed_widthdict[width] = dict(zip(mmeds, limits))
			#print "{mmed : xs limit} for width " + str(width)
			#print self._xslimit_vs_mmed_widthdict[width]
			self._limit_mmeds.extend(mmeds)
			self._limit_mmeds = list(set(self._limit_mmeds))
			#self._limit_mmeds = list(set(self._limit_mmeds.extend(mmeds)))
		self._limit_mmeds = sorted(self._limit_mmeds)

		for width in sorted(input_path_dict.keys()):
			print "Obs xs limit for mmed=1600, width={} = {}".format(width, self._xslimit_vs_mmed_widthdict[width][1600.])

		self.check_lllimits()

	def load_exp_lllimits(self, input_path_dict, quantile=0.5):
		# input_path_dict = {0.01: path_to_0.01_limits, ...}
		# Limit files contain (mass, limit), multiple per mass corresponding to toys. 

		if self._xslimit_vs_mmed_widthdict:
			raise ValueError("Attempt to load dilepton limits more than once!")
		self._xslimit_vs_mmed_widthdict = {}

		for width, path in input_path_dict.iteritems():
			data = np.loadtxt(path)
			mmeds = sorted(list(set(data[:,0])))
			limits = []
			for mass in mmeds:
				limits.append(np.percentile(data[data[:,0] == mass][:,1] * 1928. * 3, quantile))
			self._xslimit_vs_mmed_widthdict[width] = dict(zip(mmeds, limits))
			self._limit_mmeds.extend(mmeds)
			self._limit_mmeds = list(set(self._limit_mmeds))
		self._limit_mmeds = sorted(self._limit_mmeds)
		self.check_lllimits()

	def check_lllimits(self):
		""" Checks that the mmed vs. width grid is complete. 
		For now, if any grid points are missing, abandon. Might be worth coming up with a scheme to allow some missing points.
		"""
		missing_points = {} # mmed : width
		for mmed in self._limit_mmeds:
			for width in self._xslimit_vs_mmed_widthdict.keys():
				if not mmed in self._xslimit_vs_mmed_widthdict[width].keys():
					if not width in missing_points:
						missing_points[width] = []
					missing_points[width].append(mmed)
		if len(missing_points) >= 1:
			print(missing_points)
			raise ValueError("Missing input limit points.")

	def load_ref_xs(self, path_to_file):
		"""Loads DMSIMP cross sections from David's text file
			Stored as dict of TGraph(1D)s. 
			{scenario: {mDM: TGraph(mmed, xs)}}
		"""
		ref_xsbrl = {}

		# Load reference cross sections from Madgraph
		data = np.loadtxt(path_to_file, dtype=float)
		mmeds = []
		mdms = []
		ref_xsbrl_gen = {}
		for mmed, mdm, xs in data:
			if mdm <= mmed:
				mmeds.append(mmed)
				mdms.append(mdm)
			ref_xsbrl_gen[(mmed, mdm)] = xs
		mmeds = sorted(list(set(mmeds)))
		mdms = sorted(list(set(mdms)))

		# Fill in MMED < 2*MDM points, which were not generated
		ref_xsbrl_grid = {}
		for mmed in mmeds:
			for mdm in mdms:
				if (mmed, mdm) in ref_xsbrl_gen:
					ref_xsbrl_grid[(mmed, mdm)] = ref_xsbrl_gen[(mmed, mdm)]
				else:
					if 2 * mdm > mmed:
						# Use (mmed, mmed/2), if it exists. If not, search for another point above the diagonal.
						if (mmed, mmed/2) in ref_xsbrl_gen:
							ref_xsbrl_grid[(mmed, mdm)] = ref_xsbrl_gen[(mmed, mmed/2)]
						else:
							for gen_mmed, gen_mdm in ref_xsbrl_gen.keys():
								found_replacement = False
								if gen_mmed == mmed and gen_mdm >= gen_mmed / 2.:
									ref_xsbrl_grid[(mmed, mdm)] = ref_xsbrl_gen[(gen_mmed, gen_mdm)]
									found_replacement = True
									break
								if not found_replacement:
									print ("WARNING : Unable to find replacement for (mmed, mdm)=({}, {}). Using 0.".format(mmed, mdm))
									ref_xsbrl_grid[(mmed, mdm)] = 0.
					else:
						print("WARNING : Couldn't find gen xs for (mmed, mdm)=({}, {}). Using 0".format(mmed, mdm))
						ref_xsbrl_grid[(mmed, mdm)] = 0.

		# Convert to TGraphs
		ref_xsbrl_graphs = {}
		for mdm in mdms:
			ref_xsbrl_graphs[mdm] = ROOT.TGraph(len(mmeds))
			for ipt, mmed in enumerate(mmeds):
				ref_xsbrl_graphs[mdm].SetPoint(ipt, mmed, ref_xsbrl_grid[(mmed, mdm)])

		return ref_xsbrl_graphs

	def load_reference_xs_andreas(self, path_to_file):
		"""Loads DMSIMP cross sections from Andreas' text file
			Stored as dict of TGraph(1D)s. 
			{scenario: {mDM: TGraph(mmed, xs)}}
		"""
		data = np.loadtxt(path_to_file, dtype=str)

		# Load cross section values from text file 
		# Note: values in file are Z' xs * BR(e + mu + tau), in pb)
		# Here, divide by 3 to get the single lepton flavor BRs.
		self._ref_xsbrl={}
		self._ref_xsbrl["V2"]={}
		self._ref_xsbrl["A2"]={}
		re_modelstr = re.compile("gdmv([\d\.]+)_gqv([\d\.]+)_gql([\d\.]+)_gdma([\d\.]+)_gqa([\d\.]+)_gql([\d\.]+)_gnu([\d\.]+)_mmed([\d\.]+)_mdm([\d\.]+)")
		for tag, xs, dxs, unit in data:
			gdmv, gqv, glv, gdma, gqa, gla, gnu, mmed, mdm = (float(x) for x in re_modelstr.match(tag).groups())

			if mmed < 200.:
				continue

			# Figure out scenario for this row
			if [gdmv,gqv,glv] == [1.0,0.1,0.01] and [gdma,gqa,gla] == [0.,0.,0.]:
				scenario = "V2"
			elif [gdmv,gqv,glv] == [0.,0.,0.] and [gdma,gqa,gla] == [1.0,0.1,0.1]:
				scenario = "A2"
			else:
				raise ValueError("Couldn't figure out scenario from tag {}".format(tag))

			#print "Reading in ref xs / scenario {} / mmed {} / mdm {} / xs {}".format(scenario, mmed, mdm, float(xs)/3.)

			if not mdm in self._ref_xsbrl[scenario]:
				self._ref_xsbrl[scenario][mdm] = ROOT.TGraph()
			self._ref_xsbrl[scenario][mdm].SetPoint(self._ref_xsbrl[scenario][mdm].GetN(), mmed, float(xs) / 3.)

		# Sort TGraphs by x axis (mmed)
		for scenario in self._ref_xsbrl:
			for mdm in self._ref_xsbrl[scenario]:
				self._ref_xsbrl[scenario][mdm].Sort()

	def compute_varwidth_limits(self):
		""" Workhorse function: actually computes the limits for each (mmed, mdm) point, taking the closest width for the model
		"""
		#mmeds = set()
		#for singlewidth_limit_dict in self._xslimit_vs_mmed_widthdict.values():
		#	mmeds = mmeds.union(set(singlewidth_limit_dict.keys()))

		# For each mmed, make a TGraph of xslimit vs. width. To be used for interpolation. 
		tg_xslimit_width_mmeddict = {}
		for mmed in self._limit_mmeds:
			tg_xslimit_width_mmeddict[mmed] = ROOT.TGraph()
			for width in self._xslimit_vs_mmed_widthdict.keys():
				#print "mmed={}, width={}".format(mmed, width)
				tg_xslimit_width_mmeddict[mmed].SetPoint(tg_xslimit_width_mmeddict[mmed].GetN(), width, self._xslimit_vs_mmed_widthdict[width][mmed])
			tg_xslimit_width_mmeddict[mmed].Sort()

		# Make a limit (xs95 vs mmed) graph for each mDM, where xs95 is derived from the interpolation graph
		self._tg_xslimit_mmed_mdmdict = {}
		for mdm in sorted(self._ref_xsbrl[self._scenario].keys()):
			self._tg_xslimit_mmed_mdmdict[mdm] = ROOT.TGraph()
			for mmed in self._limit_mmeds:
				if self._scenario == "A2":
					width = gamma_axial_total(mmed, mdm, g_q=0.1, g_chi=1.0, g_l=0.1) / mmed
				elif self._scenario == "V2":
					width = gamma_vector_total(mmed, mdm, g_q=0.1, g_chi=1.0, g_l=0.01) / mmed

				# If width is lower than the experimental grid, just take the lowest (0.5%), since it's way below the experimental resolution here.
				if width < min(tg_xslimit_width_mmeddict[mmed].GetX()):
					width = min(tg_xslimit_width_mmeddict[mmed].GetX())
				elif width > max(tg_xslimit_width_mmeddict[mmed].GetX()):
					print "Error for scenario {}, mdm={}, mmed={}, width={}".format(self._scenario, mdm, mmed, width)
					raise ValueError("Width {} is outside of analysis range ({}, {})".format(width, min(tg_xslimit_width_mmeddict[mmed].GetX()), max(tg_xslimit_width_mmeddict[mmed].GetX())))

				self._tg_xslimit_mmed_mdmdict[mdm].SetPoint(self._tg_xslimit_mmed_mdmdict[mdm].GetN(), mmed, tg_xslimit_width_mmeddict[mmed].Eval(width, 0, "S"))

	def compute_contour(self):
		self.compute_varwidth_limits()

		# Subtract reference xs from limit xs
		# Also make a TGraph2D instead of {mdm, TGraph1D}, to use the GetContour() function.
		self._tg_dxs_mdm_mmed     = ROOT.TGraph2D()
		self._tg_xslimit_mdm_mmed = ROOT.TGraph2D()
		self._tg_xsref_mdm_mmed   = ROOT.TGraph2D()
		for mdm in self._tg_xslimit_mmed_mdmdict.keys():
			for ipt in xrange(self._tg_xslimit_mmed_mdmdict[mdm].GetN()):
				mmed = self._tg_xslimit_mmed_mdmdict[mdm].GetX()[ipt]

				# Temporary: if mmed is outside reference range, skip.
				# You need to compute these cross sections.
				if mmed > max(self._ref_xsbrl[self._scenario][mdm].GetX()) or mmed < min(self._ref_xsbrl[self._scenario][mdm].GetX()):
					continue

				xslimit = self._tg_xslimit_mmed_mdmdict[mdm].GetY()[ipt]
				if mmed < min(self._ref_xsbrl[self._scenario][mdm].GetX()) or mmed > max(self._ref_xsbrl[self._scenario][mdm].GetX()):
					raise ValueError("mmed {} is outside of reference range ({}, {})".format(mmed, min(self._ref_xsbrl[self._scenario][mdm].GetX()), max(self._ref_xsbrl[self._scenario][mdm].GetX())))
				ref_xs = self._ref_xsbrl[self._scenario][mdm].Eval(mmed)

				self._tg_xslimit_mdm_mmed.SetPoint(self._tg_xslimit_mdm_mmed.GetN(), mmed, mdm, xslimit)
				self._tg_xsref_mdm_mmed.SetPoint(self._tg_xsref_mdm_mmed.GetN(), mmed, mdm, ref_xs)
				if xslimit <= 0 or ref_xs <= 0:
					raise ValueError("Negative xslimit {} or ref_xs {} for (mmed, mdm)=({}, {})".format(xslimit, ref_xs, mmed, mdm))
				self._tg_dxs_mdm_mmed.SetPoint(self._tg_dxs_mdm_mmed.GetN(), mmed, mdm, math.log(xslimit) - math.log(ref_xs))
		self._limit_contours = self._tg_dxs_mdm_mmed.GetContourList(0.)

		# Combine contours into one shape.
		# Not guaranteed to work for anything beyond EXO-19-019.
		self._combined_contour = ROOT.TGraph()
		ipt1 = 0
		self._combined_contour.SetPoint(ipt1, -1., -1.)
		ipt1 += 1

		for contour in self._limit_contours:
			self._combined_contour.SetPoint(ipt1, contour.GetX()[0], -1)
			ipt1 += 1
			for ipt2 in xrange(contour.GetN()):
				self._combined_contour.SetPoint(ipt1, contour.GetX()[ipt2], contour.GetY()[ipt2])
				ipt1 += 1
			if contour.GetY()[contour.GetN() - 1] == 0:
				self._combined_contour.SetPoint(ipt1, contour.GetX()[contour.GetN() - 1], -1)
			else:
				self._combined_contour.SetPoint(ipt1, contour.GetX()[contour.GetN() - 1], 5.e4)
			ipt1 += 1
		self._combined_contour.SetPoint(ipt1, -1, self._combined_contour.GetY()[self._combined_contour.GetN()-1])
		ipt1 += 1
		self._combined_contour.SetPoint(ipt1, -1, -1)
		ipt1 += 1

	def get_contours(self):
		return self._limit_contours

	def get_combined_contour(self):
		return self._combined_contour

	def get_xslimit_graph(self):
		return self._tg_xslimit_mdm_mmed

	def get_xsref_graph(self):
		return self._tg_xsref_mdm_mmed

	def get_dxs_graph(self):
		return self._tg_dxs_mdm_mmed


if __name__ == "__main__":
	for scenario in ["V2", "A2"]:
		output_file = ROOT.TFile("ScanMM/contours_dilepton_{}.root".format(scenario), "RECREATE")

		# Observed
		converter = DileptonConverter(scenario)
		input_path_dict_obs = {
			0.0050: "raw/ZPrime_limitCard_Run2_width005_Obs_legcay.txt",
			0.0075: "raw/ZPrime_limitCard_Run2_width0075_Obs_legcay.txt",
			0.0100: "raw/ZPrime_limitCard_Run2_width01_Obs_legcay.txt",
			0.0125: "raw/ZPrime_limitCard_Run2_width0125_Obs_legcay.txt",
			0.0150: "raw/ZPrime_limitCard_Run2_width015_Obs_legcay.txt",
			0.0175: "raw/ZPrime_limitCard_Run2_width0175_Obs_legcay.txt",
			0.0200: "raw/ZPrime_limitCard_Run2_width02_Obs_legcay.txt",
			0.0225: "raw/ZPrime_limitCard_Run2_width0225_Obs_legcay.txt",
			0.0250: "raw/ZPrime_limitCard_Run2_width025_Obs_legcay.txt",
			0.0275: "raw/ZPrime_limitCard_Run2_width0275_Obs_legcay.txt",
			0.0300: "raw/ZPrime_limitCard_Run2_width03_Obs_legcay.txt",
			0.0325: "raw/ZPrime_limitCard_Run2_width0325_Obs_legcay.txt",
			0.035: "raw/ZPrime_limitCard_Run2_width035_Obs_legcay.txt",
			#0.05: "raw/ZPrime_limitCard_Run2_width05_Obs_legcay.txt",
			#0.1: "raw/ZPrime_limitCard_Run2_width10_Obs_legcay.txt",
		}
		converter.load_obs_lllimits(input_path_dict_obs)
		converter.compute_contour()
		if converter.get_contours():
			for i, contour in enumerate(converter.get_contours()):
				contour.SetName("obs_{}".format(i))
			converter.get_contours().Write()
		converter.get_combined_contour().SetName("obs_combined")
		converter.get_combined_contour().Write()
		converter.get_xslimit_graph().SetName("obs_xslimit")
		converter.get_xslimit_graph().Write()
		converter.get_xsref_graph().SetName("obs_xsref")
		converter.get_xsref_graph().Write()
		converter.get_dxs_graph().SetName("obs_dxs")
		converter.get_dxs_graph().Write()

		input_path_dict_exp = {
			0.0050: "raw/ZPrime_limitCard_Run2_width005_Exp_legcay.txt",
			0.0075: "raw/ZPrime_limitCard_Run2_width0075_Exp_legcay.txt",
			0.0100: "raw/ZPrime_limitCard_Run2_width01_Exp_legcay.txt",
			0.0125: "raw/ZPrime_limitCard_Run2_width0125_Exp_legcay.txt",
			0.0150: "raw/ZPrime_limitCard_Run2_width015_Exp_legcay.txt",
			0.0175: "raw/ZPrime_limitCard_Run2_width0175_Exp_legcay.txt",
			0.0200: "raw/ZPrime_limitCard_Run2_width02_Exp_legcay.txt",
			0.0225: "raw/ZPrime_limitCard_Run2_width0225_Exp_legcay.txt",
			0.0250: "raw/ZPrime_limitCard_Run2_width025_Exp_legcay.txt",
			0.0275: "raw/ZPrime_limitCard_Run2_width0275_Exp_legcay.txt",
			0.0300: "raw/ZPrime_limitCard_Run2_width03_Exp_legcay.txt",
			0.0325: "raw/ZPrime_limitCard_Run2_width0325_Exp_legcay.txt",
			0.035: "raw/ZPrime_limitCard_Run2_width035_Exp_legcay.txt",
			0.05: "raw/ZPrime_limitCard_Run2_width05_Exp_legcay.txt",
			0.1: "raw/ZPrime_limitCard_Run2_width10_Exp_legcay.txt",
		}
		for quantile, expname in [(0.025, "m2"), (0.16, "m1"), (0.5, "med"), (0.84, "p1"), (0.975, "p2")]:
			converter_exp = DileptonConverter(scenario)
			converter_exp.load_exp_lllimits(input_path_dict_exp, quantile=quantile)
			converter_exp.compute_contour()
			if converter_exp.get_contours():
				for i, contour in enumerate(converter_exp.get_contours()):
					contour.SetName("exp_{}_{}".format(expname, i))
			converter_exp.get_contours().Write()
			converter_exp.get_combined_contour().SetName("exp_combined_{}".format(expname))
			converter_exp.get_combined_contour().Write()
			converter_exp.get_xslimit_graph().SetName("exp_{}_xslimit".format(expname))
			converter_exp.get_xslimit_graph().Write()
			converter_exp.get_xsref_graph().SetName("exp_{}_xsref".format(expname))
			converter_exp.get_xsref_graph().Write()
			converter_exp.get_dxs_graph().SetName("exp_{}_dxs".format(expname))
			converter_exp.get_dxs_graph().Write()

		output_file.Close()
