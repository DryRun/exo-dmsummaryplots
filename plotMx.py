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

from ROOT import *
import ast

################
### Settings ###
################

DijetOnly = False

DDresult = raw_input('Choose DD [SI or SD]: ')
METless  = ast.literal_eval(raw_input('MET-less? [True or False]: '))
if METless: DijetOnly = ast.literal_eval(raw_input('Dijet only? [True or False]: '))
vFloor  = ast.literal_eval(raw_input('Neutrino floor? [True or False]: '))

#################
### Analyses ####
#################

if   DDresult == "SI": 
    metx    = ["monojet","monophoton","monoZ"]
    metless = ["dijet","trijet"]
elif DDresult == "SD": 
    metx    = ["monojet","monophoton","monoZ"]
    metless = ["dijet","trijet"]

cmsanalyses = metx
if METless  : cmsanalyses = metx+metless
if DijetOnly: cmsanalyses = ["dijet_2016"]

if   DDresult == "SI" and DijetOnly : analyses = cmsanalyses+["Cresst","CDMSlite","PandaX","LUX"]
elif DDresult == "SD" and DijetOnly : analyses = cmsanalyses+["Pico2L","Pico60","SuperK","IceCube"]
elif DDresult == "SI"               : analyses = ["Cresst","CDMSlite","PandaX","LUX"]+cmsanalyses
elif DDresult == "SD"               : analyses = ["Pico2L","Pico60","SuperK","IceCube"]+cmsanalyses

if vFloor: analyses += ["vFloor"]

print "***********************"
print "DD result = ", DDresult
print "List of analyses = ", analyses
print "***********************"

tgraph    = {}
DDgraph   = {}
color     = {}
text      = {}
filepath  = {}
linestyle = {}

############# 
### Files ###
#############

if DDresult == "SI":
    filepath["LUX"]            = "DD/LUX_SI_DMTools_Jul2016.dat"#"DD/lux2015.txt"
    filepath["PandaX"]         = "DD/pandax.txt"                 
    filepath["CDMSlite"]       = "DD/cdmslite2015.txt"
    filepath["Cresst"]         = "DD/cresstii.txt"
    filepath["vFloor"]         = "DD/Neutrino_SI.txt"
    ### ICHEP
    filepath["dijet"]          = "Dijet/ScanMM/MMedMDM_dijet_v_90_Phil500.root"
    ### Dijet paper
    #filepath["dijet_2016"]     = "Dijet/ScanMM/MMedMDM_dijet_v_90_Phil600.root"
    #filepath["dijet_2016_exp"] = "Dijet/ScanMM/MMedMDM_dijet_v_90_Phil600.root"
    filepath["dijet_2016"]     = "Dijet/ScanMM/MMedMDM_dijet_v_90_top56.root"
    filepath["dijet_2016_exp"] = "Dijet/ScanMM/MMedMDM_dijet_v_90_top56.root"    
    filepath["trijet"]         = "Trijet/ScanMM/MMedMDM_v_90.root"
    filepath["monojet"]        = "Monojet/ScanMM/vector_g025_DD.root"
    filepath["monophoton"]     = "Monophoton/ScanMM/Monophoton_SI_MM_ICHEP2016_obs.root"
    #2015: filepath["monoZ"]   = "MonoZll/ScanMM/monoz_vector_gq0p25_cl90_2015.txt"
    filepath["monoZ"]          = "MonoZll/ScanMM/monoz_exo16038_si.txt"
