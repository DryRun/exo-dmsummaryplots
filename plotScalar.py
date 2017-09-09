#########################################
#########################################
###                                   ###
### Draw awesome MET+X Summary plots  ###
###                                   ###
### (c) MET+X Combo                   ###
###                                   ###
#########################################
#########################################
import os
from ROOT import *
import ast
from Utilities import *
################
### Settings ###
################


#~ Mediator = raw_input('Choose Mediator [Scalar or Pseudo]: ')
#~ ObsOnly  = ast.literal_eval(raw_input('Obs only? [True or False]: '))

#################
### Analyses ####
#################
def do_plot(Mediator,ObsOnly):
	analyses = ["BSM",
				"monojet_obs",
				"monoz_obs",
				#"DMtt_obs",
				#"METbb_DMtt_obs",
				#"METbb_DMbb_obs"
				#,"METbb_DMhf_obs"
				"METHF_DMhf_obs",
				"Stop_obs"
				]
	
	if not ObsOnly: analyses=["BSM",
							"monojet_obs",   "monojet_exp",
							"monoz_obs",     "monoz_exp",
							#"DMtt_obs",      "DMtt_exp",
							#"METbb_DMbb_obs","METbb_DMbb_exp"
							#"METbb_DMtt_exp","METbb_DMtt_obs",
							"METHF_DMhf_obs","METHF_DMhf_exp",
							"Stop_obs","Stop_exp"
							]
	tgraph    = {}
	color     = {}
	text      = {}
	filepath  = {}
	linestyle = {}
	
	############# 
	### Files ###
	#############
	
	if Mediator == "Scalar":
		filepath["monojet_obs"]    = "Monojet/EXO-16-048/ScanMM/limit_scalar_1D.root"
 		filepath["monojet_exp"]    = "Monojet/EXO-16-048/ScanMM/limit_scalar_1D.root"
		filepath["monoz_obs"]      = "MonoZll/EXO-16-052/ScanMM/spin0/monoz_limit_S_obs.txt"
		filepath["monoz_exp"]      = "MonoZll/EXO-16-052/ScanMM/spin0/monoz_limit_S_exp.txt"
		
		filepath["DMtt_obs"]       = "DMtt/DMtt_Scalar_ICHEP2016_Mx_obs.txt"
		filepath["DMtt_exp"]       = "DMtt/DMtt_Scalar_ICHEP2016_Mx_exp.txt"
		filepath["METbb_DMtt_obs"] = "DMbb/2015/Limits_hfDMs.root"
		filepath["METbb_DMbb_obs"] = "DMbb/2015/Limits_hfDMs.root"
		filepath["METbb_DMhf_obs"] = "DMbb/2015/Limits_hfDMs.root"
		filepath["METHF_DMhf_obs"] = "DMHF/2015/HF_spin0_limits.root"
		filepath["METbb_DMtt_exp"] = "DMbb/2015/Limits_hfDMs.root"
		filepath["METbb_DMbb_exp"] = "DMbb/2015/Limits_hfDMs.root"
		filepath["METbb_DMhf_exp"] = "DMbb/2015/Limits_hfDMs.root"
		filepath["METHF_DMhf_exp"] = "DMHF/2015/HF_spin0_limits.root"
		filepath["Stop_obs"]	   = "Stop/SUS-17-001/S_1_obs.txt"
		filepath["Stop_exp"]	   = "Stop/SUS-17-001/S_1_exp.txt"
	if Mediator == "Pseudo":
		filepath["monojet_obs"]    = "Monojet/EXO-16-048/ScanMM/limit_pseudoscalar_1D.root"
		filepath["monojet_exp"]    = "Monojet/EXO-16-048/ScanMM/limit_pseudoscalar_1D.root"
		filepath["monoz_obs"]      = "MonoZll/EXO-16-052/ScanMM/spin0/monoz_limit_P_obs.txt"
		filepath["monoz_exp"]      = "MonoZll/EXO-16-052/ScanMM/spin0/monoz_limit_P_exp.txt"
		filepath["DMtt_obs"]       = "DMtt/DMtt_Pseudo_ICHEP2016_Mx_obs.txt"
		filepath["DMtt_exp"]       = "DMtt/DMtt_Pseudo_ICHEP2016_Mx_exp.txt"
		filepath["METbb_DMtt_obs"] = "DMbb/2015/Limits_hfDMps.root"
		filepath["METbb_DMbb_obs"] = "DMbb/2015/Limits_hfDMps.root"
		filepath["METbb_DMhf_obs"] = "DMbb/2015/Limits_hfDMps.root"
		filepath["METHF_DMhf_obs"] = "DMHF/2015/HF_spin0_limits.root"
		filepath["METbb_DMtt_exp"] = "DMbb/2015/Limits_hfDMps.root"
		filepath["METbb_DMbb_exp"] = "DMbb/2015/Limits_hfDMps.root"
		filepath["METbb_DMhf_exp"] = "DMbb/2015/Limits_hfDMps.root"
		filepath["METHF_DMhf_exp"] = "DMHF/2015/HF_spin0_limits.root"
		filepath["Stop_obs"]	   = "Stop/SUS-17-001/PS_1_obs.txt"
		filepath["Stop_exp"]	   = "Stop/SUS-17-001/PS_1_exp.txt"
	#######################
	### Plot linestyles ###
	#######################
	
	linestyle["BSM" ]           = 1
	#MET+jets

	for analysis in analyses:
		if("obs" in analysis.lower()):
			linestyle[analysis] = kSolid
		elif("exp" in analysis.lower()):
			linestyle[analysis] = kDashed

	###################
	### Plot colors ###
	###################
	
	color["BSM"]            = kBlack
	color["monojet_obs"]    = kRed+1
	color["monoz_obs"]      = kOrange-3
	color["DMtt_obs"]       = kGreen+2
	color["METbb_DMbb_obs"] = kGreen+1
	##
	color["METbb_DMhf_obs"] = kGreen+2
	color["METbb_DMtt_obs"] = kGreen+2
	color["METHF_DMhf_obs"] = kGreen+2

	color["Stop_obs"] = kAzure+2
	##
	color["monojet_exp"]    = color["monojet_obs"]
	color["monoz_exp"]    = color["monoz_obs"]
	color["DMtt_exp"]       = color["DMtt_obs"]
	color["METbb_DMbb_exp"] = color["METbb_DMbb_obs"]
	color["METbb_DMtt_exp"] = color["METbb_DMtt_obs"]
	color["METbb_DMhf_exp"] = color["METbb_DMhf_obs"]
	color["METHF_DMhf_exp"] = color["METHF_DMhf_obs"]
	color["Stop_exp"] = color["Stop_obs"]
	##################
	### Plot texts ###
	##################
	
	text["BSM"]            = "#sigma_{theory} (LHC DM WG)"
	text["monojet_obs"] = "#splitline{#bf{DM + j/V(qq)} (35.9 fb^{-1})}{[EXO-16-048]}"
	text["monoz_obs"]       = "#splitline{#bf{DM + Z(ll)} (35.9 fb^{-1})}{[EXO-16-052]}"
	#~ text["DMtt_obs"]       = "DM + tt (2.2 fb^{-1}) #it{EXO-16-005}"
	#~ text["METbb_DMbb_obs"] = "DM + bb (2.2 fb^{-1}) #it{B2G-15-007}"
	#~ text["METbb_DMtt_obs"] = "DM + tt (nj<4) [B2G-15-007]"
	#~ text["METbb_DMhf_obs"] = "MET+bb: DM+HF [B2G-15-007]"
	text["METHF_DMhf_obs"] = "#splitline{#bf{DM + tt/bb} (2.2 fb^{-1})}{[EXO-16-005]}"
	text["Stop_obs"] = "#splitline{#bf{DM + tt(ll)} (35.9 fb^{-1})}{[SUS-17-001]}"
	#exp
	#~ text["monojet_exp"]    = "exp.excl 95%CL"
	#~ text["monoz_exp"]    = "exp.excl 95%CL"
	#~ text["DMtt_exp"]       = "exp.excl 95%CL"
	#~ text["METbb_DMbb_exp"] = "exp.excl 95%CL"
	#~ text["METbb_DMtt_exp"] = "exp.excl 95%CL"
	#~ text["METbb_DMhf_exp"] = "exp.excl 95%CL"
	#~ text["METHF_DMhf_exp"] = "exp.excl 95%CL"
	
	text["gen_obs"] = "Observed exclusion 95% CL"
	text["gen_exp"] = "Expected exclusion 95% CL"
	
	####################
	### Get datfiles ###
	### Get graphs   ###
	####################
	
	f1 = TF1("f1","1",0,1000)
	
	for analysis in analyses: 
		if   analysis == "BSM"            : tgraph[analysis] = TGraph(f1)
		elif analysis == "monojet_obs"    : tgraph[analysis] = convert_spline_to_graph(TFile(filepath[analysis]).Get("observed_limit"),20,600)
 		elif analysis == "monojet_exp"    : tgraph[analysis] = convert_spline_to_graph(TFile(filepath[analysis]).Get("expected_limit"),20,600) 		
		elif analysis == "METbb_DMbb_obs" : tgraph[analysis] = TFile(filepath[analysis]).Get("bbObs0s")
		elif analysis == "METbb_DMtt_obs" : tgraph[analysis] = TFile(filepath[analysis]).Get("ttObs0s")
		elif analysis == "METbb_DMhf_obs" : tgraph[analysis] = TFile(filepath[analysis]).Get("hfObs0s")
		elif analysis == "METHF_DMhf_obs" : 
			if Mediator == "Scalar" :
				tgraph[analysis] = TFile(filepath[analysis]).Get("obs_hf_scalar")
			else :
				tgraph[analysis] = TFile(filepath[analysis]).Get("obs_hf_pseudoscalar")
		elif analysis == "METbb_DMbb_exp" : tgraph[analysis] = TFile(filepath[analysis]).Get("bbExp0s")
		elif analysis == "METbb_DMtt_exp" : tgraph[analysis] = TFile(filepath[analysis]).Get("ttExp0s")
		elif analysis == "METbb_DMhf_exp" : tgraph[analysis] = TFile(filepath[analysis]).Get("hfExp0s")
		elif analysis == "METHF_DMhf_exp" : 
			if Mediator == "Scalar" :
				tgraph[analysis] = TFile(filepath[analysis]).Get("exp_hf_scalar")
			else :
				tgraph[analysis] = TFile(filepath[analysis]).Get("exp_hf_pseudoscalar")
		else                              : tgraph[analysis] = TGraph(filepath[analysis])
	
	###################
	### Make Canvas ###
	### Set ranges  ###
	###################
	
	C=TCanvas("C","C",750,600)
	#C.cd(1).SetLogx()
	C.cd(1).SetLogy()
	
	tgraph["monojet_obs"].SetTitle("")
	tgraph["monojet_obs"].GetXaxis().SetTitle("Mediator mass M_{ Med} [GeV]")
	tgraph["monojet_obs"].GetYaxis().SetTitle("#sigma / #sigma_{theory}")
	tgraph["monojet_obs"].GetXaxis().SetTitleOffset(1.0)
	tgraph["monojet_obs"].GetYaxis().SetTitleOffset(1.0)
	tgraph["monojet_obs"].GetXaxis().SetTitleSize(0.045)
	tgraph["monojet_obs"].GetYaxis().SetTitleSize(0.045)
	tgraph["monojet_obs"].GetXaxis().SetRangeUser(10,    500)
	tgraph["monojet_obs"].GetYaxis().SetRangeUser(0.1, 1e3)
	tgraph["monojet_obs"].Draw()
	
	##################
	### Add legend ###
	##################
	
	if Mediator == "Scalar": 
		tex1=TLatex(130, 40000, "#bf{Scalar mediator}")
	if Mediator == "Pseudo": 
		tex1=TLatex(130, 40000, "#bf{Pseudoscalar mediator}")
	
	tex2=TLatex(130, 20000, "#bf{Dirac DM}, #it{m_{DM} = 1 GeV}")
	tex3=TLatex(130, 11000, "#it{g_{q} = 1, g_{DM} = 1}")
	
	tex1.SetTextFont(42)
	tex2.SetTextFont(42)
	tex3.SetTextFont(42)
	tex1.SetTextSize(0.03)
	tex2.SetTextSize(0.03)
	tex3.SetTextSize(0.03)
	tex1.Draw("same")
	tex2.Draw("same")
	tex3.Draw("same")
	
	#~ if Mediator == "Scalar": leg=C.BuildLegend(0.15,0.59,0.50,0.88)
	#~ if Mediator == "Pseudo": leg=C.BuildLegend(0.21,0.62,0.55,0.88)
	leg = TLegend(0.13,0.47,0.53,0.87)
	leg.SetBorderSize(0)
	leg.SetTextFont(42)
	leg.SetTextSize(0.025)
	leg.Clear()
	
	leg2=C.BuildLegend(0.10,0.905,0.90,0.955)
	leg2.SetBorderSize(0)
	leg2.SetTextFont(42)
	leg2.SetFillColor(0)
	leg2.Clear()
	leg2.SetHeader("#bf{CMS} #it{Preliminary}")
	
	#~ leg3=C.BuildLegend(0.44,0.905,1.54,0.955)
	#~ leg3.SetBorderSize(0)
	#~ leg3.SetTextFont(42)
	#~ leg3.SetFillColor(0)
	#~ leg3.Clear()

	texts = []
	medname = Mediator if Mediator=="Scalar" else Mediator+"scalar"
	texts.append(add_text(0.55,0.9,0.65,0.85,["#bf{{{MED} Mediator}}".format(MED=medname),"Dirac DM","g_{q} = 1.0", "g_{DM} = 1.0", "m_{DM} = 1 GeV"],alignment=12))
	texts.append(add_text(0.7,0.85,0.86,1.0,"EPS 2017"))
	#~ leg3.SetHeader("2.2 fb^{-1} & 35.9 fb^{-1} (13 TeV)")
	
	############
	### Draw ###
	############
	
	for analysis in analyses:
		tgraph[analysis].SetLineColor(color[analysis])
		if analysis == "BSM" or "exp" in analysis:
			tgraph[analysis].SetLineWidth(3)
			tgraph[analysis].SetFillStyle(1001)
			tgraph[analysis].SetFillColor(kWhite)
		else:
			tgraph[analysis].SetFillColor(color[analysis])
			tgraph[analysis].SetFillStyle(3005)
			tgraph[analysis].SetLineWidth( 202)
		tgraph[analysis].SetLineStyle(linestyle[analysis])
	
	dummy1 = TGraph("dummy_100.dat")
	dummy2 = TGraph("dummy_600.dat")
	
	tgraph["gen_obs"]=dummy1
	tgraph["gen_exp"]=dummy2
	
	for analysis in ["gen_obs","gen_exp"]:
			tgraph[analysis].SetLineWidth( 2)
			tgraph[analysis].SetFillStyle(3005)
			tgraph[analysis].SetLineColor(kBlack)
			tgraph[analysis].SetMarkerSize(0.1)
			tgraph[analysis].SetMarkerColor(kBlack)
			tgraph[analysis].SetFillColor(kBlack)
			tgraph[analysis].SetLineWidth( 403)
		
	#~ tgraph["gen_exp"].SetFillColor(kWhite)
	tgraph["gen_exp"].SetLineStyle(kDashed)
		
	tgraph["fermion"] = tgraph["BSM"].Clone()
	tgraph["fermion"].SetLineColor(kWhite)
	text["fermion"] = "fermion only #it{EXO-16-037}"

	leg.AddEntry(tgraph["BSM"],text["BSM"],"FL")
	for analysis in ["gen_obs","gen_exp"]:
		leg.AddEntry(tgraph[analysis],text[analysis],"L")
	for analysis in analyses:
		if not "exp" in analysis and not "BSM" in analysis:
			leg.AddEntry(tgraph[analysis],text[analysis],"L")
		
	
	leg.Draw()
	#~ leg2.Draw()
	#~ leg3.Draw()
	C.Update()
	for analysis in analyses:
		tgraph[analysis].Draw("same")
	C.Update()
	
	############
	### Save ###
	############
	gPad.SetTicky()
	gPad.SetTickx()

	if( not os.path.exists("./output") ): os.makedirs("./output")
	if ObsOnly: C.SaveAs("./output/"+Mediator+"_METX_Summary_obsonly.pdf")
	else      : C.SaveAs("./output/"+Mediator+"_METX_Summary_obsnexp.pdf")
	C.Close()

do_plot("Scalar",0)
do_plot("Pseudo",0)
