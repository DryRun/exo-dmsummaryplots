import os
import sys
import math
import ROOT
from ROOT import TCanvas, TLegend, TF1, TLatex, TH1D, TColor
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

sys.path.append("./python/")
from dijet_data import DijetData
from zprime_equations import *

from seaborn_colors import SeabornColors
seaborn_colors = SeabornColors()
seaborn_colors.load_palette("Blues_d", palette_dir="./python/seaborn_palettes")
seaborn_colors.load_palette("Reds_d", palette_dir="./python/seaborn_palettes")
seaborn_colors.load_palette("Oranges_d", palette_dir="./python/seaborn_palettes")
seaborn_colors.load_palette("Greens_d", palette_dir="./python/seaborn_palettes")
seaborn_colors.load_palette("Purples_d", palette_dir="./python/seaborn_palettes")


# Set all the plot styling here
style = {
	"default":{
		"line_color":1,
		"line_width":402,
		"line_style":1,
		"marker_style":20,
		"marker_size":0,
		"marker_color":1,
		"fill_style":3004,
		"fill_color":0,
	}, "EXO16046_obs":{
		"line_color":seaborn_colors.get_root_color("Blues_d", 2),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Blues_d", 2),		
	}, "EXO16046_exp":{
		"line_color":seaborn_colors.get_root_color("Blues_d", 5),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Blues_d", 5),		
	}, "EXO16056_narrow_obs":{
		"line_color":seaborn_colors.get_root_color("Reds_d", 2),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Reds_d", 2),		
	}, "EXO16056_narrow_exp":{
		"line_color":seaborn_colors.get_root_color("Reds_d", 5),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Reds_d", 5),		
	}, "EXO16056_wide_obs":{
		"line_color":seaborn_colors.get_root_color("Purples_d", 2),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Purples_d", 2),		
	}, "EXO16056_wide_exp":{
		"line_color":seaborn_colors.get_root_color("Purples_d", 5),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Purples_d", 5),		
	}, "EXO16057_SR1_obs":{
		"line_color":seaborn_colors.get_root_color("Oranges_d", 3),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Oranges_d", 3),		
	}, "EXO16057_SR1_exp":{
		"line_color":seaborn_colors.get_root_color("Oranges_d", 5),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Oranges_d", 5),		
	}, "EXO16057_SR2_obs":{
		"line_color":seaborn_colors.get_root_color("Oranges_d", 3),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Oranges_d", 3),		
	}, "EXO16057_SR2_exp":{
		"line_color":seaborn_colors.get_root_color("Oranges_d", 5),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Oranges_d", 5),		
	}, "EXO17001_obs":{
		"line_color":seaborn_colors.get_root_color("Greens_d", 2),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Greens_d", 2),		
	}, "EXO17001_exp":{
		"line_color":seaborn_colors.get_root_color("Greens_d", 5),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Greens_d", 5),		
	}
}

legend_entries = {
	"EXO16046_obs":"Dijet #chi Obs. (EXO-16-046)",
	"EXO16046_exp":"Dijet #chi Exp. (EXO-16-046)",
	"EXO16056_narrow_obs":"Narrow Dijet Obs. (EXO-16-056)",
	"EXO16056_narrow_exp":"Narrow Dijet Exp. (EXO-16-056)",
	"EXO16056_wide_obs":"Wide Dijet Obs. (EXO-16-056)",
	"EXO16056_wide_exp":"Wide Dijet Obs. (EXO-16-056)",
	"EXO16057_SR1_obs":"Dijet w/b Tag Obs. (EXO-16-057)",
	"EXO16057_SR1_exp":"Dijet w/b Tag Exp. (EXO-16-057)",
	"EXO16057_SR2_obs":False, # Only need one of SR1/SR2 for the legend
	"EXO16057_SR2_exp":False, # Only need one of SR1/SR2 for the legend
	"EXO17001_obs":"Boosted Dijet Obs. (EXO-17-001)",
	"EXO17001_exp":"Boosted Dijet Exp. (EXO-17-001)",
}