elif DDresult == "SD" :
    filepath["Pico2L"]         = "DD/Pico2L.txt"
    filepath["Pico60"]         = "DD/Pico60.txt"
    filepath["SuperK"]         = "DD/SuperKtautau.txt"
    filepath["IceCube"]        = "DD/IceCubetautau.txt"
    filepath["vFloor"]         = "DD/Neutrino_SD.txt"
    ### ICHEP
    filepath["dijet"]          = "Dijet/ScanMM/MMedMDM_dijet_av_90_Phil500.root"
    ### Dijet paper
    #filepath["dijet_2016"]     = "Dijet/ScanMM/MMedMDM_dijet_av_90_Phil600.root"
    #filepath["dijet_2016_exp"] = "Dijet/ScanMM/MMedMDM_dijet_av_90_Phil600.root"
    filepath["dijet_2016"]     = "Dijet/ScanMM/MMedMDM_dijet_av_90_top56.root"
    filepath["dijet_2016_exp"] = "Dijet/ScanMM/MMedMDM_dijet_av_90_top56.root"
    filepath["trijet"]         = "Trijet/ScanMM/MMedMDM_av_90.root"
    filepath["monojet"]        = "Monojet/ScanMM/axial_g025_DD.root"
    filepath["monophoton"]     = "Monophoton/ScanMM/Monophoton_SD_MM_ICHEP2016_obs.root"
    #2015: filepath["monoZ"]   = "MonoZll/ScanMM/monoz_axial_gq0p25_cl90_2015.txt"
    filepath["monoZ"]          = "MonoZll/ScanMM/monoz_exo16038_sd.txt"

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
linestyle["Pico2L"]     = kSolid
linestyle["Pico60"]     = kSolid
linestyle["SuperK"]     = kDashed
linestyle["IceCube"]    = kDashed
### CMS Met-less
linestyle["dijet"]      = kSolid
linestyle["dijet_2016"] = kSolid
linestyle["trijet"]     = kSolid
### CMS MET+X
linestyle["monophoton"] = kSolid
linestyle["monoZ"]      = kSolid
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
color["Pico2L"]     = kGreen+1
color["Pico60"]     = kGreen+3
color["SuperK"]     = kGreen+2
color["IceCube"]    = kGreen+4
### CMS Met-less
color["dijet"]      = kAzure
color["dijet_2016"] = kAzure
color["trijet"]     = kAzure+1
color["chi"]        = kBlue
### CMS MET+X
color["monojet"]    = kRed+1#kRed+1
color["monophoton"] = kOrange+10#kRed+2
color["monoZ"]      = kOrange-3#kRed+3
color["monotop"]    = kViolet+1

##################
### Plot texts ###
##################

text["vFloor"]     = "v floor (permeable)"
### SI
text["LUX"]        = "LUX"
text["PandaX"]     = "PandaX-II"
text["CDMSlite"]   = "CDMSlite"
text["Cresst"]     = "CRESST-II"
### SD
text["Pico2L"]     = "PICO-2L"
text["Pico60"]     = "PICO-60"
text["SuperK"]     = "Super-K (#tau^{+}#tau^{-})"
text["IceCube"]    = "IceCube (#tau^{+}#tau^{-})"
### CMS MET-less
text["dijet"]      = "Dijet #it{[arxiv:1604.08907] + [EXO-16-032]}"
text["dijet_2016"] = "Dijet #it{[EXO-16-032]}"
text["trijet"]     = "Boosted dijet #it{[EXO-16-030]}"
text["chi"]        = "chi obs. (exp.excl.)"
### CMS MET+X
text["monojet"]    = "DM+j/V_{qq} #it{[EXO-16-037]}"
text["monoZ"]      = "DM+Z_{ll} #it{[EXO-16-038]}"
text["monophoton"] = "DM+#gamma #it{[EXO-16-039]}"
text["monotop"]    = "DM+t (FC) #it{[EXO-16-040]}"

####################
### Get datfiles ###
### Get graphs   ###
####################

