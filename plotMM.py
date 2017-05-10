#########################################
#########################################
###                                   ###
### Draw awesome MET+X Summary plots  ###
###                                   ###
### (c) MET+X Combo                   ###
###                                   ###
#########################################
#########################################

from ROOT import *
import ast
import os
from Utilities import *
#################################
### Parameters to be modified ###
#################################

Dijet    = False
Dilepton = False

# Mediator  = raw_input('Choose mediator [Vector or Axial]: ')
# Scenario  = raw_input('Choose Scenario according to 1703.05703 [1 or 2 or dijetchi or Monotop]: ') #1 for Default MET+X, 2 for dil, gq=gDM=1 for dijetchi
# #METXonly  = ast.literal_eval(raw_input('MET+X only? [True or False]: '))
# METX        = ast.literal_eval(raw_input('MET+X? [True or False]: '))
# Resonances  = ast.literal_eval(raw_input('Resonances? [True or False]: '))
# if Resonances :
#     Dijet     = ast.literal_eval(raw_input('Dijet? [True or False]: '))
#     Dilepton  = ast.literal_eval(raw_input('Dilepton? [True or False]: '))

# if Dilepton : gl = ast.literal_eval(raw_input('gl? [0.10 or 0.025 or 0.01]: '))

# logx      = ast.literal_eval(raw_input('Log x? '))

#A1/V1
# Mediator = "Vector"
# Scenario = "1"
# METX = 1
# Resonances = 1
# Dijet = 1
# Dilepton = 0
# logx = 0

#A1/V1 just MET+X
Mediator = "Vector"
Scenario = "1"
METX = 1
Resonances = 1
Dijet = 1
Dilepton = 0
logx = 0

#A2
# Mediator = "Axial"
# #Mediator = "Vector"
# Scenario = "2"
# METX = 0
# Resonances = 1
# Dijet = 0
# Dilepton = 1

# logx = 0

#dijetchi
# Mediator = "Vector"
# Scenario = "dijetchi"
# METX = 0
# Resonances = 1
# Dijet = 1
# Dilepton = 0
# logx = 0


#Monotop
# Mediator = "Vector"
# Scenario = "Monotop"
# METX = 1
# Resonances = 0
# logx = 0


CL = "95"

#################
### Analyses ####
#################

#####DECIDE WHERE TO PUT MONOTOP and DIJETCHI DIJET_EXP

