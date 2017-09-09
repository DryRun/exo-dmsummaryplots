#########################################
#########################################
###                                   ###
### Draw awesome MET+X Summary plots  ###
###                                   ###
### SI/SD                             ###
###                                   ###
### (c) MET+X Combo                   ###
###                                   ###
#########################################
#########################################
import os
from ROOT import *
import ast
from Utilities import extrapolation
from Utilities import *


def convert_to_nucleon_xs(input_graph, scenario, gq=0.25):

    if(scenario == "SI"):
        if(gq==0.25): c = 6.9e-41*1e12
        elif(gq==1): c = 0.3984e-27*(9./3.14159)
    elif(scenario == "SD"):
        if(gq==0.25): c = 2.4e-42*1e12
        elif(gq==1): c = 4.6*1e-29

    xs_graph = TGraph()
    for i in range(0,input_graph.GetN()) :
            mMed = Double(0)
            mDM  = Double(0)
            input_graph.GetPoint(i,mMed,mDM)
            mR = Double(0.939*mDM)/(0.939+mDM)
            xsec = Double(c*(mR**2)/(mMed**4))
            xs_graph.SetPoint(i,mDM,xsec)
    return xs_graph



def convert_graph_to_lin_scale(graph, convert_x=True, convert_y=True):
    new_graph = TGraph()
    for i in range(0,graph.GetN()):
        x = Double(0)
        y = Double(0)
        graph.GetPoint(i,x,y)
        new_graph.SetPoint(i, pow(10,x) if convert_x else x, pow(10,y) if convert_y else y )
    return new_graph

################
### Settings ###
################
TextonPlot = False


DijetOnly = False

DDresult = "SD"
Resonances = 1
DijetOnly = 0

Extend    = True
vFloor    = False
mDM_lb = 1