for analysis in analyses: 
    if   analysis == "dijet"          : tgraph["dijet"]          = TFile(filepath[analysis]).Get("obs_025")  
    elif analysis == "dijet_2016"     : tgraph["dijet_2016"]     = TFile(filepath[analysis]).Get("obs_025")  
    elif analysis == "dijet_2016_exp" : tgraph["dijet_2016_exp"] = TFile(filepath[analysis]).Get("exp_025")  
    elif analysis == "trijet"         : tgraph["trijet"]         = TFile(filepath[analysis]).Get("obs_025")  
    elif analysis == "monojet"        : tgraph["monojet"]        = TFile(filepath[analysis]).Get("observed")
    elif analysis == "monophoton"     : tgraph["monophoton"]     = TFile(filepath[analysis]).Get("monophoton_obs")
    elif analysis == "monotop"        : tgraph["monotop"]        = TFile(filepath[analysis]).Get("observed")
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
            print "SI - analysis = ", analysis, ", i = ", i, ", mMed = ", mMed, ", mDM = ", mDM
            if analysis == "monophoton":
                DDgraph[analysis].SetPoint(i,pow(10,mMed),pow(10,mDM))        
            elif analysis == "monojet" or analysis == "monoZ":
                DDgraph[analysis]=tgraph[analysis]
            else: 
                mR = Double(0.939*mDM)/(0.939+mDM)
                xsec = Double(c_SI*(mR*mR)/(mMed*mMed*mMed*mMed))
                print "x-sec = ", xsec
                DDgraph[analysis].SetPoint(i,mDM,xsec)        
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
            print "SD - analysis = ", analysis, ", i = ", i, ", mMed = ", mMed, ", mDM = ", mDM
            if analysis == "monophoton":
                DDgraph[analysis].SetPoint(i,pow(10,mMed),pow(10,mDM))        
            elif analysis == "monojet" or analysis == "monoZ":
                DDgraph[analysis]=tgraph[analysis]
            else: 
                mR = Double(0.939*mDM)/(0.939+mDM)
                xsec = Double(c_SD*(mR*mR)/(mMed*mMed*mMed*mMed))
                print "x-sec = ", xsec
                DDgraph[analysis].SetPoint(i,mDM,xsec)        
        tgraph[analysis] = DDgraph[analysis]

###################
### Make Canvas ###
### Add legend  ###
###################

if not DijetOnly:
    C=TCanvas("C","C",1000,600)
    C.Divide(2)
    C.cd(1).SetPad(0.0,0,0.6,1.0)
    C.cd(1).SetLeftMargin(0.15)
else :
    C=TCanvas("C","C",600,600)
    C.Divide(1)
    C.cd(1).SetPad(0.0,0,1.0,1.0)
    C.cd(1).SetLeftMargin(0.15)
    C.cd(1).SetRightMargin(0.05)

C.cd(1).SetLogx()
C.cd(1).SetLogy()

if   DDresult=="SD" and DijetOnly : frame = C.cd(1).DrawFrame(0.1,1e-44,1450,1e-37)
#elif DDresult=="SD"               : frame = C.cd(1).DrawFrame(0.9,1e-45,1450,1e-35) 
elif DDresult=="SD"               : frame = C.cd(1).DrawFrame(0.9,1e-45,1450,1e-37) 
elif DDresult=="SI" and DijetOnly : frame = C.cd(1).DrawFrame(0.1,1e-46,1450,1e-38)
elif DDresult=="SI"               : frame = C.cd(1).DrawFrame(0.9,1e-50,1450,1e-35) 

C.cd(1).SetTickx()
C.cd(1).SetTicky()

frame.SetXTitle("m_{DM} [GeV]")
if   DDresult=="SD": frame.SetYTitle("#sigma^{SD}_{DM-proton} [cm^{2}]")
elif DDresult=="SI": frame.SetYTitle("#sigma^{SI}_{DM-nucleon} [cm^{2}]")
#frame.GetXaxis().SetLabelSize(0.05)
#frame.GetYaxis().SetLabelSize(0.05)
frame.GetXaxis().SetTitleSize(0.045)
frame.GetYaxis().SetTitleSize(0.045)
frame.GetXaxis().SetTitleOffset(1.0)
frame.GetYaxis().SetTitleOffset(1.5)