# graph = TGraph to be styled
# name = CADI line etc
def style_graph(graph, name):
	if not name in style:
		print "[style_graph] ERROR : Analysis {} is not present in the style dict. Please add.".format(name)
		sys.exit(1)
	if "line_color" in style[name]:
		graph.SetLineColor(style[name]["line_color"])
	else:
		graph.SetLineColor(style["default"]["line_color"])
	if "line_style" in style[name]:
		graph.SetLineStyle(style[name]["line_style"])
	else:
		graph.SetLineStyle(style["default"]["line_style"])
	if "line_width" in style[name]:
		graph.SetLineWidth(style[name]["line_width"])
	else:
		graph.SetLineWidth(style["default"]["line_width"])
	if "marker_color" in style[name]:
		graph.SetMarkerColor(style[name]["marker_color"])
	else:
		graph.SetMarkerColor(style["default"]["marker_color"])
	if "marker_style" in style[name]:
		graph.SetMarkerStyle(style[name]["marker_style"])
	else:
		graph.SetMarkerStyle(style["default"]["marker_style"])
	if "marker_size" in style[name]:
		graph.SetMarkerSize(style[name]["marker_size"])
	else:
		graph.SetMarkerSize(style["default"]["marker_size"])
	if "fill_style" in style[name]:
		graph.SetFillStyle(style[name]["fill_style"])
	else:
		graph.SetFillStyle(style["default"]["fill_style"])
	if "fill_color" in style[name]:
		graph.SetFillColor(style[name]["fill_color"])
	else:
		graph.SetFillColor(style["default"]["fill_color"])


class GQSummaryPlot:
	def __init__(self):
		self._analyses = []
		self._dijet_data = {}
		self._legend_entries = {}
		self._graphs = {}
		self._GoMs = []
		self._vtype = "vector"

	def set_vtype(self, vtype):
		vtype = vtype.lower()
		if not vtype in ["vector", "axial"]:
			raise ValueError("[set_vtype] Argument vtype must be 'vector' or 'axial'")
		self._vtype = vtype

	def add_data(self, dijet_data, name, legend):
		self._analyses.append(name)
		self._dijet_data[name] = dijet_data
		self._legend_entries[name] = legend
		self._graphs[name] = dijet_data.get_graph()

	def set_width_curves(self, GoMs):
		self._GoMs = GoMs

	def draw(self, 
		logx=False, 
		logy=False, 
		x_title="m_{Med} [GeV]", 
		y_title="g'_{q}", 
		x_range=[40., 7000.],
		y_range=[0, 1.45],
		canvas_dim=[1800, 1200],
		legend_coords=[0.15, 0.4, 0.5, 0.88],
		draw_cms=None):
		canvas_name = "c_gq_{}_{}".format(("logx" if logx else "linearx"), ("logy" if logy else "lineary"))
		self._canvas = TCanvas(canvas_name, canvas_name, canvas_dim[0], canvas_dim[1])
		ROOT.gStyle.SetPadTickX(1)
		ROOT.gStyle.SetPadTickY(1)
		self._canvas.SetLeftMargin(0.09)
		self._canvas.SetBottomMargin(0.12)
		self._canvas.SetTopMargin(0.075)
		self._canvas.SetRightMargin(0.035)

		if logx:
			self._canvas.SetLogx()
		if logy:
			self._canvas.SetLogy()
		self._canvas.SetTicks(1, 1)
		self._canvas.cd()
		self._legend = TLegend(legend_coords[0], legend_coords[1], legend_coords[2], legend_coords[3])
		self._legend.SetFillColor(0)
		self._legend.SetBorderSize(0)

		self._frame = TH1D("frame", "frame", 100, x_range[0], x_range[1])
		self._frame.SetDirectory(0)
		self._frame.GetYaxis().SetRangeUser(y_range[0], y_range[1])
		self._frame.GetXaxis().SetTitle(x_title)
		self._frame.GetYaxis().SetTitle(y_title)
		self._frame.Draw("axis")
		self._frame.GetXaxis().SetMoreLogLabels()
		self._frame.GetXaxis().SetNdivisions(10)
		self._frame.GetXaxis().SetNoExponent(True)
		self._frame.GetXaxis().SetTitleOffset(1.)
		self._frame.GetXaxis().SetTitleSize(0.05)
		self._frame.GetXaxis().SetLabelSize(0.04)
		self._frame.GetYaxis().SetTitleOffset(0.8)
		self._frame.GetYaxis().SetTitleSize(0.05)
		self._frame.GetYaxis().SetLabelSize(0.04)
    


		for analysis_name in self._analyses:
			style_graph(self._graphs[analysis_name], analysis_name)
			self._graphs[analysis_name].Draw("lp")
			if self._legend_entries[analysis_name] != False:
				self._legend.AddEntry(self._graphs[analysis_name], self._legend_entries[analysis_name], "l")
		self._legend.Draw()

		# Lines at fixed Gamma / M
		GoM_tf1s = {}
		GoM_labels = {}
		for GoM in self._GoMs:
			GoM_tf1s[GoM] = TF1("tf1_gq_{}".format(GoM), lambda x: width_to_gq(GoM * x[0], x[0], self._vtype), x_range[0], x_range[1], 0)
			GoM_tf1s[GoM].SetLineColor(ROOT.kGray+1)
			GoM_tf1s[GoM].SetLineStyle(ROOT.kDashed)
			GoM_tf1s[GoM].Draw("same")

			# TLatex for Gamma / M
			if logx:
				label_xfrac = 0.14
			else:
				label_xfrac = 0.864
			label_x = (x_range[1] - x_range[0]) * label_xfrac + x_range[0]
			if logy:
				label_y = GoM_tf1s[GoM](label_x) * 0.95
			else:
				label_y = GoM_tf1s[GoM](label_x) - 0.085
			GoM_labels[GoM] = TLatex(label_x, label_y, "#frac{{#Gamma}}{{M_{{Med}}}} #approx {}%".format(int(GoM * 100)))
			GoM_labels[GoM].SetTextSize(0.033)
			GoM_labels[GoM].SetTextColor(ROOT.kGray+1)
			GoM_labels[GoM].Draw("same")

		if draw_cms:
			if draw_cms == "":
				cms_text = "#bf{CMS}"
			else:
				cms_text = "#bf{{CMS}} #it{}".format(draw_cms)
			cms_label = TLatex(x_range[0], y_range[1] + 0.03, cms_text)
			cms_label.SetTextFont(42)
			cms_label.SetTextSize(0.04)

	def save(self, folder, exts=["pdf"]):
		for ext in exts:
			self._canvas.SaveAs("{}/{}.{}".format(folder, self._canvas.GetName(), ext))