#################
### Analyses ####
#################
def make_plot(DDresult, Resonances, DijetOnly):
    if   DDresult == "SI":
        metx    = ["monojet","monophoton","monoZ"]
        resonances = ["trijet","dijet"]
    elif DDresult == "SD":
        metx    = ["monojet","monophoton","monoZ"]
        resonances = ["trijet","dijet"]


    analyses = []
    cmsanalyses = []
    if Resonances  :
        analyses.extend(resonances)
        cmsanalyses.extend(resonances)


    if   DDresult == "SI" and DijetOnly : analyses.extend(["Cresst","CDMSlite","PandaX","LUX","XENON1T"])
    elif DDresult == "SD" and DijetOnly : analyses.extend(["PICASSO", "Pico60","SuperKbb","IceCubebb", "IceCubett"])
    elif DDresult == "SI"               : analyses.extend(["Cresst","CDMSlite","PandaX","LUX","XENON1T"])
    elif DDresult == "SD"               : analyses.extend(["PICASSO", "Pico60","SuperKbb","IceCubebb", "IceCubett"])


    if not DijetOnly:
        analyses.extend(metx)
        cmsanalyses.extend(metx)

    if vFloor: analyses += ["vFloor"]

    print "***********************"
    print "DD result = ", DDresult
    print "List of analyses = ", analyses
    print "***********************"

    if Extend :
        print "*******************"
        print "N.B: METX analyses = " , metx
        print "will be extended downto MDM = " , mDM_lb
        print "*******************"

    tgraph    = {}
    tgraph_original    = {}
    DDgraph   = {}
    color     = {}
    text      = {}
    filepath  = {}
    linestyle = {}

    #############
    ### Files ###
    #############

    if DDresult == "SI":
        filepath["XENON1T"]        = "DD/SI/xenon1t.txt"
        filepath["LUX"]            = "DD/SI/LUX_SI_Combination_Oct2016.txt"#"DD/SI/LUX_SI_DMTools_Jul2016.dat"#"DD/lux2015.txt"
        filepath["PandaX"]         = "DD/SI/pandax_2017.txt"
        filepath["CDMSlite"]       = "DD/SI/cdmslite2015.txt"
        filepath["Cresst"]         = "DD/SI/cresstii.txt"
        filepath["vFloor"]         = "DD/SI/Neutrino_SI.txt"

        filepath["dijet"]          = "Dijet/ScanMM/Dijet_MM_V_Dijetpaper2016_obs_90.root"
        filepath["dijet_exp"]          = "Dijet/ScanMM/Dijet_MM_V_Dijetpaper2016_obs_90.root"



        filepath["trijet"]         = "Trijet/ScanMM/MMedMDM_v_90.root"
        filepath["monojet"]        = "Monojet/EXO-16-048/ScanMM/limits_DD_vector.root"
        filepath["monophoton"]     = "Monophoton/ScanMM/Monophoton_SI_MM_ICHEP2016_obs.root" #outdated
        filepath["monoZ"]          = "MonoZll/EXO-16-052/ScanMM/monoz_contour_observed_limit_vector_cl90_Mmedmore10.txt"
        filepath["monoHgg"]          = "MonoHgg/ScanMM/EXO-16-054/input_combo_MonoHgg_25April_90CL.root"

    elif DDresult == "SD" :
        filepath["PICASSO"]         = "DirectDetection/PicassoFinal.root"
        filepath["Pico60"]         = "DirectDetection/Pico602017.root"
        filepath["SuperKbb"]      = "DirectDetection/SuperKbb.root"
        filepath["IceCubebb"]     = "DirectDetection/IceCubebb.root"
        filepath["IceCubett"]     = "DirectDetection/IceCubett.root"
        filepath["vFloor"]         = "DD/SD/Neutrino_SD.txt"
        filepath["dijet"]          = "Dijet/ScanMM/Dijet_MM_A_Dijetpaper2016_obs_90.root"
        filepath["trijet"]         = "Trijet/ScanMM/MMedMDM_av_90.root"
        filepath["monojet"]        = "Monojet/EXO-16-048/ScanMM/limits_DD_axial.root"
        filepath["monophoton"]     = "Monophoton/ScanMM/Monophoton_SD_MM_ICHEP2016_obs.root" #outdated
        filepath["monoZ"]          = "MonoZll/EXO-16-052/ScanMM/monoz_contour_observed_limit_axial_cl90_Mmedmore10.txt"

    #######################
    ### Plot linestyles ###
    #######################

    linestyle["vFloor"]     = kDashed
    ### SI
    linestyle["XENON1T"]    = kSolid
    linestyle["LUX"]        = kSolid
    linestyle["PandaX"]     = kSolid
    linestyle["CDMSlite"]   = kSolid
    linestyle["Cresst"]     = kSolid
    ### SD
    linestyle["PICASSO"]     = kSolid
    linestyle["Pico60"]     = kSolid
    linestyle["SuperKbb"]     = kSolid
    linestyle["IceCubebb"]     = kSolid
    linestyle["IceCubett"]     = kSolid
    ### CMS Met-less
    linestyle["dijet"]      = kSolid
    linestyle["dijet_2016"] = kSolid
    linestyle["trijet"]     = kSolid
    ### CMS MET+X
    linestyle["monophoton"] = kSolid
    linestyle["monoZ"]      = kSolid
    linestyle["monoHgg"]      = kSolid
    linestyle["monotop"]    = kSolid
    linestyle["monojet"]    = kSolid


    ###################
    ### Plot colors ###
    ###################

    color["vFloor"]     = kOrange+3
    ### SI
    color["Cresst"]     = kGreen+1
    color["CDMSlite"]   = kGreen+3
    color["PandaX"]     = kGreen+2
    color["LUX"]        = kGreen+4
    color["XENON1T"]    = kGreen-5
    ### SD
    color["PICASSO"]     = kBlack
    color["Pico60"]     = kGreen+1
    color["SuperKbb"]     = kGreen+3
    color["IceCubebb"]     = kGreen+2
    color["IceCubett"]     = kGreen
    ### CMS Met-less
    color["dijet"]      = kAzure-9
    color["dijet"]      = kBlue-8
    color["dijet"]      = kYellow-10
    color["dijet_2016"] = kAzure
    color["trijet"]     = kAzure+10
    color["trijet"]     = kCyan-10

    color["chi"]        = kBlue
    ### CMS MET+X
    color["monojet"]    = kRed+2#kRed+1
    color["monophoton"] = kOrange+9#kRed+2
    color["monoZ"]      = kOrange+1#kRed+3
    color["monoHgg"]          = kMagenta-7
    color["monotop"]    = kViolet+1

    linecolor = {}
    linecolor["dijet"] = kYellow +3
    linecolor["trijet"] = kCyan-5

    ##################
    ### Plot texts ###
    ##################

    text["vFloor"]     = "#nu floor (permeable)"
    ### SI
    text["XENON1T"]    = "#bf{XENON1T}"
    text["LUX"]        = "#bf{LUX}"
    text["PandaX"]     = "#bf{PandaX-II}"
    text["CDMSlite"]   = "#bf{CDMSlite}"
    text["Cresst"]     = "#bf{CRESST-II}"
    ### SD
    text["PICASSO"]     = "#bf{PICASSO}"
    text["Pico60"]      = "#bf{PICO-60}"
    text["SuperKbb"]    = "#bf{Super-K (b#bar{b})}"
    text["IceCubebb"]   = "#bf{IceCube (b#bar{b})}"
    text["IceCubett"]   = "#bf{IceCube (t#bar{t})}"
    ### CMS MET-less
    if DDresult=="SD" :
        text["dijet"]      = "CMS Dijet [EXO-16-056]"
    else :
        text["dijet"]      = "#splitline{CMS Dijet}{[EXO-16-056]}"
    text["dijet_2016"] = "CMS Dijet #it{[EXO-16-056]}"
    text["trijet"]     = "CMS Boosted dijet #it{[EXO-17-001]}"
    text["chi"]        = "chi obs. (exp.excl.)"
    ### CMS MET+X
    #~ text["monojet"]    = "CMS DM+j/V(qq) #it{[EXO-16-056]}"
    #~ text["monoZ"]      = "CMS DM+Z(ll) #it{[EXO-16-052]}"
    text["monoHgg"]    = "CMS H_{#gamma #gamma} #it{[EXO-16-054]}"
    text["monophoton"] = "CMS DM+#gamma #it{[EXO-16-039]}"

    text["monojet"]        = "#splitline{DM + j/V(qq) (35.9 fb^{-1})}{#it{[EXO-16-048]}}"
    text["monoz"]          = "#splitline{DM + Z_(ll) (35.9 fb^{-1})}{#it{[EXO-16-052]}}"#text["monotop"]    = "CMS DM+t (FC) #it{[EXO-16-040]}"
    text["monoHgg"]        = "#splitline{DM + H_{#gamma #gamma} (35.9 fb^{-1})}{#it{[EXO-16-054]}}"
    text["monophoton"]     = "#splitline{DM + #gamma (12.9 fb^{-1})}{#it{[EXO-16-039]}}"

    ####################
    ### Get datfiles ###
    ### Get graphs   ###
    ####################

    for analysis in analyses:
        if   analysis == "dijet"          : tgraph["dijet"]          = TFile(filepath[analysis]).Get("Obs_90")
        elif analysis == "dijet_2016"     : tgraph["dijet_2016"]     = TFile(filepath[analysis]).Get("Obs_90")
        elif analysis == "dijet_2016_exp" : tgraph["dijet_2016_exp"] = TFile(filepath[analysis]).Get("Obs_90")
        elif analysis == "trijet"         : tgraph["trijet"]         = TFile(filepath[analysis]).Get("obs_025")
        elif analysis == "monojet"        : tgraph["monojet"]        = TFile(filepath[analysis]).Get("contour_obs_graph")
        elif analysis == "monophoton"     : tgraph["monophoton"]     = convert_graph_to_lin_scale(TFile(filepath[analysis]).Get("monophoton_obs"))
        elif analysis == "monoZ"          : tgraph["monoZ"]          = TGraph(filepath[analysis])
        elif analysis == "monoHgg"        : tgraph["monoHgg"]        = TFile(filepath[analysis]).Get("observed_baryonic_MonoHgg")


        elif analysis == "PICASSO"        : tgraph["PICASSO"]        = TFile(filepath[analysis]).Get("Obs_90")
        elif analysis == "Pico60"         : tgraph["Pico60"]         = TFile(filepath[analysis]).Get("Obs_90")
        elif analysis == "SuperKbb"       : tgraph["SuperKbb"]       = TFile(filepath[analysis]).Get("Obs_90")
        elif analysis == "IceCubebb"      : tgraph["IceCubebb"]      = TFile(filepath[analysis]).Get("Obs_90")
        elif analysis == "IceCubett"      : tgraph["IceCubett"]      = TFile(filepath[analysis]).Get("Obs_90")
        else                              : tgraph[analysis]         = TGraph(filepath[analysis])

    #######################
    ### Transform 90%CL ###
    ### to DD plane     ###
    #######################



    for analysis in cmsanalyses:
        if not analysis=="monophoton":
            tgraph[analysis] = convert_to_nucleon_xs(tgraph[analysis],DDresult)

    if Extend :
        extrapolation( tgraph, DijetOnly, Resonances, resonances, metx, mDM_lb )


    ###################
    ### Make Canvas ###
    ### Add legend  ###
    ###################

    if not DijetOnly:
        C=TCanvas("C","C",1000,600)
        C.Divide(2)
        C.cd(1).SetPad(0.0,0,0.75,1.0)
        C.cd(1).SetLeftMargin(0.15)
    else :
        C=TCanvas("C","C",600,600)
        C.Divide(1)
        C.cd(1).SetPad(0.0,0,1.0,1.0)
        C.cd(1).SetLeftMargin(0.15)
        C.cd(1).SetRightMargin(0.05)

    C.cd(1).SetLogx()
    C.cd(1).SetLogy()

    if   DDresult=="SD" and DijetOnly : frame = C.cd(1).DrawFrame(mDM_lb,1e-44,2000,1e-37)
    elif DDresult=="SD"               : frame = C.cd(1).DrawFrame(mDM_lb,1e-45,2000,5*1e-37)
    elif DDresult=="SI" and DijetOnly : frame = C.cd(1).DrawFrame(mDM_lb,1e-47,2000,1e-37)
    elif DDresult=="SI"               : frame = C.cd(1).DrawFrame(mDM_lb,1e-47,2000,2*1e-35)


    C.cd(1).SetTickx()
    C.cd(1).SetTicky()

    frame.SetXTitle("Dark matter mass m_{ DM} [GeV]")
    if   DDresult=="SD": frame.SetYTitle("#sigma^{SD}_{DM-proton} [cm^{2}]")
    elif DDresult=="SI": frame.SetYTitle("#sigma^{SI}_{DM-nucleon} [cm^{2}]")
    frame.GetXaxis().SetTitleSize(0.045)
    frame.GetYaxis().SetTitleSize(0.045)
    frame.GetXaxis().SetTitleOffset(1.0)
    frame.GetYaxis().SetTitleOffset(1.5)

    if DijetOnly:
        if DDresult == "SI" : leg  = TLatex(0.1,1.2e-38,"#bf{CMS}")
        if DDresult == "SD" : leg  = TLatex(0.1,1.2e-37,"#bf{CMS}")
        leg.SetTextFont(42)
        leg.SetTextSize(0.04)
        leg.Draw("same")

    ###################
    ### Add legend  ###
    ###################

    if not DijetOnly:
        leg1=C.BuildLegend(0.7,0.4,0.95,0.95)
        leg1.SetBorderSize(0)
        leg1.SetTextFont(42)
        leg1.SetTextSize(0.025)
        leg1.SetTextAlign(12)
        leg1.Clear()
        if DDresult=="SI":
            leg1.SetHeader("#splitline{#bf{CMS observed exclusion 90% CL}}{Vector med., Dirac DM; g_{ q} = 0.25, g_{ DM} = 1.0}")
        elif DDresult=="SD":
            leg1.SetHeader("#splitline{#bf{CMS observed exclusion 90% CL}}{Axial-vector med., Dirac DM; g_{ q} = 0.25, g_{ DM} = 1.0}")

        leg2=C.BuildLegend(0.7,0.05,0.95,0.4)
        leg2.SetBorderSize(0)
        leg2.SetTextFont(42)
        leg2.SetTextSize(0.025)
        leg2.SetTextAlign(12)
        leg2.Clear()
        if   DDresult == "SI": leg2.SetHeader("#bf{DD observed exclusion 90% CL}")
        elif DDresult == "SD": leg2.SetHeader("#bf{DD/ID observed exclusion 90% CL}")

        for analysis in analyses:
            if analysis=="dijet" or analysis == "dijet_2016": leg1.AddEntry(tgraph[analysis],"#splitline{#bf{Dijet} (35.9 fb^{-1})}{#it{[EXO-16-056]}}")
            elif analysis == "trijet"     : leg1.AddEntry(tgraph[analysis],"#splitline{#bf{Boosted dijet} (35.9 fb^{-1})}{#it{[EXO-17-001]}}")
            elif analysis == "XENON1T"    : leg2.AddEntry(tgraph[analysis],"#splitline{"+text[analysis]+"}{#it{[arXiv:1705.06655]}}","L")
            elif analysis == "LUX"        : leg2.AddEntry(tgraph[analysis],"#splitline{"+text[analysis]+"}{#it{[arXiv:1608.07648]}}","L")#1608.07648]}}") #[arXiv:1512.03506]}}")
            elif analysis == "PandaX"     : leg2.AddEntry(tgraph[analysis],"#splitline{"+text[analysis]+"}{#it{[arXiv:1708.06917]}}","L")
            elif analysis == "CDMSlite"   : leg2.AddEntry(tgraph[analysis],"#splitline{"+text[analysis]+"}{#it{[arXiv:1509.02448]}}","L")
            elif analysis == "Cresst"     : leg2.AddEntry(tgraph[analysis],"#splitline{"+text[analysis]+"}{#it{[arXiv:1509.01515]}}","L")
            elif analysis == "PICASSO"    : leg2.AddEntry(tgraph[analysis],"#splitline{"+text[analysis]+"}{#it{[arXiv:1611.01499]}}","L")
            elif analysis == "Pico60"     : leg2.AddEntry(tgraph[analysis],"#splitline{"+text[analysis]+"}{#it{[arXiv:1702.07666]}}","L")
            elif analysis == "SuperKbb"   : leg2.AddEntry(tgraph[analysis],"#splitline{"+text[analysis]+"}{#it{[arXiv:1503.04858]}}","L")
            elif analysis == "IceCubebb"  : leg2.AddEntry(tgraph[analysis],"#splitline{"+text[analysis]+"}{#it{[arXiv:1612.05949]}}","L")
            elif analysis == "IceCubett"  : leg2.AddEntry(tgraph[analysis],"#splitline{"+text[analysis]+"}{#it{[arXiv:1601.00653]}}","L")
            elif analysis == "monojet"    : leg1.AddEntry(tgraph[analysis],"#splitline{#bf{DM + j/V_{qq}} (35.9 fb^{-1})}{#it{[EXO-16-048]}}","L")
            elif analysis == "monoZ"      : leg1.AddEntry(tgraph[analysis],"#splitline{#bf{DM + Z_{ll}} (35.9 fb^{-1})}{#it{[EXO-16-052]}}","L")
            elif analysis == "monophoton" : leg1.AddEntry(tgraph[analysis],"#splitline{#bf{DM + #gamma} (12.9 fb^{-1})}{#it{[EXO-16-039]}}","L")
            elif analysis == "monoHgg"    : leg1.AddEntry(tgraph[analysis],"#splitline{#bf{DM + H_{#gamma #gamma}} (35.9 fb^{-1})}{#it{[EXO-16-054]}}","L")



    ############
    ### Draw ###
    ############

    if not DijetOnly:
        C.cd(2).SetPad(0.75,0.0,1.0,1.0)
        C.Update()
        C.cd(1)
        C.Update()

    C.Update()



    ####################
    ### Draw RESULTS ###
    ####################
    gStyle.SetHatchesLineWidth(2)
    for analysis in analyses:
        tgraph[analysis].SetLineColor(color[analysis])
        tgraph[analysis].SetFillColor(color[analysis])
        tgraph[analysis].SetFillColor(color[analysis])
        tgraph[analysis].SetFillStyle(3005)
        tgraph[analysis].SetLineWidth( 203)
        tgraph[analysis].SetLineStyle(linestyle[analysis])
        tgraph[analysis].SetMarkerSize(0.1)
        tgraph[analysis].SetMarkerColor(color[analysis])
        if analysis=="monoZ":
            tgraph[analysis].SetLineWidth(-203)
        if analysis=="dijet" or analysis == "dijet_2016" or analysis=="trijet":
            tgraph[analysis].SetLineWidth(2)
            tgraph[analysis].SetFillStyle(1001)
            tgraph[analysis].SetLineColor(linecolor[analysis])
            tgraph[analysis].SetMarkerColor(linecolor[analysis])
            tgraph[analysis].Draw("F,same")
            tgraph[analysis].Draw("same")
        elif analysis == "XENON1T" or analysis == "LUX" or analysis=="PandaX" or analysis=="CDMSlite" or analysis=="Cresst":
            tgraph[analysis].SetFillColor(kWhite)
            tgraph[analysis].SetFillStyle(4001)
            tgraph[analysis].SetLineWidth(2)
            tgraph[analysis].Draw("same")
        elif analysis == "PICASSO" or analysis=="Pico60" or analysis=="SuperKbb" or analysis=="IceCubebb" or analysis=="IceCubett":
            tgraph[analysis].SetFillColor(kWhite)
            tgraph[analysis].SetFillStyle(4001)
            tgraph[analysis].SetLineWidth(2)
            tgraph[analysis].Draw("same")
        elif analysis == "monojet" or analysis=="monophoton" or analysis=="monoZ" or analysis=="monoHgg" or analysis=="dijet" or analysis=="dijet_2016":
            tgraph[analysis].Draw("same")
        elif analysis == "vFloor" :
            tgraph[analysis].SetLineWidth(-102)
            tgraph[analysis].Draw("same")

    texts = []

    texts.append(add_text(0.15,0.4,0.89,0.99,"#bf{CMS} Preliminary"))
    texts.append(add_text(0.7,0.88,0.89,0.99,"LHCP 2017"))
    C.Update()
    C.cd(1).RedrawAxis()
    ############
    ### Save ###
    ############

    if( not os.path.exists("./output") ): os.makedirs("./output")
    if DijetOnly : C.SaveAs("./output/"+DDresult+"_CMSDD_Dijet.pdf")
    elif Resonances : C.SaveAs("./output/"+DDresult+"_CMSDD_Summary.pdf")
    else         : C.SaveAs("./output/"+DDresult+"_CMSDD_Summary_nodijet.pdf")

    ###########
    ### FIN ###
    ###########

make_plot("SI",1,0)
make_plot("SD",1,0)