if not DijetOnly:
    if DDresult == "SI" : leg  = TLatex(1,2.5e-33,"#it{Moriond 2017}")
    if DDresult == "SD" : leg  = TLatex(1,1.8e-35,"#it{Moriond 2017}")
    leg.SetTextFont(42)
    leg.SetTextSize(0.04)
    leg.Draw("same")
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
    leg1=C.BuildLegend(0.60,0.55,0.85,0.85)
    leg1.SetBorderSize(0)
    leg1.SetTextFont(42)
    leg1.Clear()
    if DDresult=="SI":
        leg1.SetHeader("#splitline{#bf{CMS} observed exclusion 90% CL}{Vector med., Dirac DM; g_{q} = 0.25, g_{DM} = 1.0}")
    elif DDresult=="SD":
        leg1.SetHeader("#splitline{#bf{CMS} observed exclusion 90% CL}{Axial-vector med., Dirac DM; g_{q} = 0.25, g_{DM} = 1.0}")
    
    leg2=C.BuildLegend(0.60,0.13,0.85,0.53)
    leg2.SetBorderSize(0)
    leg2.SetTextFont(42)
    leg2.Clear()
    if   DDresult == "SI": leg2.SetHeader("#bf{DD} observed exclusion 90% CL")
    elif DDresult == "SD": leg2.SetHeader("#bf{DD/ID} observed exclusion 90% CL")

    for analysis in analyses:
        if analysis=="dijet" or analysis == "dijet_2016": leg1.AddEntry(tgraph[analysis],"#splitline{CMS dijet}{#it{[EXO-16-032]}}")
        elif analysis == "trijet"     : leg1.AddEntry(tgraph[analysis],"#splitline{CMS boosted dijet}{#it{[EXO-16-030]}}")
        elif analysis == "LUX"        : leg2.AddEntry(tgraph[analysis],"#splitline{"+text[analysis]+"}{#it{[arXiv:1608.07648]}}") #[arXiv:1512.03506]}}")
        elif analysis == "PandaX"     : leg2.AddEntry(tgraph[analysis],"#splitline{"+text[analysis]+"}{#it{[arXiv:1607.07400]}}")
        elif analysis == "CDMSlite"   : leg2.AddEntry(tgraph[analysis],"#splitline{"+text[analysis]+"}{#it{[arXiv:1509.02448]}}")
        elif analysis == "Cresst"     : leg2.AddEntry(tgraph[analysis],"#splitline{"+text[analysis]+"}{#it{[arXiv:1509.01515]}}")
        elif analysis == "Pico2L"     : leg2.AddEntry(tgraph[analysis],"#splitline{"+text[analysis]+"}{#it{[arXiv:1601.03729]}}")
        elif analysis == "Pico60"     : leg2.AddEntry(tgraph[analysis],"#splitline{"+text[analysis]+"}{#it{[arXiv:1510.07754]}}")
        elif analysis == "IceCube"    : leg2.AddEntry(tgraph[analysis],"#splitline{"+text[analysis]+"}{#it{[arXiv:1601.00653]}}")
        elif analysis == "SuperK"     : leg2.AddEntry(tgraph[analysis],"#splitline{"+text[analysis]+"}{#it{[arXiv:1503.04858]}}")
        elif analysis == "monojet"    : leg1.AddEntry(tgraph[analysis],"#splitline{CMS DM+j/V_{qq}}{#it{[EXO-16-037]}}")
        elif analysis == "monoZ"      : leg1.AddEntry(tgraph[analysis],"#splitline{CMS DM+Z_{ll}}{#it{[EXO-16-038]}}")
        elif analysis == "monophoton" : leg1.AddEntry(tgraph[analysis],"#splitline{CMS DM+#gamma}{#it{[EXO-16-039]}}")
        #else                          : leg1.AddEntry(tgraph[analysis],text[analysis])

######################
### Plot SI LEGEND ###
######################

if not DijetOnly and not METless and DDresult=="SI":
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

