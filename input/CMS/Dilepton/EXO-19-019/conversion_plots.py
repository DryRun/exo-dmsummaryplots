import os
import sys
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(False)
ROOT.gStyle.SetOptTitle(False)

for scenario in ["V2", "A2"]:
	f = ROOT.TFile("ScanMM/contours_dilepton_{}.root".format(scenario), "READ")

	for what in ["obs", "exp_med"]:
		c_input = ROOT.TCanvas("c_input_{}_{}".format(scenario, what), "c_input_{}_{}".format(scenario, what), 1000, 800)
		c_input.SetLogz()
		c_input.SetLeftMargin(0.15)
		tg_input = f.Get("{}_inputlimits".format(what))
		tg_input.SetNpx(500)
		tg_input.SetNpy(500)
		#h_input = tg_input.GetHistogram()
		tg_input.GetHistogram().GetXaxis().SetTitle("m_{Z'} [GeV]")
		tg_input.GetHistogram().GetXaxis().SetTitleOffset(2.0)
		tg_input.GetHistogram().GetYaxis().SetTitle("#Gamma_{Z'}/m_{Z'}")
		tg_input.GetHistogram().GetYaxis().SetTitleOffset(2.0)
		if what == "obs":
			tg_input.GetHistogram().GetZaxis().SetTitle("#\sigma_{95}^{(obs} [pb]")
			tg_input.GetHistogram().GetZaxis().SetTitleOffset(2.0)
		elif what == "exp_med":
			tg_input.GetHistogram().GetZaxis().SetTitle("#\sigma_{95}^{(exp} [pb]")
			tg_input.GetHistogram().GetZaxis().SetTitleOffset(2.0)
		tg_input.Draw("TRI1")
		c_input.SetTheta(22.85)
		c_input.SetPhi(-26.76)
		c_input.SaveAs("figures/{}.pdf".format(c_input.GetName()))
		c_input.SaveAs("figures/{}.png".format(c_input.GetName()))		

		c_mdmlimits = ROOT.TCanvas("c_mdmlimits_{}_{}".format(scenario, what), "c_mdmlimits_{}_{}".format(scenario, what), 1000, 800)
		c_mdmlimits.SetLogz()
		c_mdmlimits.SetLeftMargin(0.15)
		tg_mdmlimits = f.Get("{}_mdmlimits".format(what))
		tg_mdmlimits.SetNpx(500)
		tg_mdmlimits.SetNpy(500)
		#h_mdmlimits = tg_mdmlimits.GetHistogram()
		tg_mdmlimits.GetHistogram().GetXaxis().SetTitle("m_{Z'} [GeV]")
		tg_mdmlimits.GetHistogram().GetXaxis().SetTitleOffset(2.0)
		tg_mdmlimits.GetHistogram().GetYaxis().SetTitle("m_{DM} [GeV]")
		tg_mdmlimits.GetHistogram().GetYaxis().SetTitleOffset(2.0)
		if what == "obs":
			tg_mdmlimits.GetHistogram().GetZaxis().SetTitle("#\sigma_{95}^{(obs)} [pb]")
			tg_mdmlimits.GetHistogram().GetZaxis().SetTitleOffset(2.0)
		elif what == "exp_med":
			tg_mdmlimits.GetHistogram().GetZaxis().SetTitle("#\sigma_{95}^{(exp)} [pb]")
			tg_mdmlimits.GetHistogram().GetZaxis().SetTitleOffset(2.0)
		tg_mdmlimits.Draw("SURF1")
		c_mdmlimits.SetTheta(22.85)
		c_mdmlimits.SetPhi(-26.76)
		c_mdmlimits.SaveAs("figures/{}.pdf".format(c_mdmlimits.GetName()))
		c_mdmlimits.SaveAs("figures/{}.png".format(c_mdmlimits.GetName()))		

		c_xslimit = ROOT.TCanvas("c_xslimit_{}_{}".format(scenario, what), "c_xslimit_{}_{}".format(scenario, what), 1200, 800)
		c_xslimit.SetLogz()
		c_xslimit.SetRightMargin(0.15)
		tg_xslimit = f.Get("{}_xslimit".format(what))
		tg_xslimit.SetNpx(500)
		tg_xslimit.SetNpy(500)
		h_xslimit = tg_xslimit.GetHistogram()
		h_xslimit.GetXaxis().SetTitle("m_{Z'} [GeV]")
		h_xslimit.GetYaxis().SetTitle("m_{DM} [GeV]")
		if what == "obs":
			h_xslimit.GetZaxis().SetTitle("#\sigma_{95}^{(obs)} [pb]")
		elif what == "exp_med":
			h_xslimit.GetZaxis().SetTitle("#\sigma_{95}^{(exp)} [pb]")
		h_xslimit.Draw("colz")
		c_xslimit.SaveAs("figures/{}.pdf".format(c_xslimit.GetName()))
		c_xslimit.SaveAs("figures/{}.png".format(c_xslimit.GetName()))		

	c_xsref = ROOT.TCanvas("c_xsref_{}".format(scenario), "c_xsref_{}".format(scenario), 1200, 800)
	c_xsref.SetLogz()
	c_xsref.SetRightMargin(0.15)
	tg_xsref = f.Get("xsref")
	tg_xsref.SetNpx(500)
	tg_xsref.SetNpy(500)
	h_xsref = tg_xsref.GetHistogram()
	h_xsref.GetXaxis().SetTitle("m_{Z'} [GeV]")
	h_xsref.GetYaxis().SetTitle("m_{DM} [GeV]")
	h_xsref.GetZaxis().SetTitle("Reference #sigma(Z') (pb)")
	h_xsref.Draw("colz")
	c_xsref.SaveAs("figures/{}.pdf".format(c_xsref.GetName()))
	c_xsref.SaveAs("figures/{}.png".format(c_xsref.GetName()))	

	for what in ["obs", "exp_med"]:
		c_dxs = ROOT.TCanvas("c_dxs_{}_{}".format(scenario, what), "c_dxs_{}_{}".format(scenario, what), 1200, 800)
		c_dxs.SetRightMargin(0.15)
		tg_dxs = f.Get("{}_dxs".format(what))
		tg_dxs.SetNpx(500)
		tg_dxs.SetNpy(500)
		h_dxs = tg_dxs.GetHistogram()
		h_dxs.GetXaxis().SetTitle("m_{Z'} [GeV]")
		h_dxs.GetYaxis().SetTitle("m_{DM} [GeV]")
		if what == "obs":
			h_dxs.GetZaxis().SetTitle("log_{10}(#sigma_{ref}) - log_{10}(#sigma_{95}^{(obs)})")
		else:
			h_dxs.GetZaxis().SetTitle("log_{10}(#sigma_{ref}) - log_{10}(#sigma_{95}^{(exp)})")
		h_dxs.Draw("colz")
		c_dxs.SaveAs("figures/{}.pdf".format(c_dxs.GetName()))
		c_dxs.SaveAs("figures/{}.png".format(c_dxs.GetName()))		