#if Mediator == "Axial": metx = ["monojet","monophoton","monoz"]
#else                  : metx = ["monojet","monophoton","monoz","monoHgg"]
def make_plot(Mediator, Scenario, METX, Resonances, Dijet, Dilepton, logx, CL):

    if(Scenario == "1" and Dilepton):
        print "Error: No dilepton curves for scenario 1. Run with Dilepton = False"
        print "Exiting."
        return 1
    output = "./output"
    if(not os.path.exists(output)): os.makedirs(output)
    texts = []

    if   Scenario == "1" :
        if Mediator == "Axial": metx = ["monojet","monophoton","monoz"]
        else                  : metx = ["monojet","monophoton","monoz"]
    #    else                  : metx = ["monojet","monophoton","monoz","monoHgg"]
    elif Scenario == "2" :
        #empty for now
        if Mediator == "Axial": metx = []
        else                  : metx = []
    elif Scenario == "dijetchi" :
        #empty for now
        if Mediator == "Axial": metx = []
        else                  : metx = []
    elif Scenario == "Monotop" :
        if Mediator == "Axial": print "Can't have axial monotop"; exit
        else                  : metx = ["monotop"]


    #if   METXonly  : analyses = ["relic"]+metx
    #if Mediator=="Vector" and METXonly : metx+=["monotop"]
    #if Dilepton  : analyses = ["relic","dilepton","dijet","trijet"]+metx
    #elif DijetOnly : analyses = ["relic","dijet_2016","dijet_2016_exp"]
    #else           : analyses = ["relic","dijet","trijet"]+metx



    analyses = ["relic"]
    if METX: analyses += metx
    if Dilepton  : analyses += ["dilepton"]
    if Dijet :
        if Scenario == "dijetchi" : analyses += ["dijetchi"]
        else : analyses += ["dijet","trijet"]



    tgraph    = {}
    color     = {}
    text      = {}
    filepath  = {}
    linestyle = {}

    #############
    ### Files ###
    #############

    if Mediator == "Vector":
        filepath["relic"]          = "Relic/madDMv2_0_6/relicContour_V_g25.root"
        #95
        filepath["trijet"]         = "Trijet/ScanMM/MMedMDM_v.root"
        filepath["monotop"]        = "Monotop/ScanMM/fcnc2d_obs_vector.root"
    elif Mediator == "Axial":
        filepath["relic"]          = "Relic/madDMv2_0_6/relicContour_A_g25.root"

        #95
        if CL=="95":
            filepath["dijet_2016"]     = "Dijet/ScanMM/Dijet_MM_A_Dijetpaper2016_exp.root"
            filepath["dijet_2016_exp"] = "Dijet/ScanMM/Dijet_MM_A_Dijetpaper2016_exp.root"
        elif CL=="90":
            filepath["dijet_2016"]          = "Dijet/ScanMM/Dijet_MM_A_Dijetpaper2016_obs_90.root"
            filepath["dijet_2016_exp"]          = "Dijet/ScanMM/Dijet_MM_A_Dijetpaper2016_obs_90.root"
        filepath["trijet"]         = "Trijet/ScanMM/MMedMDM_av.root"

    ###################
    ### Plot colors ###
    ###################

    ### Planck
    linestyle["relic"]          = kDotted#was dotted
    ### Met-less
    linestyle["dijet"]          = kSolid
    linestyle["dijetchi"]          = kSolid
    linestyle["dijet_2016"]     = kSolid
    linestyle["dijet_2016_exp"] = kDashed
    linestyle["dilepton"]       = kSolid
    linestyle["trijet"]         = kSolid
    ### MET+X
    linestyle["monophoton"]     = kSolid
    linestyle["monoz"]          = kSolid
    linestyle["monoHgg"]          = kSolid
    linestyle["monotop"]        = kDashed
    ### dummies dashed
    linestyle["monojet"]        = kSolid

    ### Planck
    color["relic"]          = kGray+2
    ### Met-less
    color["dijet"]          = kAzure
    color["dijetchi"]          = kAzure
    color["dilepton"]       = kGreen+3
    color["dijet_2016"]     = kAzure
    color["dijet_2016_exp"] = kAzure+1
    color["trijet"]         = kAzure+1
    color["chi"]            = kBlue
    ### MET+X
    color["monojet"]        = kRed+1#kRed+1
    color["monophoton"]     = kOrange+10#kRed+2
    color["monoz"]          = kOrange-3#kRed+3
    color["monoHgg"]          = kMagenta-7#kRed+3
    color["monotop"]        = kViolet+1

    ##################
    ### Plot texts ###
    ##################

    #if not METXonly:
    text["relic"]          = "\Omega_{c} h^{2} \geq 0.12"
    text["dijet"]      = "CMS Dijet [EXO-16-056]"
    text["dijetchi"]      = "CMS Dijet [EXO-16-046]"
    text["dilepton"]       = "Z' #rightarrow ll"
    text["dijet_2016"]     = "Observed"
    text["dijet_2016_exp"] = "Expected"
    text["trijet"]         = "#splitline{Boosted dijet}{#it{[EXO-17-001]}}"
    text["chi"]            = "chi obs. (exp.excl.)"
    text["monojet"]        = "#splitline{DM + j/V_{qq}}{#it{[EXO-16-048]}}"
    text["monoz"]          = "#splitline{DM + Z_{ll}}{#it{[EXO-16-052]}}"
    text["monoHgg"]          = "#splitline{DM + H_{#gamma #gamma}}{#it{[EXO-16-054]}}"
    text["monophoton"]     = "#splitline{DM + #gamma}{#it{[EXO-16-039]}}"
    text["monotop"]        = "#splitline{DM + t (100% FC)}{#it{[EXO-16-051]}}"
    # else:
    #     text["relic"]      = "\Omega_{c} h^{2} \geq 0.12"
    # #    text["dijet"]      = "Dijet #it{[EXO-16-032]}+ #it{[arXiv:1604.08907]}"
    #     text["dijet"]      = "CMS Dijet [EXO-16-056]"
    #     text["dijetchi"]      = "CMS Dijet [EXO-16-046]"
    #     text["trijet"]     = "Boosted dijet #it{[EXO-17-001]}}"
    #     text["chi"]        = "chi obs. (exp.excl.)"
    #     text["monojet"]    = "DM + j/V_{qq} #it{[EXO-16-048]}"
    #     text["monoz"]      = "DM + Z_{ll} #it{[EXO-16-038]}"
    #     text["monoHgg"]          = "#splitline{DM + H_{#gamma #gamma}}{#it{[EXO-16-054]}}"
    #     text["monophoton"] = "DM + #gamma #it{[EXO-16-039]}"
    #     text["monotop"]    = "DM + t (100% FC) #it{[EXO-16-051]}"

    ####################
    ### Get graphs   ###
    ####################

    #~ for analysis in analyses:
        #~ if analysis == "relic":
            #~ mylist = TFile(filepath["relic"]).Get("mytlist")
            #~ print "==> Relic list length = ",mylist.GetSize()
            #~ tgraph["relic"] = mylist.At(0)
        #~ elif analysis == "dijet"          : tgraph["dijet"]          = TFile(filepath[analysis]).Get("Obs_90")
        #~ elif analysis == "dijetchi"          : tgraph["dijetchi"]          = TFile(filepath[analysis]).Get("obs_MvsM")
        #~ #dijet paper
        #~ elif analysis == "dijet_2016"     : tgraph["dijet_2016"]     = TFile(filepath[analysis]).Get("obs_025")
        #~ elif analysis == "dijet_2016_exp" : tgraph["dijet_2016_exp"] = TFile(filepath[analysis]).Get("exp_025")
        #~ elif analysis == "trijet"         : tgraph["trijet"]         = TFile(filepath[analysis]).Get("obs_025")
        #~ #
    #~ #    elif analysis == "dilepton"       : tgraph["dilepton"]       = TFile(filepath[analysis]).Get("obs_025")
        #~ elif analysis == "dilepton" :
            #~ tgraph["dilepton"]       = TFile(filepath[analysis]).Get("obs")
        #~ elif analysis == "monojet"        :
                #~ tgraph["monojet"]        = TFile(filepath[analysis]).Get("contour_observed")
        #~ elif analysis == "monophoton"     : tgraph["monophoton"]     = TFile(filepath[analysis]).Get("monophoton_obs")
        #~ elif analysis == "monoHgg"        : tgraph["monoHgg"]     = TFile(filepath[analysis]).Get("observed_baryonic_MonoHgg")
        #~ elif analysis == "monotop"        : tgraph["monotop"]        = TFile(filepath[analysis]).Get("observed")
        #~ else                              : tgraph[analysis]         = TGraph(filepath[analysis])

    #~ try:
        #~ tgraph["dilepton"] = rescale_graph_axis(tgraph["dilepton"],1e3,1e3)
    #~ except KeyError:
        #~ pass

    all_graphs = read_graphs()
    if(  Mediator == "Axial"  and Scenario == "1"): scenario_tag = "A1"
    elif(Mediator == "Axial"  and Scenario == "2"): scenario_tag = "A2"
    elif(Mediator == "Vector" and Scenario == "1"): scenario_tag = "V1"
    elif(Mediator == "Vector" and Scenario == "2"): scenario_tag = "V2"

    #~ tgraphs = {}
    for a in analyses:
        print a
        tgraph[a] = all_graphs[a][scenario_tag]["obs"]

    
    ###################
    ### Recast ###
    ###################




    ###################
    ### Make Canvas ###
    ### Set ranges  ###
    ###################

    C=TCanvas("C","C",1000,600)
    C.cd(1)

    C.cd(1).SetTickx()
    C.cd(1).SetTicky()

    if logx       : frame = C.cd(1).DrawFrame(90,0,3700, 1450)
    #elif METXonly : frame = C.cd(1).DrawFrame(0,0,2000, 780)
    #elif Dilepton : frame = C.cd(1).DrawFrame(0,0,5000,2000)
    #else          : frame = C.cd(1).DrawFrame(0,0,3700,1450)
    else :
        if Dilepton :
            frame = C.cd(1).DrawFrame(0,0,4200,2000)
        elif Scenario=="dijetchi":
            frame = C.cd(1).DrawFrame(0,0,5500,2000)
        elif Scenario=="1" and Resonances==0 and Dijet==0 and Dilepton==0 :
            frame = C.cd(1).DrawFrame(0,0,2000,1000)
        else :
            frame = C.cd(1).DrawFrame(0,0,5200,2000)

    if logx : C.cd(1).SetLogx()

    frame.SetXTitle("Mediator mass [GeV]")
    frame.SetYTitle("m_{DM} [GeV]")
    #frame.GetXaxis().SetLabelSize(0.05)
    #frame.GetYaxis().SetLabelSize(0.05)
    frame.GetXaxis().SetTitleSize(0.052)#was 45
    frame.GetYaxis().SetTitleSize(0.052)#was 45
    frame.GetXaxis().SetTitleOffset(0.85)
    frame.GetYaxis().SetTitleOffset(0.85)

    ##############
    ### LEGEND ###
    ##############

    if   logx     : leg=C.BuildLegend(0.31,0.25,0.51,0.75)
    # elif METXonly : leg=C.BuildLegend(0.15,0.55,0.45,0.88)
    # elif Dilepton : leg=C.BuildLegend(0.68,0.12,0.87,0.45)
    # elif DijetOnly: leg=C.BuildLegend(0.69,0.12,0.91,0.37)
    # else:           leg=C.BuildLegend(0.67,0.12,0.89,0.57)
    else           :
        if Dilepton :
            leg=C.BuildLegend(0.68,0.12,0.87,0.25)
        elif Scenario=="dijetchi" :
            leg=C.BuildLegend(0.60,0.12,0.81,0.45)
        elif Scenario=="1" and Resonances==0 and Dijet==0 and Dilepton==0 :
            leg=C.BuildLegend(0.60,0.12,0.81,0.45)
        else :
            leg=C.BuildLegend(0.68,0.12,0.87,0.45)

    leg.SetBorderSize(0)
    leg.SetTextFont(42)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.Clear()

    #if DijetOnly: leg.SetHeader("#bf{Dijet "+CL+"% CL}")
    #else        : leg.SetHeader("#bf{Observed exclusion 95% CL}")
    leg.SetHeader("#bf{Observed exclusion 95% CL}")

    ####################
    ### Add diagonal ###
    ####################

    f1 = TF1("f1","x/2.",0,4000)
    g1 = TGraph(f1)
    g1.SetLineColor(color["relic"]-1)
    g1.SetLineStyle(kDashed)

    #if Dilepton:
    g1.Draw("same")
    legd=TLatex(1300,680,"M_{Med} = 2 x m_{DM}")
    legd.SetTextAngle(35)
    legd.SetTextFont(42)
    legd.SetTextSize(0.030)
    legd.SetTextColor(color["relic"])
    legd.Draw("same")
    # elif DijetOnly:
    #     g1.Draw("same")
    #     legd=TLatex(1300,680,"M_{Med} = 2 x m_{DM}")
    #     legd.SetTextAngle(37)
    #     legd.SetTextFont(42)
    #     legd.SetTextSize(0.040)
    #     legd.SetTextColor(color["relic"])
    #     legd.Draw("same")
    # elif not METXonly:
    #     g1.Draw("same")
    #     legd=TLatex(1600,740,"M_{Med} = 2 x m_{DM}")
    #     legd.SetTextAngle(45)
    #     legd.SetTextFont(42)
    #     legd.SetTextSize(0.040)
    #     legd.SetTextColor(color["relic"])
    #     legd.Draw("same")

    ##################
    ### Relic text ###
    ##################

    #if Mediator=="Vector" and Dilepton:
    if Mediator=="Vector" :
        legw=TLatex(2700,450,"#Omega_{c} h^{2} #geq 0.12")
        legw.SetTextAngle(25)
        legw.SetTextSize(0.030)
    # elif Mediator=="Vector" and DijetOnly:
    #     legw=TLatex(2940,580,"#Omega_{c} h^{2} #geq 0.12")
    #     legw.SetTextAngle(30)
    #     legw.SetTextSize(0.04)
    # elif Mediator=="Vector" and not METXonly:
    #     legw=TLatex(3950,900,"#Omega_{c} h^{2} #geq 0.12")
    #     legw.SetTextAngle(40)
    #     legw.SetTextSize(0.03)
    # elif Mediator=="Axial" and DijetOnly:
    #     legw  = TLatex(1670,1070,"#Omega_{c} h^{2} #geq 0.12")
    #     legw.SetTextAngle(34)
    #     legw2 = TLatex(2800,1070,"#Omega_{c} h^{2} #geq 0.12")
    #     legw2.SetTextFont(42)
    #     legw2.SetTextColor(color["relic"])
    #     legw2.SetTextAngle(34)
    #     legw.SetTextSize(0.04)
    #     legw2.SetTextSize(0.04)
    #     legw2.Draw("same")
    #elif Mediator=="Axial" and not METXonly:
    elif Mediator=="Axial" :
        legw  = TLatex(1720,1150,"#Omega_{c} h^{2} #geq 0.12")
        legw.SetTextAngle(40)
        legw2 = TLatex(3020,1150,"#Omega_{c} h^{2} #geq 0.12")
        legw2.SetTextFont(42)
        legw2.SetTextColor(color["relic"])
        legw2.SetTextAngle(40)
        legw2.SetTextSize(0.02)
        legw.SetTextSize(0.03)
        texts.append(legw2)
    # elif Mediator=="Vector" and METXonly:
    #     legw=TLatex(1600,160,"#Omega_{c} h^{2} #geq 0.12")
    #     legw.SetTextAngle(16)
    #     legw.SetTextSize(0.03)
    # elif Mediator=="Axial" and METXonly:
    #     legw=TLatex(1750,600,"#Omega_{c} h^{2} #geq 0.12")
    #     legw.SetTextSize(0.03)
    #     legw.SetTextAngle(35)
    legw.SetTextFont(42)
    legw.SetTextColor(color["relic"])
    texts.append(legw)

    ##################
    ### Model text ###
    ##################

    if logx:
        leg1=TLatex(250,1300,"#splitline{#bf{"+Mediator+" mediator}}{#bf{Dirac DM}}")
        leg1.SetTextFont(42)
        leg1.SetTextSize(0.030)
        if Scenario == "1" :
            leg4=TLatex(250,1200,"#it{g_{q} = 0.25, g_{DM} = 1}")
        elif Scenario == "2" :
            if Mediator=="Axial" :
                leg4=TLatex(250,1200,"#it{g_{q} = 0.1, g_{DM} = 1, g_{l} = 0.01}")
            if Mediator=="Vector" :
                leg4=TLatex(250,1200,"#it{g_{q} = 0.1, g_{DM} = 1, g_{l} = 0.1}")
        leg4.SetTextFont(42)
        leg4.SetTextSize(0.030)
        texts.append(leg1)
        texts.append(leg4)


    #elif Mediator=="Vector" and Dilepton:
    elif Mediator=="Vector" :
        tmp_texts = []
        if Scenario == "dijetchi" :
            tmp_texts.append(TLatex(3700,1550,"#splitline{#bf{Vector mediator}}{#bf{& Dirac DM}}"))
            tmp_texts.append(TLatex(3700,1350,"#splitline{#it{g_{DM} = 1.0}}{#it{g_{q} = 1.0}}"))
        elif Scenario == "2" :
            tmp_texts.append(TLatex(3400,1550,"#splitline{#bf{Vector mediator}}{#bf{& Dirac DM}}"))
            tmp_texts.append(TLatex(3400,1350,"#splitline{#it{g_{q} = 0.1, g_{DM} = 1}}{#it{g_{l} = 0.1}}") )
        else :
            if Scenario=="1" and Resonances==0 and Dijet==0 and Dilepton==0 :
                tmp_texts.append(TLatex(200,900,"#splitline{#bf{Vector mediator}}{#bf{& Dirac DM}}"))
                tmp_texts.append(TLatex(200,800,"#splitline{#it{g_{DM} = 1.0}}{#it{g_{q} = 0.25}}"))
            else :

                tmp_texts.append(TLatex(3700,1550,"#splitline{#bf{Vector mediator}}{#bf{& Dirac DM}}"))
                tmp_texts.append(TLatex(3700,1350,"#splitline{#it{g_{DM} = 1.0}}{#it{g_{q} = 0.25}}"))

        for t in tmp_texts:
            t.SetTextFont(42)
            t.SetTextSize(0.030)
        texts.extend(tmp_texts)
    # elif Mediator=="Vector" and DijetOnly:
    #     leg1=TLatex(2750,1120,"#splitline{#bf{Vector mediator}}{#bf{&}}")
    #     leg5=TLatex(2750,1000,"#bf{Dirac DM}")
    #     leg4=TLatex(2750, 850,"#splitline{#it{g_{q} = 0.25}}{#it{g_{DM} = 1.0}}")
    #     leg1.SetTextFont(42)
    #     leg4.SetTextFont(42)
    #     leg5.SetTextFont(42)
    #     leg1.SetTextSize(0.040)
    #     leg4.SetTextSize(0.040)
    #     leg5.SetTextSize(0.040)
    #     leg4.Draw("same")
    #     leg5.Draw("same")
    # elif Mediator=="Axial" and DijetOnly:
    #     leg1=TLatex(2750, 920,"#splitline{#bf{"+Mediator+"-vector}}{#bf{mediator &}}")
    #     leg5=TLatex(2750, 800,"#bf{Dirac DM}")
    #     leg4=TLatex(2750, 650,"#splitline{#it{g_{q} = 0.25}}{#it{g_{DM} = 1.0}}")
    #     leg1.SetTextFont(42)
    #     leg4.SetTextFont(42)
    #     leg5.SetTextFont(42)
    #     leg1.SetTextSize(0.040)
    #     leg4.SetTextSize(0.040)
    #     leg5.SetTextSize(0.040)
    #     leg4.Draw("same")
    #     leg5.Draw("same")
    # elif Mediator=="Vector" and not METXonly:
    #     leg1=TLatex(2770,1100,"#splitline{#bf{"+Mediator+" mediator, Dirac DM}}{        #it{g_{q} = 0.25, g_{DM} = 1}}")
    #     leg1.SetTextFont(42)
    #     leg1.SetTextSize(0.030)
    #elif Mediator=="Axial" and not METXonly:
    elif Mediator=="Axial" :
        tmp_texts = []
        if Scenario == "1" :
            if Scenario=="1" and Resonances==0 and Dijet==0 and Dilepton==0 :
                tmp_texts.append(TLatex(200,900,"#splitline{#bf{Axial-vector mediator}}{#bf{& Dirac DM}}"))
                tmp_texts.append(TLatex(200,800,"#splitline{#it{g_{DM} = 1.0}}{#it{g_{q} = 0.25}}"))
            else :
                tmp_texts.append(TLatex(3200,1000,"#splitline{#bf{Axial-vector mediator, Dirac DM}}{#it{g_{q} = 0.25, g_{DM} = 1.0}}"))
        elif Scenario == "2" :
            tmp_texts.append(TLatex(3400,1550,"#splitline{#bf{Axial-vector mediator}}{#bf{& Dirac DM}}"))
            tmp_texts.append(TLatex(3400,1350,"#it{g_{q} = 0.1, g_{DM} = 1, g_{l}=0.1}"))
        elif Scenario == "dijetchi" :
            tmp_texts.append(TLatex(3000,1000,"#splitline{#bf{Axial-vector mediator, Dirac DM}}{#it{g_{q} = 1.0, g_{DM} = 1.0}}"))


        for t in tmp_texts:
            t.SetTextFont(42)
            t.SetTextSize(0.030)
        texts.extend(tmp_texts)

    # elif Mediator=="Vector" and METXonly:
    #     leg1=TLatex(1105,710,"#splitline{#bf{"+Mediator+" mediator, Dirac DM}}{#it{g_{q} = 0.25, g_{DM} = 1}}")
    #     leg1.SetTextFont(42)
    #     leg1.SetTextSize(0.030)
    # elif Mediator=="Axial" and METXonly:
    #     leg1=TLatex(1105,705,"#splitline{#bf{"+Mediator+"-vector mediator, Dirac DM}}{#it{g_{q} = 0.25, g_{DM} = 1}}")
    #     leg1.SetTextFont(42)
    #     leg1.SetTextSize(0.030)

    ################################
    ### CMS / lumi / energy text ###
    ################################

    if logx         :
        # CMS
        leg2=TLatex(100,1470,"#bf{CMS} #it{Preliminary}")
        leg2.SetTextFont(42)
        leg2.SetTextSize(0.045)
        # lumi
        leg3=TLatex(1500,1470,"#bf{Dark Matter Summary}")
        leg3.SetTextFont(42)
        leg3.SetTextSize(0.033)
    #elif Dilepton :
    else :
        # CMS
        if Scenario=="1" and Resonances==0 and Dijet==0 and Dilepton==0 :
            leg2=TLatex(100,1020,"#bf{CMS}")
        else :
            leg2=TLatex(100,2050,"#bf{CMS}")
        leg2.SetTextFont(42)
        leg2.SetTextSize(0.045)
        # lumi
        if Dilepton :
            leg3=TLatex(3200,2050,"12.9 fb^{-1} (13 TeV)")
        elif Scenario == "dijetchi" :
            leg3=TLatex(4200,2050,"35.9 fb^{-1} (13 TeV)")
        elif Scenario=="1" and Resonances==0 and Dijet==0 and Dilepton==0 :
            leg3=TLatex(1200,1020,"12.9 fb^{-1} & 35.9 fb^{-1} (13 TeV)")
        else :
            leg3=TLatex(3200,2050,"12.9 fb^{-1} & 35.9 fb^{-1} (13 TeV)")
        leg3.SetTextFont(42)
        leg3.SetTextSize(0.045)
    # elif DijetOnly :
    #     # CMS
    #     leg2=TLatex(100,1470,"#bf{CMS}")
    #     leg2.SetTextFont(42)
    #     leg2.SetTextSize(0.045)
    #     # lumi
    #     leg3=TLatex(2750,1470,"12.9 fb^{-1} (13 TeV)")
    #     leg3.SetTextFont(42)
    #     leg3.SetTextSize(0.045)
    #elif Mediator=="Vector" and DijetOnly :
    #    # CMS
    #    leg2=TLatex(100,1470,"#bf{CMS}")
    #    leg2.SetTextFont(42)
    #    leg2.SetTextSize(0.045)
    #    # lumi
    #    leg3=TLatex(2550,1470,"12.9 fb^{-1} (13 TeV)")
    #    leg3.SetTextFont(42)
    #    leg3.SetTextSize(0.045)
    # else         :
    #     # CMS
    #     leg2=TLatex(100,1470,"#bf{CMS} #it{Preliminary}")
    #     leg2.SetTextFont(42)
    #     leg2.SetTextSize(0.045)
    #     # lumi
    #     leg3=TLatex(2800,1470,"#bf{Dark Matter Summary} #it{ICHEP 2016}")
    #     leg3.SetTextFont(42)
    #     leg3.SetTextSize(0.033)

    ############
    ### Draw ###
    ############

    for analysis in analyses:
        if not  analysis=="relic":
            leg.AddEntry(tgraph[analysis],text[analysis])

    reliclist = read_relic_lists()
    for analysis in analyses:
        if( not tgraph[analysis]): continue
        print "analysis "+analysis
        tgraph[analysis].SetLineColor(color[analysis])
        tgraph[analysis].SetMarkerSize(0.1)
        tgraph[analysis].SetMarkerColor(color[analysis])
        tgraph[analysis].SetFillColor(color[analysis])
        tgraph[analysis].SetFillStyle(3005)
        tgraph[analysis].SetLineWidth( 202)
        tgraph[analysis].SetLineStyle(linestyle[analysis])
        if analysis == "relic":
            for i in range(0,reliclist[scenario_tag].GetSize()):
                tgraph["relic"] = reliclist[scenario_tag].At(i)
                tgraph["relic"].SetLineColor(color[analysis]-1)
                tgraph["relic"].SetFillColor(color[analysis]-1)
                tgraph["relic"].SetLineStyle(linestyle[analysis])
                tgraph["relic"].SetLineWidth(-202)#was 202
                tgraph["relic"].SetFillStyle(3005)
                tgraph["relic"].Draw("same")
        elif analysis == "chi":
            tgraph[analysis].SetLineWidth(-404)
        tgraph[analysis].Draw("same")

    ########################
    ### Write some texts ###
    ########################


    leg.Draw("same")
    for t in texts: t.Draw("same")

    C.Update()

    ############
    ### Save ###
    ############

    #if METXonly    : C.SaveAs(Mediator+"_METX_Summary.pdf")
    #elif DijetOnly : C.SaveAs(Mediator+"_Dijet_DM.pdf")
    #else           : C.SaveAs(Mediator+"_EXO_Summary.pdf")




    figname = Mediator
    if METX      : figname += "_METX"
    if Dilepton  : figname += "_Dilepton"
    if Dijet     : figname += "_Multijet"
    figname += "_Scenario"+Scenario+"_Summary.pdf"

    C.SaveAs("{OUTPUT}/{FILE}".format(OUTPUT=output,FILE=figname))
    C.Close()

for Mediator in ["Axial", "Vector"]:
    for Scenario in ["1", "2"]:
        for Resonances in [0,1]:
            make_plot(Mediator, Scenario, METX=True, Resonances=Resonances, Dijet=Resonances, Dilepton=False, logx=False, CL="95")
            make_plot(Mediator, Scenario, METX=True, Resonances=Resonances, Dijet=Resonances, Dilepton=True, logx=False, CL="95")


###########
### FIN ###
###########