if DDresult=="SI" and DijetOnly:
    #Cresst Dijet
    legy1 = TLatex(30,1.4e-41,text["Cresst"])
    legy1.SetTextAngle(0)
    legy1.SetTextFont(42)
    legy1.SetTextColor(color["Cresst"])
    legy1.SetTextSize(0.025)
    legy1.Draw("same")
    #CDMS Dijet
    legy2 = TLatex(16,4.0e-42,text["CDMSlite"]+" 2015")
    legy2.SetTextAngle(0)
    legy2.SetTextFont(42)
    legy2.SetTextColor(color["CDMSlite"])
    legy2.SetTextSize(0.025)
    legy2.Draw("same")
    #PandaX Dijet
    legy4 = TLatex(70,1.5e-45,text["PandaX"]+" 2016")
    legy4.SetTextAngle(0)
    legy4.SetTextFont(42)
    legy4.SetTextColor(color["PandaX"])
    legy4.SetTextSize(0.025)
    legy4.Draw("same")
    #LUX Dijet
    legy3 = TLatex(300,3.3e-46,text["LUX"]+" 2016")
    legy3.SetTextAngle(0)
    legy3.SetTextFont(42)
    legy3.SetTextColor(color["LUX"])
    legy3.SetTextSize(0.025)
    legy3.Draw("same")
    #Leg
    legX=C.BuildLegend(0.18,0.15,0.48,0.50)
    legX.SetBorderSize(0)
    legX.SetFillStyle(0)
    legX.SetTextFont(42)
    legX.Clear()
    legX.SetHeader("#bf{Excluded 90% CL}")
    legX.AddEntry(tgraph["dijet_2016"],"#splitline{Vector med., Dirac DM}{#it{g_{q} = 0.25, g_{DM} = 1.0}}")
    legX.AddEntry(tgraph["Cresst"]    ,"#splitline{"+text["Cresst"]+"}{#it{arXiv:1509.01515}}")
    legX.AddEntry(tgraph["CDMSlite"]  ,"#splitline{"+text["CDMSlite"]+"}{#it{arXiv:1509.02448}}")
    legX.AddEntry(tgraph["PandaX"]    ,"#splitline{"+text["PandaX"]+"}{#it{arXiv:1607.07400}}")
    legX.AddEntry(tgraph["LUX"]       ,"#splitline{"+text["LUX"]+"}{#it{arXiv:1608.07648}}")##it{arXiv:1512.03506}}")
    legX.Draw("same")

elif DDresult=="SI":
    # v Floor
    legy0  = TLatex(1.5,3.0e-46,"#splitline{#nu Floor (perm.)}{arXiv/1506.08309}")
    legy0.SetTextAngle(0)
    legy0.SetTextFont(42)
    legy0.SetTextColor(color["vFloor"])
    legy0.SetTextSize(0.025)
    legy0.Draw("same")
    #CDMS MET+X
    legy1 = TLatex(2.2,2.2e-40,text["CDMSlite"])
    legy1.SetTextAngle(3)
    legy1.SetTextFont(42)
    legy1.SetTextColor(color["CDMSlite"])
    legy1.SetTextSize(0.025)
    legy1.Draw("same")
    #Cresst MET+X
    legy2 = TLatex(10,1.5e-41,text["Cresst"])
    legy2.SetTextAngle(5)
    legy2.SetTextFont(42)
    legy2.SetTextColor(color["Cresst"])
    legy2.SetTextSize(0.025)
    legy2.Draw("same")
    #PandaX MET+X
    legy4 = TLatex(85,8e-46,text["PandaX"])
    legy4.SetTextAngle(13)
    legy4.SetTextFont(42)
    legy4.SetTextColor(color["PandaX"])
    legy4.SetTextSize(0.025)
    legy4.Draw("same")
    #LUX MET+X
    legy3 = TLatex(100,8e-47,text["LUX"])
    legy3.SetTextAngle(13)
    legy3.SetTextFont(42)
    legy3.SetTextColor(color["LUX"])
    legy3.SetTextSize(0.025)
    legy3.Draw("same")

###############
### Plot SD ###
###############

if not DijetOnly and not METless and DDresult=="SD":
    # SD MET+X monoZ 
    legx1  = TLatex(3,1e-41,"CMS "+text["monoZ"])
    legx1.SetTextAngle(5)
    legx1.SetTextFont(42)
    legx1.SetTextColor(color["monoZ"])
    legx1.SetTextSize(0.025)
    legx1.Draw("same")
    # SD MET+X monophoton 
    legx2  = TLatex(3,1.6e-42,"CMS "+text["monophoton"])
    legx2.SetTextAngle(3)
    legx2.SetTextFont(42)
    legx2.SetTextColor(color["monophoton"])
    legx2.SetTextSize(0.025)
    legx2.Draw("same")
    # SD MET+X monojet
    legx3  = TLatex(3,4.0e-44,"CMS "+text["monojet"])
    legx3.SetTextAngle(2)
    legx3.SetTextFont(42)
    legx3.SetTextColor(color["monojet"])
    legx3.SetTextSize(0.025)
    legx3.Draw("same")

