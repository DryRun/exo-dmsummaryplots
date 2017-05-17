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
################
### Settings ###
################
TextonPlot = False


DijetOnly = False

#~ DDresult = raw_input('Choose DD [SI or SD]: ')
#~ Resonances  = ast.literal_eval(raw_input('Resonances? [True or False]: '))
#~ if Resonances: DijetOnly = ast.literal_eval(raw_input('Dijet only? [True or False]: '))

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


    if   DDresult == "SI" and DijetOnly : analyses.extend(["Cresst","CDMSlite","PandaX","LUX"])
    elif DDresult == "SD" and DijetOnly : analyses.extend(["PICASSO", "Pico60","SuperKbb","IceCubebb", "IceCubett"])
    elif DDresult == "SI"               : analyses.extend(["Cresst","CDMSlite","PandaX","LUX"])
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
        filepath["LUX"]            = "DD/SI/LUX_SI_Combination_Oct2016.txt"#"DD/SI/LUX_SI_DMTools_Jul2016.dat"#"DD/lux2015.txt"
        filepath["PandaX"]         = "DD/SI/pandax.txt"
        filepath["CDMSlite"]       = "DD/SI/cdmslite2015.txt"
        filepath["Cresst"]         = "DD/SI/cresstii.txt"
        filepath["vFloor"]         = "DD/SI/Neutrino_SI.txt"

        #~ filepath["dijet"]          = "Dijet/ScanMM/Dijet_MM_V_Dijetpaper2016_obs_90.root"
        filepath["dijet"]          = "Dijet/ScanMM/Dijet_MM_V_Dijetpaper2016_obs_90.root"
        filepath["dijet_exp"]          = "Dijet/ScanMM/Dijet_MM_V_Dijetpaper2016_obs_90.root"



        filepath["trijet"]         = "Trijet/ScanMM/MMedMDM_v_90.root"
        filepath["monojet"]        = "Monojet/EXO-16-048/ScanMM/limits_DD_vector.root"
        filepath["monophoton"]     = "Monophoton/ScanMM/Monophoton_SI_MM_ICHEP2016_obs.root" #outdated
        filepath["monoZ"]          = "MonoZll/EXO-16-052/ScanMM/monoz_contour_observed_limit_vector_cl90_Mmedmore10.txt"
        filepath["monoHgg"]          = "MonoHgg/ScanMM/EXO-16-054/input_combo_MonoHgg_25April_90CL.root"

    elif DDresult == "SD" :
        # filepath["Pico2L"]         = "DD/SD/Pico2L.txt"
        # filepath["Pico60"]         = "DD/SD/Pico60.txt"
        # filepath["SuperK"]         = "DD/SD/SuperKtautau.txt"
        # filepath["IceCube"]        = "DD/SD/IceCubetautau.txt"

        # filepath["PICASSO"]         = "Pico60/PicassoFinal.root"
        # filepath["Pico60"]         = "Pico60/Pico602017.root"
        # filepath["SuperKbb"]      = "Pico60/Neutrino.root"
        # filepath["IceCubebb"]     = "Pico60/Neutrino.root"
        # filepath["IceCubett"]     = "Pico60/Neutrino.root"

        filepath["PICASSO"]         = "DirectDetection/PicassoFinal.root"
        filepath["Pico60"]         = "DirectDetection/Pico602017.root"
        filepath["SuperKbb"]      = "DirectDetection/SuperKbb.root"
        filepath["IceCubebb"]     = "DirectDetection/IceCubebb.root"
        filepath["IceCubett"]     = "DirectDetection/IceCubett.root"
        filepath["vFloor"]         = "DD/SD/Neutrino_SD.txt"
        ### ICHEP
    #    filepath["dijet"]          = "Dijet/ScanMM/MMedMDM_dijet_av_90_Phil500.root"
    #from Tyler EXO-16-056
        filepath["dijet"]          = "Dijet/ScanMM/Dijet_MM_A_Dijetpaper2016_obs_90.root"
        ### Dijet paper
        #filepath["dijet_2016"]     = "Dijet/ScanMM/MMedMDM_dijet_av_90_Phil600.root"
        #filepath["dijet_2016_exp"] = "Dijet/ScanMM/MMedMDM_dijet_av_90_Phil600.root"

        #filepath["dijet_2016"]     = "Dijet/ScanMM/MMedMDM_dijet_av_90_top56.root"
        #filepath["dijet_2016_exp"] = "Dijet/ScanMM/MMedMDM_dijet_av_90_top56.root"
        #~ filepath["dijet_2016"]          = "Dijet/ScanMM/Dijet_MM_A_Dijetpaper2016_obs_90.root"
        #~ filepath["dijet_2016_exp"]          = "Dijet/ScanMM/Dijet_MM_A_Dijetpaper2016_obs_90.root"
        filepath["trijet"]         = "Trijet/ScanMM/MMedMDM_av_90.root"
        filepath["monojet"]        = "Monojet/EXO-16-048/ScanMM/limits_DD_axial.root"
        filepath["monophoton"]     = "Monophoton/ScanMM/Monophoton_SD_MM_ICHEP2016_obs.root" #outdated
        filepath["monoZ"]          = "MonoZll/EXO-16-052/ScanMM/monoz_contour_observed_limit_axial_cl90_Mmedmore10.txt"

    #######################
    ### Plot linestyles ###
    #######################

    linestyle["vFloor"]     = kDashed
    ### SI
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
    #    if   analysis == "dijet"          : tgraph["dijet"]          = TFile(filepath[analysis]).Get("obs_025")

    #from Tyler EXO-16-056
        if   analysis == "dijet"          : tgraph["dijet"]          = TFile(filepath[analysis]).Get("Obs_90")

        #elif analysis == "dijet_2016"     : tgraph["dijet_2016"]     = TFile(filepath[analysis]).Get("obs_025")
        #elif analysis == "dijet_2016_exp" : tgraph["dijet_2016_exp"] = TFile(filepath[analysis]).Get("exp_025")
        elif analysis == "dijet_2016"     : tgraph["dijet_2016"]     = TFile(filepath[analysis]).Get("Obs_90")
        elif analysis == "dijet_2016_exp" : tgraph["dijet_2016_exp"] = TFile(filepath[analysis]).Get("Obs_90")
    #    elif analysis == "monojet"        : tgraph["monojet"]        = TFile(filepath[analysis]).Get("observed")
        elif analysis == "trijet"         : tgraph["trijet"]         = TFile(filepath[analysis]).Get("obs_025")
        elif analysis == "monojet"        :
            tgraph["monojet"]        = TFile(filepath[analysis]).Get("contour_obs_graph")
        elif analysis == "monophoton"     : tgraph["monophoton"]     = TFile(filepath[analysis]).Get("monophoton_obs")
        elif analysis == "monoZ"   : tgraph["monoZ"]          = TGraph(filepath[analysis])
        elif analysis == "monoHgg"        : tgraph["monoHgg"]     = TFile(filepath[analysis]).Get("observed_baryonic_MonoHgg")


    #    elif analysis == "monotop"        : tgraph["monotop"]        = TFile(filepath[analysis]).Get("observed")
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

    if DDresult=="SI":
        #c_SI = 0.3984e-27*(9./3.14159) #gq=1
        c_SI = 6.9e-41*1e12
        for analysis in cmsanalyses:

            DDgraph[analysis]=TGraph()
            for i in range(0,tgraph[analysis].GetN()) :
                mMed = Double(0)
                mDM  = Double(0)
                tgraph[analysis].GetPoint(i,mMed,mDM)
                #~ print "SI - analysis = ", analysis, ", i = ", i, ", mMed = ", mMed, ", mDM = ", mDM
                if analysis == "monophoton":
                    DDgraph[analysis].SetPoint(i,pow(10,mMed),pow(10,mDM))
                # elif analysis == "monojet" or analysis == "monoZ":
                #     DDgraph[analysis]=tgraph[analysis]
                else:
                    mR = Double(0.939*mDM)/(0.939+mDM)
                    xsec = Double(c_SI*(mR*mR)/(mMed*mMed*mMed*mMed))
    #                print "x-sec = ", xsec
                    DDgraph[analysis].SetPoint(i,mDM,xsec)
                    if analysis == "monoHgg" :
                        print "SD - analysis = ", analysis, ", i = ", i, ", mMed = ", mMed, ", mDM = ", mDM
                        print "xsec ", xsec, " mR ", mR
            tgraph[analysis] = DDgraph[analysis]
    elif DDresult=="SD":
        #c_SD = 4.6*1e-29  #gq=1
        c_SD = 2.4e-42*1e12
        for analysis in cmsanalyses:
            DDgraph[analysis]=TGraph()
            for i in range(0,tgraph[analysis].GetN()) :
                mMed = Double(1)
                mDM  = Double(1)
                tgraph[analysis].GetPoint(i,mMed,mDM)
    #            print "SD - analysis = ", analysis, ", i = ", i, ", mMed = ", mMed, ", mDM = ", mDM
                if analysis == "monophoton":
                    DDgraph[analysis].SetPoint(i,pow(10,mMed),pow(10,mDM))
                else:
                    mR = Double(0.939*mDM)/(0.939+mDM)
                    xsec = Double(c_SD*(mR*mR)/(mMed*mMed*mMed*mMed))
    #               print "x-sec = ", xsec
                    DDgraph[analysis].SetPoint(i,mDM,xsec)
            tgraph[analysis] = DDgraph[analysis]

        print "****BEFORE EXTRAPOLATIOn*****"
        #~ for analysis in cmsanalyses :
    #        print "Analysis ", analysis
            #~ for i in range(0,tgraph[analysis].GetN()) :
                #~ mDM_i  = Double(0)
                #~ xsec_i = Double(0)
                #~ tgraph[analysis].GetPoint(i,mDM_i,xsec_i)
    #            print "i = ", i, " mDM_i = ", mDM_i, "xsec_i = ", xsec_i
        print "*********"


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

    #~ if not DijetOnly:
        #~ if DDresult == "SI" : leg  = TLatex(100,3e-34,"#it{LHCP 2017}")
        #~ if DDresult == "SD" : leg  = TLatex(100,3e-36,"#it{LHCP 2017}")
        #~ leg.SetTextFont(42)
        #~ leg.SetTextSize(0.04)
        #~ leg.Draw("same")
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
            elif analysis == "LUX"        : leg2.AddEntry(tgraph[analysis],"#splitline{"+text[analysis]+"}{#it{[arXiv:1608.07648]}}","L")#1608.07648]}}") #[arXiv:1512.03506]}}")
            elif analysis == "PandaX"     : leg2.AddEntry(tgraph[analysis],"#splitline{"+text[analysis]+"}{#it{[arXiv:1607.07400]}}","L")
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
            elif analysis == "monoHgg" : leg1.AddEntry(tgraph[analysis],"#splitline{#bf{DM + H_{#gamma #gamma}} (35.9 fb^{-1})}{#it{[EXO-16-054]}}","L")
            #else                          : leg1.AddEntry(tgraph[analysis],text[analysis])



    ######################
    ### Plot SI LEGEND ###
    ######################
    if TextonPlot :
        if not DijetOnly and not Resonances and DDresult=="SI":
            # SI MET+X monoZ
            legx1  = TLatex(15,4e-40,"CMS "+text["monoZ"])
            legx1.SetTextAngle(1)
            legx1.SetTextFont(42)
            legx1.SetTextColor(color["monoZ"])
            legx1.SetTextSize(0.025)
            legx1.Draw("same")
        # SI MET+X monophoton
            legx2  = TLatex(30,6e-41,"CMS "+text["monophoton"])
            legx2.SetTextAngle(1)
            legx2.SetTextFont(42)
            legx2.SetTextColor(color["monophoton"])
            legx2.SetTextSize(0.025)
            legx2.Draw("same")
        # SI MET+X monojet
            legx3 = TLatex(50,1e-42,"CMS "+text["monojet"])
            legx3.SetTextAngle(1)
            legx3.SetTextFont(42)
            legx3.SetTextColor(color["monojet"])
            legx3.SetTextSize(0.025)
            legx3.Draw("same")

        elif DDresult=="SI" and DijetOnly:
        #Cresst Dijet
            legy1 = TLatex(7,3e-41,"#splitline{"+text["Cresst"]+"}{#it{arXiv:1509.01515}}")
            legy1.SetTextAngle(0)
            legy1.SetTextFont(42)
            legy1.SetTextColor(color["Cresst"])
            legy1.SetTextSize(0.025)
            legy1.Draw("same")
        #CDMS Dijet
            legy2 = TLatex(2.,8e-39,"#splitline{"+text["CDMSlite"]+"}{#it{arXiv:1509.02448}}")
            legy2.SetTextAngle(0)
            legy2.SetTextFont(42)
            legy2.SetTextColor(color["CDMSlite"])
            legy2.SetTextSize(0.025)
            legy2.Draw("same")
        #PandaX Dijet
            legy4 = TLatex(30,1e-45,"#splitline{"+text["PandaX"]+"}{#it{arXiv:1607.07400}}")
            legy4.SetTextAngle(0)
            legy4.SetTextFont(42)
            legy4.SetTextColor(color["PandaX"])
            legy4.SetTextSize(0.025)
            legy4.Draw("same")
        #LUX Dijet
            legy3 = TLatex(200,8.0e-47,"#splitline{"+text["LUX"]+"}{#it{arXiv:1608.07648}}")
            legy3.SetTextAngle(0)
            legy3.SetTextFont(42)
            legy3.SetTextColor(color["LUX"])
            legy3.SetTextSize(0.025)
            legy3.Draw("same")
        #Dijet
            legy5  = TLatex(100,1.3e-40,"#splitline{#bf{CMS (dijet)}}{#splitline{Vector mediator, Dirac DM}{g_{q} = 0.25, g_{DM} = 1.0}}")
            legy5.SetTextAngle(0)
            legy5.SetTextFont(42)
            legy5.SetTextColor(color["dijet"])
            legy5.SetTextSize(0.025)
            legy5.Draw("same")

        elif DDresult=="SI":
        # v Floor
            if vFloor == True :
                legy0  = TLatex(1.5,3.0e-46,"#splitline{#nu Floor (perm.)}{arXiv/1506.08309}")
                legy0.SetTextAngle(0)
                legy0.SetTextFont(42)
                legy0.SetTextColor(color["vFloor"])
                legy0.SetTextSize(0.025)
                legy0.Draw("same")

            legy1 = TLatex(1.7,2.0e-38,text["CDMSlite"])
            legy1.SetTextAngle(280)
            legy1.SetTextFont(42)
            legy1.SetTextColor(color["CDMSlite"])
            legy1.SetTextSize(0.020)
            legy1.Draw("same")
        #Cresst MET+X
            legy2 = TLatex(10,3e-41,text["Cresst"])
            legy2.SetTextAngle(5)
            legy2.SetTextFont(42)
            legy2.SetTextColor(color["Cresst"])
            legy2.SetTextSize(0.020)
            legy2.Draw("same")
        #PandaX MET+X
            legy4 = TLatex(85,6e-46,text["PandaX"])
            legy4.SetTextAngle(13)
            legy4.SetTextFont(42)
            legy4.SetTextColor(color["PandaX"])
            legy4.SetTextSize(0.020)
            legy4.Draw("same")
        #LUX MET+X
            legy3 = TLatex(100,6e-47,text["LUX"])
            legy3.SetTextAngle(13)
            legy3.SetTextFont(42)
            legy3.SetTextColor(color["LUX"])
            legy3.SetTextSize(0.020)
            legy3.Draw("same")

            legx4  = TLatex(10,2e-39,text["monoZ"])
            legx4.SetTextAngle(2)
            legx4.SetTextFont(42)
            legx4.SetTextColor(color["monoZ"])
            legx4.SetTextSize(0.020)
            legx4.Draw("same")
        # SD MET+X monophoton
            legx5  = TLatex(40,4.0e-41,text["monophoton"])
            legx5.SetTextAngle(0)
            legx5.SetTextFont(42)
            legx5.SetTextColor(color["monophoton"])
            legx5.SetTextSize(0.020)
            legx5.Draw("same")
        # SD MET+X monojet
            legx6  = TLatex(40,6.0e-42,text["monojet"])
            legx6.SetTextAngle(0)
            legx6.SetTextFont(42)
            legx6.SetTextColor(color["monojet"])
            legx6.SetTextSize(0.020)
            legx6.Draw("same")
        # SD dijet
            legx7  = TLatex(1.2,1.0e-41,text["dijet"])
            legx7.SetTextAngle(0)
            legx7.SetTextFont(42)
            legx7.SetTextColor(color["dijet"])
            legx7.SetTextSize(0.020)
            legx7.Draw("same")
        # SD trijet
            legx8  = TLatex(2,1.0e-37,text["trijet"])
            legx8.SetTextAngle(0)
            legx8.SetTextFont(42)
            legx8.SetTextColor(color["trijet"])
            legx8.SetTextSize(0.020)
            legx8.Draw("same")

    ###############
    ### Plot SD ###
    ###############

        if not DijetOnly and not Resonances and DDresult=="SD":
            # SD MET+X monoZ
            legx1  = TLatex(3,1e-41,text["monoZ"])
            legx1.SetTextAngle(5)
            legx1.SetTextFont(42)
            legx1.SetTextColor(color["monoZ"])
            legx1.SetTextSize(0.025)
            legx1.Draw("same")
        # SD MET+X monophoton
            legx2  = TLatex(3,1.6e-42,text["monophoton"])
            legx2.SetTextAngle(3)
            legx2.SetTextFont(42)
            legx2.SetTextColor(color["monophoton"])
            legx2.SetTextSize(0.025)
            legx2.Draw("same")
        # SD MET+X monojet
            legx3  = TLatex(3,4.0e-44,text["monojet"])
            legx3.SetTextAngle(2)
            legx3.SetTextFont(42)
            legx3.SetTextColor(color["monojet"])
            legx3.SetTextSize(0.025)
            legx3.Draw("same")


        elif DDresult=="SD" and DijetOnly:
            legy0  = TLatex(11,6.3e-39,"#splitline{"+text["PICASSO"]+"}{#it{arXiv:1611.01499}}")
            legy0.SetTextAngle(0)
            legy0.SetTextFont(42)
            legy0.SetTextColor(color["PICASSO"])
            legy0.SetTextSize(0.020)
            legy0.Draw("same")
            # Pico60 MET+X
            legy1  = TLatex(15,8e-41,"#splitline{"+text["Pico60"]+"}{#it{arXiv:1702.07666}}")
            legy1.SetTextAngle(0)
            legy1.SetTextFont(42)
            legy1.SetTextColor(color["Pico60"])
            legy1.SetTextSize(0.020)
            legy1.Draw("same")
        # SuperK MET+X
            legy2  = TLatex(10,6.0e-40,"#splitline{"+text["SuperKbb"]+"}{#it{arXiv:1503.04858}}")
            legy2.SetTextAngle(0)
            legy2.SetTextFont(42)
            legy2.SetTextColor(color["SuperKbb"])
            legy2.SetTextSize(0.020)
            legy2.Draw("same")
        # IceCube MET+X
            legy3  = TLatex(300,1.3e-39,"#splitline{"+text["IceCubebb"]+"}{#it{arXiv:1612.05949}}")
            legy3.SetTextAngle(0)
            legy3.SetTextFont(42)
            legy3.SetTextColor(color["IceCubebb"])
            legy3.SetTextSize(0.020)
            legy3.Draw("same")
            legy4  = TLatex(330,7.0e-41,"#splitline{"+text["IceCubett"]+"}{#it{arXiv:1601.00653}}")
            legy4.SetTextAngle(0)
            legy4.SetTextFont(42)
            legy4.SetTextColor(color["IceCubett"])
            legy4.SetTextSize(0.020)
            legy4.Draw("same")
        # SD dijet
            legx5  = TLatex(30,6.0e-42,"#splitline{#bf{CMS (dijet)}}{#splitline{Axial-vector mediator, Dirac DM}{g_{q} = 0.25, g_{DM} = 1.0}}")
            legx5.SetTextAngle(0)
            legx5.SetTextFont(42)
            legx5.SetTextColor(color["dijet"])
            legx5.SetTextSize(0.030)
            legx5.Draw("same")
        elif DDresult=="SD":
                        # v Floor
            if vFloor == True :
                legy0  = TLatex(30,5.0e-45,"#nu Floor (permeable) arXiv/1506.08309")
                legy0.SetTextAngle(10)
                legy0.SetTextFont(42)
                legy0.SetTextColor(color["vFloor"])
                legy0.SetTextSize(0.025)
                legy0.Draw("same")
            legy1  = TLatex(200,2.0e-38,text["PICASSO"])
            legy1.SetTextAngle(20)
            legy1.SetTextFont(42)
            legy1.SetTextColor(color["PICASSO"])
            legy1.SetTextSize(0.020)
            legy1.Draw("same")
            # Pico60 MET+X
            legy2  = TLatex(8,4e-40,text["Pico60"])
            legy2.SetTextAngle(320)
            legy2.SetTextFont(42)
            legy2.SetTextColor(color["Pico60"])
            legy2.SetTextSize(0.020)
            legy2.Draw("same")
        # SuperK MET+X
            legy3  = TLatex(7,2.0e-39,text["SuperKbb"])
            legy3.SetTextAngle(5)
            legy3.SetTextFont(42)
            legy3.SetTextColor(color["SuperKbb"])
            legy3.SetTextSize(0.020)
            legy3.Draw("same")
        # IceCube MET+X
            legy4  = TLatex(200,1.5e-39,text["IceCubebb"])
            legy4.SetTextAngle(0)
            legy4.SetTextFont(42)
            legy4.SetTextColor(color["IceCubebb"])
            legy4.SetTextSize(0.020)
            legy4.Draw("same")
            legy5  = TLatex(250,5.0e-41,text["IceCubett"])
            legy5.SetTextAngle(0)
            legy5.SetTextFont(42)
            legy5.SetTextColor(color["IceCubett"])
            legy5.SetTextSize(0.020)
            legy5.Draw("same")

            legx6  = TLatex(1.1,2.5e-41,text["monoZ"])
            legx6.SetTextAngle(5)
            legx6.SetTextFont(42)
            legx6.SetTextColor(color["monoZ"])
            legx6.SetTextSize(0.020)
            legx6.Draw("same")
        # SD MET+X monophoton
            legx7  = TLatex(30,2.0e-42,text["monophoton"])
            legx7.SetTextAngle(3)
            legx7.SetTextFont(42)
            legx7.SetTextColor(color["monophoton"])
            legx7.SetTextSize(0.020)
            legx7.Draw("same")
        # SD MET+X monojet
            legx8  = TLatex(30,2.0e-43,text["monojet"])
            legx8.SetTextAngle(2)
            legx8.SetTextFont(42)
            legx8.SetTextColor(color["monojet"])
            legx8.SetTextSize(0.020)
            legx8.Draw("same")
        # SD dijet
            legx9  = TLatex(2,5.0e-43,text["dijet"])
            legx9.SetTextAngle(0)
            legx9.SetTextFont(42)
            legx9.SetTextColor(color["dijet"])
            legx9.SetTextSize(0.020)
            legx9.Draw("same")
        # SD trijet
            legx10  = TLatex(0.02,2.0e-42,text["trijet"])
            legx10.SetTextAngle(45)
            legx10.SetTextFont(42)
            legx10.SetTextColor(color["trijet"])
            legx10.SetTextSize(0.020)
            legx10.Draw("same")


    ############
    ### Draw ###
    ############

    if not DijetOnly:
        C.cd(2).SetPad(0.75,0.0,1.0,1.0)
        C.Update()
        C.cd(1)
        #~ leg.Draw("same")
        C.Update()

    #~ if DDresult == "SI" and not DijetOnly:
        #~ leg3=TLatex(mDM_lb,3e-34,"#bf{CMS} #it{Preliminary}")
        #~ leg3.SetTextFont(42)
        #~ leg3.SetTextSize(0.04)
    #    leg4=TLatex(20,2e-35,"13 fb^{-1} & 27 fb^{-1} & 36 fb^{-1} (13 TeV)")
        #~ leg4=TLatex(30,2e-34,"12.9 fb^{-1} & 35.9 fb^{-1} (13 TeV)")
        #~ leg4.SetTextFont(42)
        #~ leg4.SetTextSize(0.033)
    #~ elif DDresult == "SD" and not DijetOnly:
        #~ leg3=TLatex(mDM_lb,3e-36,"#bf{CMS} #it{Preliminary}")
        #~ leg3.SetTextFont(42)
        #~ leg3.SetTextSize(0.04)
    #    leg4=TLatex(20,2e-37,"13 fb^{-1} & 27 fb^{-1} & 36 fb^{-1} (13 TeV)")
        #~ leg4=TLatex(30,2e-36,"12.9 fb^{-1} & 35.9 fb^{-1} (13 TeV)")
        #~ leg4.SetTextFont(42)
        #~ leg4.SetTextSize(0.033)
    #~ elif DDresult == "SI" and DijetOnly:
    #    leg3=TLatex(600,2e-38,"#bf{CMS}")
        #~ leg3=TLatex(mDM_lb,1.2e-37,"#bf{CMS} #it{Preliminary}")
        #~ leg3.SetTextFont(42)
        #~ leg3.SetTextSize(0.04)
    #    leg4=TLatex(10,3e-36,"#splitline{#bf{Axial-vector med., Dirac DM}}{#it{g_{q} = 0.25, g_{DM} = 1}}")
        #~ leg4=TLatex(70,1.2e-37,"27 fb^{-1} & 36 fb^{-1} (13 TeV)")
        #~ leg4.SetTextFont(42)
        #~ leg4.SetTextSize(0.033)
        #~ leg5=TLatex(15,2.4e-38,"#scale[0.7]{Excluded at 90% CL}")
        #~ leg5.SetTextFont(42)
        #~ leg5.SetTextSize(0.033)
        #~ leg5.Draw("same")
    #~ elif DDresult == "SD" and DijetOnly:
        #~ leg3=TLatex(mDM_lb,1.2e-37,"#bf{CMS} #it{Preliminary}")
        #~ leg3.SetTextFont(42)
        #~ leg3.SetTextSize(0.04)
        #~ leg4=TLatex(70,1.2e-37,"27 fb^{-1} & 36 fb^{-1} (13 TeV)")
        #~ leg4.SetTextFont(42)
        #~ leg4.SetTextSize(0.033)
        #~ leg5=TLatex(10,4e-38,"#scale[0.7]{Excluded at 90% CL}")
        #~ leg5.SetTextFont(42)
        #~ leg5.SetTextSize(0.033)
        #~ leg5.Draw("same")

    #~ leg3.Draw("same")
    #~ leg4.Draw("same")

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
        elif analysis == "LUX" or analysis=="PandaX" or analysis=="CDMSlite" or analysis=="Cresst":
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
    #~ if(DDresult=="SD"):
        #~ texts.append(add_text(0.2,0.45,0.1,0.2,"Spin Dependent"))
    #~ else:
        #~ texts.append(add_text(0.2,0.45,0.1,0.2,"Spin Independent"))
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
