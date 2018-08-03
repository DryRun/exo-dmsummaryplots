# Plot the reference cross sections used for g'_q conversions
import os
import sys
sys.path.append("./python/")
from gq_summary_plot import GQSummaryPlot, seaborn_colors
from dijet_data import DijetData
import ROOT
from ROOT import TLine, TGraph, TLegend, TCanvas, TH1F

# Read reference cross sections
ref_xs_files = {
	8:"data/reference/ZPrime_8TeV_gq0p25.dat",
	13:"data/reference/ZPrime_13TeV_gq0p25.dat",
}

xs_graphs = {}
max_xs = -1e20
min_xs = 1e20
for sqrts in [8, 13]:
	with open(ref_xs_files[sqrts], 'r') as f:
		this_xss = {}
		for line in f:
			if line[0] == "#":
				continue
			line_contents = line.split()
			xs = float(line_contents[1])
			this_xss[float(line_contents[0])] = xs
			if xs > max_xs:
				max_xs = xs
			if xs < min_xs:
				min_xs = xs
		xs_graphs[sqrts] = TGraph(len(this_xss))
		for i, mass in enumerate(sorted(this_xss.keys())):
			xs_graphs[sqrts].SetPoint(i, mass, this_xss[mass])

xs_graphs[8].SetMarkerStyle(20)
xs_graphs[8].SetMarkerColor(seaborn_colors.get_root_color("Oranges_d", 1))
xs_graphs[8].SetLineColor(seaborn_colors.get_root_color("Oranges_d", 1))
xs_graphs[13].SetMarkerStyle(22)
xs_graphs[13].SetMarkerColor(seaborn_colors.get_root_color("Blues_d", 3))
xs_graphs[13].SetLineColor(seaborn_colors.get_root_color("Blues_d", 3))

c = TCanvas("c_reference_xses", "Reference #sigma", 800, 600)
c.SetLogy()
frame = TH1F("frame", "frame", 100, 0., 1500.)
frame.GetXaxis().SetTitle("m_{Z'} [GeV]")
frame.GetYaxis().SetTitle("#sigma(pp#rightarrow Z') [pb]")
frame.SetMinimum(min_xs / 10.)
frame.SetMaximum(max_xs * 10.)
frame.Draw()
xs_graphs[8].Draw("cp")
xs_graphs[13].Draw("cp")
l = TLegend(0.7, 0.7, 0.88, 0.88)
l.SetFillStyle(0)
l.SetBorderSize(0)
l.AddEntry(xs_graphs[8], "#sqrt{s}=8 TeV", "pl")
l.AddEntry(xs_graphs[13], "#sqrt{s}=13 TeV", "pl")
l.Draw()
c.SaveAs("plots/{}.pdf".format(c.GetName()))