if DDresult=="SD" and DijetOnly:
    # Pico2L Dijet
    legy1  = TLatex(150,2.7e-39,text["Pico2L"])
    legy1.SetTextAngle(0)
    legy1.SetTextFont(42)
    legy1.SetTextColor(color["Pico2L"])
    legy1.SetTextSize(0.020)
    legy1.Draw("same")
    # Pico60 Dijet
    legy2  = TLatex(210,6.0e-40,text["Pico60"])
    legy2.SetTextAngle(0)
    legy2.SetTextFont(42)
    legy2.SetTextColor(color["Pico60"])
    legy2.SetTextSize(0.020)
    legy2.Draw("same")
    # SuperK Dijet
    legy3  = TLatex(220,1.4e-40,text["SuperK"])
    legy3.SetTextAngle(0)
    legy3.SetTextFont(42)
    legy3.SetTextColor(color["SuperK"])
    legy3.SetTextSize(0.020)
    legy3.Draw("same")
    # IceCube Dijet
    legy4  = TLatex(230,4.7e-41,text["IceCube"])
    legy4.SetTextAngle(0)
    legy4.SetTextFont(42)
    legy4.SetTextColor(color["IceCube"])
    legy4.SetTextSize(0.020)
    legy4.Draw("same")
    #Leg Dijet
    legX=C.BuildLegend(0.18,0.48,0.53,0.865)#50 was 45
    legX.SetBorderSize(0)
    legX.SetFillStyle(0)
    legX.SetTextFont(42)
    legX.Clear()
    legX.SetHeader("#bf{Excluded 90% CL}")
    legX.AddEntry(tgraph["Pico2L"]    ,"#splitline{"+text["Pico2L"]+"}{#it{arXiv:1601.03729}}")
    legX.AddEntry(tgraph["Pico60"]    ,"#splitline{"+text["Pico60"]+"}{#it{arXiv:1510.07754}}")
    legX.AddEntry(tgraph["SuperK"]    ,"#splitline{"+text["SuperK"]+"}{#it{arXiv:1503.04858}}")
    legX.AddEntry(tgraph["IceCube"]   ,"#splitline{"+text["IceCube"]+"}{#it{arXiv:1601.00653}}")
    legX.AddEntry(tgraph["dijet_2016"],"#splitline{Axial-vector med., Dirac DM}{#it{g_{q} = 0.25, g_{DM} = 1.0}}")
    legX.Draw("same")

elif DDresult=="SD":
    # v Floor
    legy0  = TLatex(30,5.0e-45,"#nu Floor (permeable) arXiv/1506.08309")
    legy0.SetTextAngle(10)
    legy0.SetTextFont(42)
    legy0.SetTextColor(color["vFloor"])
    legy0.SetTextSize(0.025)
    legy0.Draw("same")
    # Pico2L MET+X
    legy1  = TLatex(300,3.0e-39,text["Pico2L"])
    legy1.SetTextAngle(15)
    legy1.SetTextFont(42)
    legy1.SetTextColor(color["Pico2L"])
    legy1.SetTextSize(0.025)
    legy1.Draw("same")
    # Pico60 MET+X
    legy2  = TLatex(300,6e-40,text["Pico60"])
    legy2.SetTextAngle(15)
    legy2.SetTextFont(42)
    legy2.SetTextColor(color["Pico60"])
    legy2.SetTextSize(0.025)
    legy2.Draw("same")
    # SuperK MET+X
    legy3  = TLatex(250,1.5e-40,text["SuperK"])
    legy3.SetTextAngle(5)
    legy3.SetTextFont(42)
    legy3.SetTextColor(color["SuperK"])
    legy3.SetTextSize(0.025)
    legy3.Draw("same")
    # IceCube MET+X
    legy4  = TLatex(415,1.07e-41,text["IceCube"])
    legy4.SetTextAngle(14)
    legy4.SetTextFont(42)
    legy4.SetTextColor(color["IceCube"])
    legy4.SetTextSize(0.025)
    legy4.Draw("same")