if __name__ == "__main__":
	from argparse import ArgumentParser
	parser = ArgumentParser(description='Make g_q summary plot')
	parser.add_argument('--analyses', type=str, default="EXO16046_obs,EXO16046_exp,EXO16056_narrow_obs,EXO16056_narrow_exp,EXO16056_wide_obs,EXO16056_wide_exp,EXO17001_obs,EXO17001_exp,EXO16057_SR1_obs,EXO16057_SR1_exp,EXO16057_SR2_obs,EXO16057_SR2_exp", help="Analyses to plot (CADI lines, comma-separated)") 
	parser.add_argument('--logx', action='store_true', help='Log x')
	parser.add_argument('--logy', action='store_true', help='Log y')
	parser.add_argument('--goms', type=str, default="0.1,0.3", help='List of Gamma/M values to draw')
	cms_label_group = parser.add_mutually_exclusive_group(required=False)
	cms_label_group.add_argument('--cms', action='store_true', help="Draw CMS label")
	cms_label_group.add_argument('--cms_text', type=str, help="Draw CMS label with extra text")
	args = parser.parse_args()

	gq_plot = GQSummaryPlot()
	analysis_data = {}
	analyses = args.analyses.split(",")
	for analysis in analyses:
		analysis_data[analysis] = DijetData(analysis)
		analysis_data[analysis].load_data("data/{}.dat".format(analysis))
		gq_plot.add_data(analysis_data[analysis], analysis, legend_entries[analysis])
	gq_plot.set_width_curves((float(x) for x in args.goms.split(",")))
	if args.cms:
		cms_label_option = ""
	elif args.cms_text:
		cms_label_option = args.cms_text
	else:
		cms_label_option = False
	gq_plot.draw(logx=args.logx, logy=args.logy, draw_cms=cms_label_option)
	gq_plot.save("plots")
