import os
import sys
import math
from scipy.optimize import fsolve
import ROOT
from ROOT import TCanvas, TLegend, TGraph, TF1, TLatex, TH1D, TColor
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

from dijet_data import DijetData
from zprime_equations import *
from cms_label import CMSLabel

from seaborn_colors import SeabornColors
seaborn_colors = SeabornColors()
palette_dir = os.path.expandvars("$CMSSW_BASE/src/ExoDMSummaryPlots/GQSummary/python/seaborn_palettes")
seaborn_colors.load_palette("Blues_d", palette_dir=palette_dir)
seaborn_colors.load_palette("Reds_d", palette_dir=palette_dir)
seaborn_colors.load_palette("Oranges_d", palette_dir=palette_dir)
seaborn_colors.load_palette("Greens_d", palette_dir=palette_dir)
seaborn_colors.load_palette("Purples_d", palette_dir=palette_dir)
seaborn_colors.load_palette("RdPu_r", palette_dir=palette_dir)


class GQSummaryPlot:
	def __init__(self, name):
		self._name = name
		self._analyses = []
		self._dijet_data = {}
		self._legend_entries = {}
		self._graphs = {}
		self._limit_fills = {}
		self._GoMs = []
		self._vtype = "vector"
		self._style = {"default":{
			"line_color":1,
			"line_width":402,
			"line_style":1,
			"marker_style":20,
			"marker_size":0,
			"marker_color":1,
			"fill_style":3004,
			"fill_color":0,
			"alpha":1.
			}
		}
		self._tranparency = {}


	# style = dict of <analysis name>:{"line_color":1, "marker_style":20, etc}
	# See the default option in __init__ for the full list of options
	def set_style(self, style):
		self._style.update(style)

	def set_vtype(self, vtype):
		vtype = vtype.lower()
		if not vtype in ["vector", "axial"]:
			raise ValueError("[set_vtype] Argument vtype must be 'vector' or 'axial'")
		self._vtype = vtype

	def add_data(self, dijet_data, name, legend, truncate_gq=False, truncate_gom=False, min_gom=False):
		self._analyses.append(name)
		self._dijet_data[name] = dijet_data
		self._legend_entries[name] = legend

		if truncate_gq and truncate_gom:
			raise ValueError("[GQSummaryPlot::add_data] ERROR : Cannot specify both truncate_gq and truncate_gom.")

		if truncate_gq:
			max_truncated_graphs = self.truncate_graph_gq(dijet_data.get_graph(), truncate_gq[1])
			truncated_graphs = []
			if truncate_gq[0] > 0:
				for tmpgraph in max_truncated_graphs:
					truncated_graphs.extend(self.truncate_graph_gq(tmpgraph, truncate_gq[0], invert=-1))
			else:
				truncated_graphs = max_truncated_graphs

			# If the truncation deleted all points, abandon
			if len(truncated_graphs) == 0:
				print "[GQSummaryPlot::add_data] ERROR : Applying truncate_gq resulted in an empty graph! Remove from the input list."
				print "[GQSummaryPlot::add_data] ERROR : truncate_gq = {}".format(truncate_gq)
				dijet_data.get_graph().Print("all")
				sys.exit(1)

			# Save the new set of graphs
			for i, graph in enumerate(truncated_graphs):
				piece_name = name
				if i != 0:
					piece_name += str(i)
					self._analyses.append(piece_name)
					self._style[piece_name] = self._style[name]
					self._legend_entries[piece_name] = False
				self._graphs[piece_name] = truncated_graphs[i]
		elif truncate_gom:
			print "DEBUG : Truncating graph {} to range {}".format(name, truncate_gom)
			max_truncated_graphs = self.truncate_graph_gom(dijet_data.get_graph(), truncate_gom[1])
			truncated_graphs = []
			if truncate_gom[0] > 0:
				for tmpgraph in max_truncated_graphs:
					truncated_graphs.extend(self.truncate_graph_gom(tmpgraph, truncate_gom[0], invert=-1))
			else:
				truncated_graphs = max_truncated_graphs

			# If the truncation deleted all points, abandon
			if len(truncated_graphs) == 0:
				print "[GQSummaryPlot::add_data] ERROR : Applying truncate_gom resulted in an empty graph! Remove from the input list."
				print "[GQSummaryPlot::add_data] ERROR : truncate_gom = {}".format(truncate_gom)
				dijet_data.get_graph().Print("all")
				sys.exit(1)

			# Save the new set of graphs
			for i, graph in enumerate(truncated_graphs):
				piece_name = name
				if i != 0:
					piece_name += str(i)
					self._analyses.append(piece_name)
					self._style[piece_name] = self._style[name]
					self._legend_entries[piece_name] = False
				self._graphs[piece_name] = truncated_graphs[i]
		else:
			self._graphs[name] = dijet_data.get_graph()

		#if max_gom_fill:
		#	self._limit_fills[name] = self.create_limit_gom_fill(dijet_data.get_graph(), max_gom_fill)
		#if max_gq_fill:
		#	self._limit_fills[name] = self.create_limit_gq_fill(dijet_data.get_graph(), max_gq_fill)

	# Add legend entry with no object
	def add_legend_only(self, name, legend_entry):
		self._legend_entries[name] = legend_entry
		self._analyses.append(name)
		self._graphs[name] = 0


	def set_width_curves(self, GoMs):
		self._GoMs = GoMs

	def style_graph(self, graph, name):
		if not name in self._style:
			print "[style_graph] ERROR : Analysis {} is not present in the style dict. Please add.".format(name)
			sys.exit(1)
		if "line_color" in self._style[name]:
			if "alpha" in self._style[name]:
				graph.SetLineColorAlpha(self._style[name]["line_color"], self._style[name]["alpha"])
			else:
				graph.SetLineColor(self._style[name]["line_color"])
		else:
			if "alpha" in self._style[name]:
				graph.SetLineColorAlpha(self._style["default"]["line_color"], self._style["default"]["alpha"])
			else:
				graph.SetLineColor(self._style["default"]["line_color"])
		if "line_style" in self._style[name]:
			graph.SetLineStyle(self._style[name]["line_style"])
		else:
			graph.SetLineStyle(self._style["default"]["line_style"])
		if "line_width" in self._style[name]:
			graph.SetLineWidth(self._style[name]["line_width"])
		else:
			graph.SetLineWidth(self._style["default"]["line_width"])
		if "marker_color" in self._style[name]:
			if "alpha" in self._style[name]:
				graph.SetMarkerColorAlpha(self._style[name]["marker_color"], self._style[name]["alpha"])
			else:
				graph.SetMarkerColor(self._style[name]["marker_color"])
		else:
			if "alpha" in self._style[name]:
				graph.SetMarkerColorAlpha(self._style["default"]["marker_color"], self._style["default"]["alpha"])
			else:
				graph.SetMarkerColor(self._style["default"]["marker_color"])
		if "marker_style" in self._style[name]:
			graph.SetMarkerStyle(self._style[name]["marker_style"])
		else:
			graph.SetMarkerStyle(self._style["default"]["marker_style"])
		if "marker_size" in self._style[name]:
			graph.SetMarkerSize(self._style[name]["marker_size"])
		else:
			graph.SetMarkerSize(self._style["default"]["marker_size"])
		if "fill_style" in self._style[name]:
			graph.SetFillStyle(self._style[name]["fill_style"])
		else:
			graph.SetFillStyle(self._style["default"]["fill_style"])
		if "fill_color" in self._style[name]:
			if "alpha" in self._style[name]:
				graph.SetFillColorAlpha(self._style[name]["fill_color"], self._style[name]["alpha"])
			else:
				graph.SetFillColor(self._style[name]["fill_color"])
		else:
			if "alpha" in self._style[name]:
				graph.SetFillColorAlpha(self._style["default"]["fill_color"], self._style["default"]["alpha"])
			else:
				graph.SetFillColor(self._style["default"]["fill_color"])

	# Returns a set of graphs with a maximum g_q (or minimum; specify invert=-1)
	def truncate_graph_gq(self, limit_graph, max_gq, invert=1):
		# Calculate the sets of x values for the new graphs
		limit_x = limit_graph.GetX()
		limit_y = limit_graph.GetY()
		x_points = [[]]
		y_points = [[]]
		if invert * limit_y[0] < invert * max_gq:
			x_points[-1].append(limit_x[0])
			y_points[-1].append(limit_y[0])
		for i in xrange(1, len(limit_x)):
			if invert * limit_y[i - 1] < invert * max_gq and invert * limit_y[i] < invert * max_gq:
				x_points[-1].append(limit_x[i])
				y_points[-1].append(limit_y[i])
			elif invert * limit_y[i - 1] > invert * max_gq and invert * limit_y[i] < invert * max_gq: # limit crosses max_gq going down: new set
				print "Solving for bad-to-good crossing (max_gq={}).".format(max_gq)
				print "(m1, gq1) = ({}, {})".format(limit_x[i-1], limit_y[i-1])
				print "(m2, gq2) = ({}, {})".format(limit_x[i], limit_y[i])

				if len(x_points[-1]) >= 1:
					x_points.append([])
					y_points.append([])
				# Calculate crossing point		
				x_cross_array = fsolve(lambda x : limit_graph.Eval(x) - max_gq, (limit_x[i-1]+limit_x[i])/2.)
				if len(x_cross_array) != 1:
					raise ValueError("ERROR : Found more than one crossing!")
				x_cross = x_cross_array[0]
				print "Found crossing (m, gq) = ({}, {})".format(x_cross, limit_graph.Eval(x_cross))
				'''
				# Old method: analytical solution by hand
				# max_gq = limit_y[i-1] + (limit_y[i]-limit_y[i-1])/(limit_x[i]-limit_x[i-1]) * dx
				slope = (limit_y[i]-limit_y[i-1])/(limit_x[i]-limit_x[i-1])
				dx = (max_gq - limit_y[i-1]) / slope
				x_cross = limit_x[i-1] + dx
				x_points[-1].append(x_cross)
				x_points[-1].append(limit_x[i])
				y_points[-1].append(limit_graph.Eval(x_cross))
				y_points[-1].append(limit_graph.Eval(limit_x[i]))
				'''
				x_points[-1].append(x_cross)
				x_points[-1].append(limit_x[i])
				y_points[-1].append(limit_graph.Eval(x_cross))
				y_points[-1].append(limit_graph.Eval(limit_x[i]))

			elif invert * limit_y[i - 1] < invert * max_gq and invert * limit_y[i] > invert * max_gq: # limit crosses max_gq going up: end this set with crossing value
				print "Solving for good-to-bad crossing (max_gq={}).".format(max_gq)
				print "(m1, gq1) = ({}, {})".format(limit_x[i-1], limit_y[i-1])
				print "(m2, gq2) = ({}, {})".format(limit_x[i], limit_y[i])
				# Calculate crossing point
				x_cross_array = fsolve(lambda x : limit_graph.Eval(x) - max_gq, (limit_x[i-1]+limit_x[i])/2.)
				if len(x_cross_array) != 1:
					raise ValueError("ERROR : Found more than one crossing!")
				x_cross = x_cross_array[0]
				# max_gq = limit_y[i-1] + (limit_y[i]-limit_y[i-1])/(limit_x[i]-limit_x[i-1]) * dx
				'''
				# Old method: analytical solution by hand
				slope = (limit_y[i]-limit_y[i-1])/(limit_x[i]-limit_x[i-1])
				dx = (max_gq - limit_y[i-1]) / slope
				x_cross = limit_x[i-1] + dx
				'''
				x_points[-1].append(x_cross)
				y_points[-1].append(limit_graph.Eval(x_cross))
				print "Found crossing (m, gq) = ({}, {})".format(x_cross, limit_graph.Eval(x_cross))
			else: # Both above limit: ignore point
				pass

		# Convert sets of points to graphs
		new_graphs = []
		for igraph in xrange(len(x_points)):
			if len(x_points[igraph]) == 0:
				print "[gq_summary_plot::truncate_graph_gq] WARNING : Graph has zero points".format(self._name)
				print x_points
				print y_points
			else:
				new_graphs.append(TGraph(len(x_points[igraph])))
				for ipoint in xrange(len(x_points[igraph])):
					new_graphs[igraph].SetPoint(ipoint, x_points[igraph][ipoint], y_points[igraph][ipoint])
		return new_graphs


	# Returns a set of graphs with a maximum Gamma/M (or minimum; specify invert=-1)
	def truncate_graph_gom(self, limit_graph, max_gom, invert=1):
		# Calculate the sets of x values for the new graphs
		limit_x = limit_graph.GetX()
		limit_y = limit_graph.GetY()
		limit_gom = [Gamma_qq_tot(limit_y[i], limit_x[i], "vector") / limit_x[i] for i in xrange(limit_graph.GetN())]
		x_points = [[]]
		y_points = [[]]
		if invert * limit_gom[0] < invert * max_gom:
			x_points[-1].append(limit_x[0])
			y_points[-1].append(limit_y[0])
		for i in xrange(1, len(limit_x)):
			if invert * limit_gom[i - 1] < invert * max_gom and invert * limit_gom[i] < invert * max_gom:
				x_points[-1].append(limit_x[i])
				y_points[-1].append(limit_y[i])
			elif invert * limit_gom[i - 1] > invert * max_gom and invert * limit_gom[i] < invert * max_gom: # limit crosses max_gom going down: new set
				if len(x_points[-1]) >= 1:
					x_points.append([])
					y_points.append([])

				# Calculate crossing point				
				print "Solving for good-to-bad crossing (max_gom={}).".format(max_gom)
				print "(m1, gq1, gom1) = ({}, {}, {})".format(limit_x[i-1], limit_y[i-1], limit_gom[i-1])
				print "(m2, gq2, gom2) = ({}, {}, {})".format(limit_x[i], limit_y[i], limit_gom[i])
				x_cross_array = fsolve(lambda x : Gamma_qq_tot(limit_graph.Eval(x), x, "vector") / x - max_gom, (limit_x[i-1]+limit_x[i])/2.)
				if len(x_cross_array) != 1:
					raise ValueError("ERROR : Found more than one crossing!")
				x_cross = x_cross_array[0]
				print "Found crossing (m, gq, gom) = ({}, {}, {})".format(x_cross, limit_graph.Eval(x_cross), Gamma_qq_tot(limit_graph.Eval(x_cross), x_cross, "vector") / x_cross)
				'''
				# Old method: analytical solution by hand
				# max_gom = limit_y[i-1] + (limit_y[i]-limit_y[i-1])/(limit_x[i]-limit_x[i-1]) * dx
				slope = (limit_y[i]-limit_y[i-1])/(limit_x[i]-limit_x[i-1])
				dx = (max_gom - limit_y[i-1]) / slope
				x_cross = limit_x[i-1] + dx
				x_points[-1].append(x_cross)
				x_points[-1].append(limit_x[i])
				y_points[-1].append(limit_graph.Eval(x_cross))
				y_points[-1].append(limit_graph.Eval(limit_x[i]))
				'''
				x_points[-1].append(x_cross)
				x_points[-1].append(limit_x[i])
				y_points[-1].append(limit_graph.Eval(x_cross))
				y_points[-1].append(limit_graph.Eval(limit_x[i]))

			elif invert * limit_gom[i - 1] < invert * max_gom and invert * limit_gom[i] > invert * max_gom: # limit crosses max_gom going up: end this set with crossing value
				# Calculate crossing point
				print "Solving for good-to-bad crossing (max_gom={}).".format(max_gom)
				print "(m1, gq1, gom1) = ({}, {}, {})".format(limit_x[i-1], limit_y[i-1], limit_gom[i-1])
				print "(m2, gq2, gom2) = ({}, {}, {})".format(limit_x[i], limit_y[i], limit_gom[i])
				x_cross_array = fsolve(lambda x : Gamma_qq_tot(limit_graph.Eval(x), x, "vector") / x - max_gom, (limit_x[i-1]+limit_x[i])/2.)
				if len(x_cross_array) != 1:
					raise ValueError("ERROR : Found more than one crossing!")
				x_cross = x_cross_array[0]
				print "Found crossing (m, gq, gom) = ({}, {}, {})".format(x_cross, limit_graph.Eval(x_cross), Gamma_qq_tot(limit_graph.Eval(x_cross), x_cross, "vector") / x_cross)
				# max_gom = limit_y[i-1] + (limit_y[i]-limit_y[i-1])/(limit_x[i]-limit_x[i-1]) * dx
				'''
				# Old method: analytical solution by hand
				slope = (limit_y[i]-limit_y[i-1])/(limit_x[i]-limit_x[i-1])
				dx = (max_gom - limit_y[i-1]) / slope
				x_cross = limit_x[i-1] + dx
				'''
				x_points[-1].append(x_cross)
				y_points[-1].append(limit_graph.Eval(x_cross))
			else: # Both above limit: ignore point
				pass

		# Convert sets of points to graphs
		new_graphs = []
		for igraph in xrange(len(x_points)):
			if len(x_points[igraph]) == 0:
				print "[gq_summary_plot::truncate_graph_gom] WARNING : Graph has zero points : {}".format(self._name)
				print x_points
				print y_points
			else:
				new_graphs.append(TGraph(len(x_points[igraph])))
				for ipoint in xrange(len(x_points[igraph])):
					new_graphs[igraph].SetPoint(ipoint, x_points[igraph][ipoint], y_points[igraph][ipoint])
		return new_graphs

	def draw(self, 
		logx=False, 
		logy=False, 
		x_title="M_{Z'} [GeV]", 
		y_title="g'_{q}", 
		x_range=[40., 7000.],
		y_range=[0, 1.45],
		canvas_dim=[1800, 1200],
		canvas_rm=0.32,
		legend_coords=[0.69, 0.17, 0.99, 0.9],
		draw_cms=None,
		legend_text_size=0.028,
		legend_ncolumns=None,
		legend_obsexp=False, # Add a solid and dotted line to legend for obs and exp
		legend_header="#bf{95% CL exclusions}",
		draw_Z_constraint=False,
		z_width_legend_entry="#splitline{Z width (all #Gamma_{Z'}/M_{Z'})}{#it{[arXiv:1404.3947]}}",
		draw_upsilon_constraint=False,
		upsilon_width_legend_entry="#splitline{#Upsilon width (all #Gamma_{Z'}/M_{Z'})}{#it{[arXiv:1404.3947]}}",
		gom_x=None, # x coordinate for Gamma/M labels
		model_label=False, # Add a string specifying the model on the plot
		gom_fills=False, # Draw limit fills including upper boundaries
		conference_label=False # Draw "timestamp" label, i.e. "Moriond 2018"
		):
		canvas_name = "c_{}_{}_{}{}".format(self._name, ("logx" if logx else "linearx"), ("logy" if logy else "lineary"), ("_gomfills" if gom_fills else ""))
		self._canvas = TCanvas(canvas_name, canvas_name, canvas_dim[0], canvas_dim[1])
		ROOT.gStyle.SetPadTickX(1)
		ROOT.gStyle.SetPadTickY(1)
		self._canvas.SetLeftMargin(0.09)
		self._canvas.SetBottomMargin(0.12)
		self._canvas.SetTopMargin(0.075)
		self._canvas.SetRightMargin(canvas_rm)

		if logx:
			self._canvas.SetLogx()
		if logy:
			self._canvas.SetLogy()
		self._canvas.SetTicks(1, 1)
		self._canvas.cd()
		self._legend = TLegend(legend_coords[0], legend_coords[1], legend_coords[2], legend_coords[3])
		self._legend.SetFillStyle(0)
		self._legend.SetBorderSize(0)
		self._legend.SetTextSize(legend_text_size)
		if legend_ncolumns:
			self._legend.SetNColumns(legend_ncolumns)
		
		# Legend headers and obs/exp lines
		self._legend.SetHeader(legend_header)
		if legend_obsexp:
			self._g_obs_dummy = TGraph(10)
			self._g_obs_dummy.SetLineStyle(1)
			self._g_obs_dummy.SetLineColor(1)
			self._g_obs_dummy.SetLineWidth(402)
			self._g_obs_dummy.SetMarkerStyle(20)
			self._g_obs_dummy.SetMarkerSize(0)
			self._g_obs_dummy.SetFillStyle(3004)
			self._g_obs_dummy.SetFillColor(1)
			self._legend.AddEntry(self._g_obs_dummy, "Observed", "lf")
			self._g_exp_dummy = TGraph(10)
			self._g_exp_dummy.SetLineStyle(2)
			self._g_exp_dummy.SetLineColor(1)
			self._g_exp_dummy.SetLineWidth(402)
			self._g_exp_dummy.SetMarkerStyle(20)
			self._g_exp_dummy.SetMarkerSize(0)
			self._legend.AddEntry(self._g_exp_dummy, "Expected", "l")

		self._frame = TH1D("frame", "frame", 100, x_range[0], x_range[1])
		self._frame.SetDirectory(0)
		self._frame.GetYaxis().SetRangeUser(y_range[0], y_range[1])
		self._frame.GetXaxis().SetTitle(x_title)
		self._frame.GetYaxis().SetTitle(y_title)
		self._frame.Draw("axis")
		if logx:
			self._frame.GetXaxis().SetMoreLogLabels()
			self._frame.GetXaxis().SetNdivisions(10)
			self._frame.GetXaxis().SetNoExponent(True)
		self._frame.GetXaxis().SetTitleOffset(1.)
		self._frame.GetXaxis().SetTitleSize(0.05)
		self._frame.GetXaxis().SetLabelSize(0.04)
		self._frame.GetYaxis().SetTitleOffset(0.8)
		self._frame.GetYaxis().SetTitleSize(0.05)
		self._frame.GetYaxis().SetLabelSize(0.04)
		#if logy:
		#	self._frame.GetYaxis().SetMoreLogLabels()

		# Draw limit fills first, if any
		for name, limit_fill in self._limit_fills.iteritems():
			self._limit_fills[name].SetFillStyle(3003)
			self._limit_fills[name].SetFillColor(self._style[name]["fill_color"])
			self._limit_fills[name].Draw("F")

		legend_entry_count = 0
		for analysis_name in self._analyses:
			if self._graphs[analysis_name]:
				self.style_graph(self._graphs[analysis_name], analysis_name)
				self._graphs[analysis_name].Draw("lp")
				if self._legend_entries[analysis_name] != False:
					self._legend.AddEntry(self._graphs[analysis_name], self._legend_entries[analysis_name], "l")
					legend_entry_count += 1
			else:
				self._legend.AddEntry(0, self._legend_entries[analysis_name], "")
				legend_entry_count += 1

		# Add an empty entry if needed, to put Z/Y constraints on the same line
		if legend_entry_count % 2 == 1:
		   self._legend.AddEntry(0, "", "")

		if draw_Z_constraint:
			self._tf_Z_constraint = TF1("Z_constraint", gq_Z_constraint, x_range[0], x_range[1], 0)
			self._tf_Z_constraint.SetNpx(1000)
			self._tf_Z_constraint.SetLineColor(17)
			ROOT.gStyle.SetLineStyleString(9, "40 20");
			self._tf_Z_constraint.SetLineStyle(9)
			self._tf_Z_constraint.SetLineWidth(2)
			self._tf_Z_constraint.Draw("same")
			self._legend.AddEntry(self._tf_Z_constraint, z_width_legend_entry, "l")

		if draw_upsilon_constraint:
			self._tf_upsilon_constraint = TF1("upsilon_constraint", gq_upsilon_constraint, x_range[0], x_range[1], 0)
			self._tf_upsilon_constraint.SetNpx(1000)
			self._tf_upsilon_constraint.SetLineColor(17)
			ROOT.gStyle.SetLineStyleString(11, "20 10");
			self._tf_upsilon_constraint.SetLineStyle(11)
			self._tf_upsilon_constraint.SetLineWidth(2)
			self._tf_upsilon_constraint.Draw("same")
			self._legend.AddEntry(self._tf_upsilon_constraint, upsilon_width_legend_entry, "l")

		# Lines at fixed Gamma / M
		self._GoM_tf1s = {}
		self._GoM_labels = {}
		for i, GoM in enumerate(self._GoMs):
			self._GoM_tf1s[GoM] = TF1("tf1_gq_{}".format(GoM), lambda x, this_gom=GoM: gom_to_gq(this_gom, x[0], self._vtype), x_range[0], x_range[1], 0) # 
			self._GoM_tf1s[GoM].SetLineColor(ROOT.kGray+1)
			self._GoM_tf1s[GoM].SetLineStyle(ROOT.kDashed)
			self._GoM_tf1s[GoM].SetLineWidth(1)
			self._GoM_tf1s[GoM].Draw("same")

			# TLatex for Gamma / M
			if gom_x:
				label_x = gom_x
			else: 
				if logx:
					label_xfrac = 0.05
				else:
					label_xfrac = 0.864
				label_x = (x_range[1] - x_range[0]) * label_xfrac + x_range[0]
			if logy:
				label_y = self._GoM_tf1s[GoM].Eval(label_x) * 0.85
				gom_text = "#Gamma_{{Z'}}#kern[-0.6]{{ }}/#kern[-0.7]{{ }}M_{{Z'}}#kern[-0.7]{{ }}=#kern[-0.7]{{ }}{}%".format(int(GoM * 100))
			else:
				# label_y = self._GoM_tf1s[GoM].Eval(label_x) - 0.085 # For labels under the line
				label_y = self._GoM_tf1s[GoM].Eval(label_x) + 0.05 # For labels over the line
				gom_text = "#frac{{#Gamma}}{{M_{{Z'}}}} = {}%".format(int(GoM * 100))
			self._GoM_labels[GoM] = TLatex(label_x, label_y, gom_text)
			if logy:
				self._GoM_labels[GoM].SetTextSize(0.028)
			else:
				self._GoM_labels[GoM].SetTextSize(0.027)
			self._GoM_labels[GoM].SetTextColor(ROOT.kGray+1)
			self._GoM_labels[GoM].Draw("same")

		# Vector label
		if model_label:
			self._model_label = TLatex(model_label["x"], model_label["y"], model_label["text"])
			if not "size_modifier" in model_label.keys():
				model_label["size_modifier"] = 1.
			self._model_label.SetTextSize(0.04 * model_label["size_modifier"])
			self._model_label.SetTextColor(1)
			self._model_label.Draw("same")

		# Legend last, to be on top of lines
		self._legend.Draw()

		if draw_cms:
			CMSLabel(self._canvas, extra_text=draw_cms, halign="left", valign="top", in_frame=False)

		if conference_label:
			self._conference_label = TLatex(conference_label["x"], conference_label["y"], conference_label["text"])
			self._conference_label.SetTextSize(0.045)
			self._conference_label.SetTextColor(1)
			self._conference_label.Draw("same")

		# Redraw axis
		self._frame.Draw("axis same")

	def cd(self):
		self._canvas.cd()

	def save(self, folder, exts=["pdf"]):
		for ext in exts:
			self._canvas.SaveAs("{}/{}.{}".format(folder, self._canvas.GetName(), ext))