############
### Draw ###
############

if not DijetOnly:
    C.cd(2).SetPad(0.6,0.0,1.0,1.0)
    C.Update()
    C.cd(1)
    leg.Draw("same")
    C.Update()

if DDresult == "SI" and not DijetOnly:
    leg3=TLatex(100,1.2e-36,"#bf{CMS} #it{Preliminary}")
    leg3.SetTextFont(42)
    leg3.SetTextSize(0.033)
    leg4=TLatex(100,1e-35,"#splitline{#bf{Vector med., Dirac DM}}{#it{g_{q} = 0.25, g_{DM} = 1}}")
    leg4.SetTextFont(42)
    leg4.SetTextSize(0.025)
elif DDresult == "SD" and not DijetOnly:
    leg3=TLatex(100,3e-38,"#bf{CMS} #it{Preliminary}")
    leg3.SetTextFont(42)
    leg3.SetTextSize(0.033)
    leg4=TLatex(70,3e-37,"#splitline{#bf{Axial-vector med., Dirac DM}}{#it{g_{q} = 0.25, g_{DM} = 1}}")
    leg4.SetTextFont(42)
    leg4.SetTextSize(0.025)
elif DDresult == "SI" and DijetOnly:
    leg3=TLatex(100,1.2e-38,"12.9 fb^{-1} (13 TeV)")
    leg3.SetTextFont(42)
    leg3.SetTextSize(0.033)
    leg4=TLatex(30,2e-39,"#splitline{#bf{Vector mediator, Dirac DM}}{#it{g_{q} = 0.25, g_{DM} = 1}}")
    leg4.SetTextFont(42)
    leg4.SetTextSize(0.025)
elif DDresult == "SD" and DijetOnly:
    leg3=TLatex(100,1.2e-37,"12.9 fb^{-1} (13 TeV)")
    leg3.SetTextFont(42)
    leg3.SetTextSize(0.033)
    leg4=TLatex(30,2e-38,"#splitline{#bf{Axial-vector mediator, Dirac DM}}{#it{g_{q} = 0.25, g_{DM} = 1}}")
    leg4.SetTextFont(42)
    leg4.SetTextSize(0.025)

leg3.Draw("same")
#leg4.Draw("same")

C.Update()

####################
### Draw RESULTS ###
####################

for analysis in analyses:
    tgraph[analysis].SetLineColor(color[analysis])
    tgraph[analysis].SetFillColor(color[analysis])
    tgraph[analysis].SetFillStyle(3003)
    tgraph[analysis].SetLineWidth( 102)
    tgraph[analysis].SetLineStyle(linestyle[analysis])
    tgraph[analysis].SetMarkerSize(0.1)
    tgraph[analysis].SetMarkerColor(color[analysis])
    if analysis=="dijet" or analysis == "dijet_2016" or analysis=="trijet":
        tgraph[analysis].SetLineWidth(2)
        tgraph[analysis].Draw("F,same")
        tgraph[analysis].Draw("same")
    elif analysis == "LUX" or analysis=="PandaX" or analysis=="CDMSlite" or analysis=="Cresst":
        tgraph[analysis].SetFillColor(kWhite)
        tgraph[analysis].Draw("same")
    elif analysis == "Pico2L" or analysis=="Pico60" or analysis=="IceCube" or analysis=="SuperK":
        tgraph[analysis].SetFillColor(kWhite)
        tgraph[analysis].Draw("same")
    elif analysis == "monojet" or analysis=="monophoton" or analysis=="monoZ" or analysis=="dijet" or analysis=="dijet_2016":
        tgraph[analysis].Draw("same")
    elif analysis == "vFloor" :
        tgraph[analysis].SetLineWidth(-102)
        tgraph[analysis].Draw("same")

C.Update()

############
### Save ###
############

if DijetOnly : C.SaveAs(DDresult+"_CMSDD_Dijet.pdf")
elif METless : C.SaveAs(DDresult+"_CMSDD_Summary_ICHEP.pdf")
else         : C.SaveAs(DDresult+"_CMSDD_Summary_ICHEP_nodijet.pdf")

###########
### FIN ###
###########
