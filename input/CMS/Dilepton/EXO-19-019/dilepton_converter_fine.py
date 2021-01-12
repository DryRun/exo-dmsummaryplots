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
import numpy as np
from scipy import interpolate

class DileptonConverterFine:
	def __init__(self, scenario):
		self._scenario = scenario
		if not self._scenario in ["V2", "A2"]:
			raise ValueError("Unknown scenario {}".format(self._scenario))

		if self._scenario == "V2":
			self._gq = 0.1
			self._gl = 0.01
			self._gDM = 1.0
			self._vtype = "vector"
		elif self._scenario == "A2":
			self._gq = 0.1
			self._gl = 0.1
			self._gDM = 1.0
			self._vtype = "axial"

		if self._scenario == "V2":
			self._mmeds = np.arange(200., 4000., 10.)
			self._mdms = np.arange(0., 4000., 10.)
		elif self._scenario == "A2":
			self._mmeds = np.arange(200., 5000., 10.)
			self._mdms = np.arange(0., 5000., 10.)

		# Load precomputed model cross sections
		self.load_xsref("xs_{}.dat".format(self._scenario))

		# Initialize dilepton limit object to None
		self._xslimit_vs_mmed_widthdict = None # dict {width: {mmed: xs*BR(single lepton) limit}}

		self._limit_mmeds = []
		#self._mdms = []

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

			# For Run 2, 10% width limits are for >600 GeV only
			if width == 0.1:
				omitted_points = (mmeds < 600)
				limits[omitted_points] = np.array([1.e20] * omitted_points.sum())

			self._xslimit_vs_mmed_widthdict[width] = dict(zip(mmeds, limits))
			#print "{mmed : xs limit} for width " + str(width)
			#print self._xslimit_vs_mmed_widthdict[width]
			self._limit_mmeds.extend(mmeds)
			self._limit_mmeds = list(set(self._limit_mmeds))
			#self._limit_mmeds = list(set(self._limit_mmeds.extend(mmeds)))
		self._limit_mmeds = sorted(self._limit_mmeds)

		#for width in sorted(input_path_dict.keys()):
		#	print "Obs xs limit for mmed=1600, width={} = {}".format(width, self._xslimit_vs_mmed_widthdict[width][1600.])

		self.check_lllimits()
		self.convert_width_to_mdm()

		# Make a 2D TGraph of inputs, for debugging
		self._xslimit_width_mmed_tg = ROOT.TGraph2D()
		for width in self._xslimit_vs_mmed_widthdict:
			for mmed, xslimit in self._xslimit_vs_mmed_widthdict[width].iteritems():
				self._xslimit_width_mmed_tg.SetPoint(self._xslimit_width_mmed_tg.GetN(), mmed, width, xslimit)

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
		self.convert_width_to_mdm()

		# Make a 2D TGraph of inputs, for debugging
		self._xslimit_width_mmed_tg = ROOT.TGraph2D()
		for width in self._xslimit_vs_mmed_widthdict:
			for mmed, xslimit in self._xslimit_vs_mmed_widthdict[width].iteritems():
				self._xslimit_width_mmed_tg.SetPoint(self._xslimit_width_mmed_tg.GetN(), mmed, width, xslimit)

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
			raise ValueError("Missing input limit points. Is the input limit grid complete? I need a full rectangular grid.")

	def convert_width_to_mdm(self):
		""" Convert dilepton limits (sigma95 vs width vs mZp) to (sigma95 vs mDM vs mZp)
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

		# Make arrays for scipy.interpolate: coarse mmed, fine mdm, vs xs95
		coarse_x = np.array(self._limit_mmeds)
		fine_y = np.array(self._mdms)
		x = []
		y = []
		z = []
		zz = np.zeros((fine_y.size, coarse_x.size))
		#print(zz.shape)
		#z = np.zeros((coarse_x.size, fine_y.size))
		self._intermediate_xslimit = ROOT.TGraph2D()
		for ix, mmed in enumerate(coarse_x):
			for iy, mdm in enumerate(fine_y):
				x.append(mmed)
				y.append(mdm)
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
				z.append(tg_xslimit_width_mmeddict[mmed].Eval(width))
				zz[iy, ix] = tg_xslimit_width_mmeddict[mmed].Eval(width)
				self._intermediate_xslimit.SetPoint(self._intermediate_xslimit.GetN(), x[-1], y[-1], z[-1])

		# Create interpolation
		#self._xslimit_interpolation = interpolate.interp2d(np.array(x), np.array(y), np.log(np.array(z)) / math.log(10.), bounds_error=False, fill_value=10., kind="linear")
		self._xslimit_interpolation = interpolate.interp2d(coarse_x, fine_y, zz, bounds_error=False, fill_value=20., kind="linear")
		self._logxslimit_interpolation = interpolate.interp2d(coarse_x, fine_y, np.log(zz) / math.log(10.), bounds_error=False, fill_value=20., kind="linear")

		# Fill TGraph2D with interpolated results
		self._xslimit_tg = ROOT.TGraph2D()
		for mmed in self._mmeds:
			for mdm in self._mdms:
				self._xslimit_tg.SetPoint(self._xslimit_tg.GetN(), mmed, mdm, self._xslimit_interpolation(mmed, mdm))

	def load_xsref(self, path_to_file):
		"""Loads DMSIMP cross sections from David's text file
			Stored as dict of TGraph(1D)s. 
			{scenario: {mDM: TGraph(mmed, xs)}}
		"""

		# Load reference cross sections from Madgraph
		data = np.loadtxt(path_to_file, dtype=float)
		mmeds = []
		mdms = []
		ref_xsbrl_gen = []
		ref_xsbrl_dict = {}
		self._input_xsref = ROOT.TGraph2D()
		for mmed, mdm, xs in data:
			mmeds.append(mmed)
			mdms.append(mdm)
			ref_xsbrl_gen.append(xs)
			ref_xsbrl_dict[(mmed, mdm)] = xs
			self._input_xsref.SetPoint(self._input_xsref.GetN(), mmed, mdm, xs)

		# Convert to grid format, and fill in missing values
		mmeds = np.array(sorted(list(set(mmeds))))
		mdms = list(set(mdms))
		max_mmed = max(mmeds)
		mdms = sorted(list(set(mdms)))
		mdms.extend([max_mmed - x for x in mdms])
		mdms = np.array(sorted(list(set(mdms))))

		#z = np.zeros((len(mmeds), len(mdms)))
		x = []
		y = []
		z = []
		zz = np.zeros((len(mdms), len(mmeds)))
		self._intermediate_xsref = ROOT.TGraph2D()
		for ix, mmed in enumerate(mmeds):
			for iy, mdm in enumerate(mdms):
				x.append(mmed)
				y.append(mdm)
				if (mmed, mdm) in ref_xsbrl_dict:
					z.append(ref_xsbrl_dict[(mmed, mdm)])
					zz[iy, ix] = ref_xsbrl_dict[(mmed, mdm)]
				else:
					if 2 * mdm > mmed:
						if (mmed, mmed/2.) in ref_xsbrl_dict:
							z.append(ref_xsbrl_dict[(mmed, mmed/2.)])
							zz[iy, ix] = ref_xsbrl_dict[(mmed, mmed/2.)]
						else:
							found_replacement = False
							for mmed2, mdm2 in ref_xsbrl_dict.keys():
								if mmed2 == mmed and mdm2 >= mmed2 / 2.:
									z.append(ref_xsbrl_dict[(mmed2, mdm2)])
									zz[iy, ix] = ref_xsbrl_dict[(mmed2, mdm2)]
									found_replacement = True
									break
							if not found_replacement:
								raise ValueError("Couldn't find xs for (mmed, mdm)=({}, {})".format(mmed, mdm))
				self._intermediate_xsref.SetPoint(self._intermediate_xsref.GetN(), x[-1], y[-1], z[-1])
		#print(mmeds.shape)
		#print(mdms.shape)
		#print(z.shape)
		#self._xsref_interpolation = interpolate.interp2d(np.array(mmeds), np.array(mdms), np.log(np.array(z)) / math.log(10.), bounds_error=False, fill_value=1.e-10, kind="linear")
		self._xsref_interpolation = interpolate.interp2d(np.array(mmeds), np.array(mdms), zz, bounds_error=False, fill_value=-20, kind="linear")
		self._logxsref_interpolation = interpolate.interp2d(np.array(mmeds), np.array(mdms), np.log(zz) / math.log(10.), bounds_error=False, fill_value=-20, kind="linear")

		# Convert to TGraphs
		ref_xsbrl_graphs = {}
		self._xsref_tg = ROOT.TGraph2D()
		for mmed in self._mmeds:
			for mdm in self._mdms:
				self._xsref_tg.SetPoint(self._xsref_tg.GetN(), mmed, mdm, self._xsref_interpolation(mmed, mdm)[0])

		for mmed in [200, 500, 1000, 2000, 4000]:
			for mdm in [mmed/4., mmed/2., mmed*0.75, mmed]:
				print "xsref({}, {}) = {}".format(mmed, mdm, self._xsref_interpolation(mmed, mdm))

	def compute_contour(self):
		self._dxs_tg = ROOT.TGraph2D()
		for mmed in self._mmeds:
			for mdm in self._mdms:
				logxsref = self._logxsref_interpolation(mmed, mdm)
				logxslimit = self._logxslimit_interpolation(mmed, mdm)
				#if xsref <= 0 or xsref > 1.e9 or xslimit <= 0 or xslimit > 1.e9:
				#	print("[compute_contour] DEBUG : Skipping (mmed, mdm)=({}, {}), xsref={}, xslimit={}".format(mmed, mdm, xsref, xslimit))
				#	continue
				if logxsref < -19. or logxsref > 19. or logxslimit < -19. or logxslimit > 19.:
					print("[compute_contour] DEBUG : Skipping (mmed, mdm)=({}, {}), logxsref={}, logxslimit={}".format(mmed, mdm, logxsref, logxslimit))
					continue
				self._dxs_tg.SetPoint(self._dxs_tg.GetN(), mmed, mdm, logxsref - logxslimit)

		# Add padding
		xmin = min(self._limit_mmeds)
		self._dxs_tg.SetPoint(self._dxs_tg.GetN(), xmin - 0.001, min(self._mdms) - 0.001, -0.001)
		for mdm in self._mdms:
			self._dxs_tg.SetPoint(self._dxs_tg.GetN(), xmin - 0.001, mdm, -0.001)
		self._dxs_tg.SetPoint(self._dxs_tg.GetN(), xmin - 0.001, max(self._mdms) + 0.001, -0.001)
		
		yinf = max(self._mdms) + 0.001
		self._dxs_tg.SetPoint(self._dxs_tg.GetN(), min(self._mmeds) - 0.001, yinf, -0.001)
		for mmed in self._mmeds:
			self._dxs_tg.SetPoint(self._dxs_tg.GetN(), mmed, yinf, -0.001)
		self._dxs_tg.SetPoint(self._dxs_tg.GetN(), max(self._mmeds), yinf, -0.001)

		#xmin = min(self._mmeds)
		#xmax = max(self._mmeds)
		#ymin = min(self._mdms)
		#ymax = max(self._mdms)
		#for mdm in self._mdms:
		#	self._dxs_tg.SetPoint(self._dxs_tg.GetN(), xmin - 0.01, mdm, -40.)
		#	self._dxs_tg.SetPoint(self._dxs_tg.GetN(), xmax + 0.01, mdm, -40.)
		#for mmed in self._mmeds:
		#	self._dxs_tg.SetPoint(self._dxs_tg.GetN(), mmed, ymin - 0.01, -40.)
		#	self._dxs_tg.SetPoint(self._dxs_tg.GetN(), mmed, ymax + 0.01, -40.)

		#self._dxs_tg.SetPoint(self._dxs_tg.GetN(), xmin - 0.01, ymin - 0.01, -40.)
		#self._dxs_tg.SetPoint(self._dxs_tg.GetN(), xmax + 0.01, ymin - 0.01, -40.)
		#self._dxs_tg.SetPoint(self._dxs_tg.GetN(), xmin - 0.01, ymax + 0.01, -40.)
		#self._dxs_tg.SetPoint(self._dxs_tg.GetN(), xmax + 0.01, ymax + 0.01, -40.)

		self._limit_contours = self._dxs_tg.GetContourList(0.)

		# Combine contours into one shape.
		self._combined_contour = self._limit_contours[0]
		# Not guaranteed to work for anything beyond EXO-19-019.
		"""
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
		"""

	def get_contours(self):
		return self._limit_contours

	def get_combined_contour(self):
		return self._combined_contour

	def get_xslimit_graph(self):
		return self._xslimit_tg

	def get_xsref_graph(self):
		return self._xsref_tg

	def get_input_xsref_graph(self):
		return self._input_xsref

	def get_dxs_graph(self):
		return self._dxs_tg

	def get_input_limits(self):
		return self._xslimit_width_mmed_tg



if __name__ == "__main__":
	for scenario in ["V2", "A2"]:
		output_file = ROOT.TFile("ScanMM/contours_dilepton_{}.root".format(scenario), "RECREATE")

		# Observed
		converter = DileptonConverterFine(scenario)
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
			0.05: "raw/ZPrime_limitCard_Run2_width05_Obs_legcay.txt",
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
		converter.get_dxs_graph().SetName("obs_dxs")
		converter.get_dxs_graph().Write()
		converter.get_input_limits().SetName("obs_inputlimits")
		converter.get_input_limits().Write()

		converter.get_xsref_graph().SetName("xsref")
		converter.get_xsref_graph().Write()
		converter.get_input_xsref_graph().SetName("inputxsref")
		converter.get_input_xsref_graph().Write()
		converter._intermediate_xsref.SetName("debugxsref")
		converter._intermediate_xsref.Write()
		converter._intermediate_xslimit.SetName("obs_mdmlimits")
		converter._intermediate_xslimit.Write()

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
			converter_exp = DileptonConverterFine(scenario)
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
			converter_exp.get_dxs_graph().SetName("exp_{}_dxs".format(expname))
			converter_exp.get_dxs_graph().Write()
			converter_exp.get_input_limits().SetName("exp_{}_inputlimits".format(expname))
			converter_exp.get_input_limits().Write()
			converter_exp._intermediate_xslimit.SetName("exp_{}_mdmlimits".format(expname))
			converter_exp._intermediate_xslimit.Write()

		output_file.Close()
