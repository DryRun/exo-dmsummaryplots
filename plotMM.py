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

#################################
### Parameters to be modified ###
#################################

Mediator  = raw_input('Choose mediator [Vector or Axial]: ')
METXonly  = ast.literal_eval(raw_input('MET+X only? [True or False]: '))
DijetOnly = ast.literal_eval(raw_input('Dijet only? [True or False]: '))

logx      = ast.literal_eval(raw_input('Log x? '))

CL = "95"

#################
### Analyses ####
#################

if Mediator == "Axial": metx = ["monojet","monophoton","monoZ"]
else                  : metx = ["monojet","monophoton","monoZ"]

if Mediator=="Vector" and METXonly : metx+=["monotop"]

if   METXonly  : analyses = ["relic"]+metx
elif DijetOnly : analyses = ["relic","dijet_2016","dijet_2016_exp"]
else           : analyses = ["relic","dijet","trijet"]+metx

tgraph    = {}
color     = {}
text      = {}
filepath  = {}
linestyle = {}

############# 
### Files ###
#############

if Mediator == "Vector":
    filepath["relic"]          = "Relic/relicContour_V_g25.root"
    #ICHEP
    filepath["dijet"]          = "Dijet/ScanMM/MMedMDM_dijet_v_Phil500.root"
    #Dijet paper
    #filepath["dijet_2016"]     = "Dijet/ScanMM/MMedMDM_dijet_v_Phil600.root"
    #filepath["dijet_2016_exp"] = "Dijet/ScanMM/MMedMDM_dijet_v_Phil600.root"
    #95
    if CL=="95":
        filepath["dijet_2016"]     = "Dijet/ScanMM/MMedMDM_dijet_v_top56.root"
        filepath["dijet_2016_exp"] = "Dijet/ScanMM/MMedMDM_dijet_v_top56.root"
    elif CL=="90":
        filepath["dijet_2016"]     = "Dijet/ScanMM/MMedMDM_dijet_v_90_top56.root"
        filepath["dijet_2016_exp"] = "Dijet/ScanMM/MMedMDM_dijet_v_90_top56.root"
    #
    #filepath["dijet_2016"]     = "Dijet/ScanMM/Dijet_MM_V_Dijetpaper2016_obs.txt"
    #filepath["dijet_2016_exp"] = "Dijet/ScanMM/Dijet_MM_V_Dijetpaper2016_exp.txt"
    filepath["trijet"]         = "Trijet/ScanMM/MMedMDM_v.root"
    filepath["monojet"]        = "Monojet/ScanMM/Monojet_V_MM_ICHEP2016_obs.root"
    filepath["monophoton"]     = "Monophoton/ScanMM/Monophoton_V_MM_ICHEP2016_obs.root"
    #2015: filepath["monoZ"]      = "MonoZll/ScanMM/monoz_vector_gq0p25_cl95_2015.txt"
    filepath["monoZ"]          = "MonoZll/ScanMM/monoz_vector_gq0p25_cl95_2016.txt"
    filepath["monotop"]        = "Monotop/ScanMM/vector_rebinned.root"
elif Mediator == "Axial":
    filepath["relic"]          = "Relic/relicContour_A_g25.root"
    #ICHEP
    filepath["dijet"]          = "Dijet/ScanMM/MMedMDM_dijet_av_Phil500.root"
    #Dijet paper
    #filepath["dijet_2016"]     = "Dijet/ScanMM/MMedMDM_dijet_av_Phil600.root"
    #filepath["dijet_2016_exp"] = "Dijet/ScanMM/MMedMDM_dijet_av_Phil600.root"
    #95
    if CL=="95":
        filepath["dijet_2016"]     = "Dijet/ScanMM/MMedMDM_dijet_av_top56.root"
        filepath["dijet_2016_exp"] = "Dijet/ScanMM/MMedMDM_dijet_av_top56.root"
    elif CL=="90":
        filepath["dijet_2016"]     = "Dijet/ScanMM/MMedMDM_dijet_av_90_top56.root"
        filepath["dijet_2016_exp"] = "Dijet/ScanMM/MMedMDM_dijet_av_90_top56.root"
    #Dijet paper?
    #filepath["dijet_2016"]     = "Dijet/ScanMM/Dijet_MM_A_Dijetpaper2016_obs.txt"
    #filepath["dijet_2016_exp"] = "Dijet/ScanMM/Dijet_MM_A_Dijetpaper2016_exp.txt"
    filepath["trijet"]         = "Trijet/ScanMM/MMedMDM_av.root"
    filepath["monojet"]        = "Monojet/ScanMM/Monojet_AV_MM_ICHEP2016_obs.root"
    filepath["monophoton"]     = "Monophoton/ScanMM/Monophoton_A_MM_ICHEP2016_obs.root"
    #2015: filepath["monoZ"]      = "MonoZll/ScanMM/monoz_axial_gq0p25_cl95_2015.txt"
    filepath["monoZ"]          = "MonoZll/ScanMM/monoz_axial_gq0p25_cl95_2016.txt"

###################
### Plot colors ###
###################

### Planck
linestyle["relic"]          = kDotted#was dotted
### Met-less
linestyle["dijet"]          = kSolid
linestyle["dijet_2016"]     = kSolid
linestyle["dijet_2016_exp"] = kDashed
linestyle["trijet"]         = kSolid
### MET+X
linestyle["monophoton"]     = kSolid
linestyle["monoZ"]          = kSolid
linestyle["monotop"]        = kDashed
### dummies dashed
linestyle["monojet"]        = kSolid

### Planck
color["relic"]          = kGray+2
### Met-less
color["dijet"]          = kAzure
color["dijet_2016"]     = kAzure
color["dijet_2016_exp"] = kAzure+1
color["trijet"]         = kAzure+1
color["chi"]            = kBlue
### MET+X
color["monojet"]        = kRed+1#kRed+1
color["monophoton"]     = kOrange+10#kRed+2
color["monoZ"]          = kOrange-3#kRed+3
color["monotop"]        = kViolet+1

##################
### Plot texts ###
##################

if not METXonly:
    text["relic"]          = "\Omega_{c} h^{2} \geq 0.12"
    text["dijet"]          = "#splitline{Dijet #it{[EXO-16-032]}}{+ #it{[arXiv:1604.08907]}}"
    text["dijet_2016"]     = "Observed"
    text["dijet_2016_exp"] = "Expected"
    text["trijet"]         = "#splitline{Boosted dijet}{#it{[EXO-16-030]}}"
    text["chi"]            = "chi obs. (exp.excl.)"
    text["monojet"]        = "#splitline{DM + j/V_{qq}}{#it{[EXO-16-037]}}"
    text["monoZ"]          = "#splitline{DM + Z_{ll}}{#it{[EXO-16-038]}}"
    text["monophoton"]     = "#splitline{DM + #gamma}{#it{[EXO-16-039]}}"
    text["monotop"]        = "#splitline{DM + t (100% FC)}{#it{[EXO-16-040]}}"
else:
    text["relic"]      = "\Omega_{c} h^{2} \geq 0.12"
    text["dijet"]      = "Dijet #it{[EXO-16-032]}+ #it{[arXiv:1604.08907]}"
    text["trijet"]     = "Boosted dijet #it{[EXO-16-030]}}"
    text["chi"]        = "chi obs. (exp.excl.)"
    text["monojet"]    = "DM + j/V_{qq} #it{[EXO-16-037]}"
    text["monoZ"]      = "DM + Z_{ll} #it{[EXO-16-038]}"
    text["monophoton"] = "DM + #gamma #it{[EXO-16-039]}"
    text["monotop"]    = "DM + t (100% FC) #it{[EXO-16-040]}"

####################
### Get graphs   ###
####################

for analysis in analyses: 
    if analysis == "relic":
        mylist = TFile(filepath["relic"]).Get("mytlist")
        print "==> Relic list length = ",mylist.GetSize()
        tgraph["relic"] = mylist.At(0)
    #ichep
    elif analysis == "dijet"          : tgraph["dijet"]          = TFile(filepath[analysis]).Get("obs_025")  
    #dijet paper
    elif analysis == "dijet_2016"     : tgraph["dijet_2016"]     = TFile(filepath[analysis]).Get("obs_025")  
    elif analysis == "dijet_2016_exp" : tgraph["dijet_2016_exp"] = TFile(filepath[analysis]).Get("exp_025")  
    elif analysis == "trijet"         : tgraph["trijet"]         = TFile(filepath[analysis]).Get("obs_025")  
    elif analysis == "monojet"        : tgraph["monojet"]        = TFile(filepath[analysis]).Get("monojet_obs")
    elif analysis == "monophoton"     : tgraph["monophoton"]     = TFile(filepath[analysis]).Get("monophoton_obs")
    #2015: elif analysis == "monoZ"   : tgraph["monoZ"]          = TFile(filepath[analysis]).Get("monoz_obs")
    elif analysis == "monotop"        : tgraph["monotop"]        = TFile(filepath[analysis]).Get("observed")
    else                              : tgraph[analysis]         = TGraph(filepath[analysis])

###################
### Make Canvas ###
### Set ranges  ###
###################

C=TCanvas("C","C",1000,600)
C.cd(1)

C.cd(1).SetTickx()
C.cd(1).SetTicky()

if logx       : frame = C.cd(1).DrawFrame(90,0,3700, 1450)
elif METXonly : frame = C.cd(1).DrawFrame(0,0,2000, 780)
else          : frame = C.cd(1).DrawFrame(0,0,3700,1450) 

if logx : C.cd(1).SetLogx()

frame.SetXTitle("M_{Med} [GeV]")
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
elif METXonly : leg=C.BuildLegend(0.15,0.55,0.45,0.88)
#elif DijetOnly: leg=C.BuildLegend(0.65,0.12,0.87,0.37)
elif DijetOnly: leg=C.BuildLegend(0.69,0.12,0.91,0.37)
else:           leg=C.BuildLegend(0.67,0.12,0.89,0.57)

leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.Clear()
if DijetOnly: leg.SetHeader("#bf{Dijet "+CL+"% CL}")
else        : leg.SetHeader("#bf{Observed exclusion 95% CL}")

####################
### Add diagonal ###
####################

f1 = TF1("f1","x/2.",0,4000)
g1 = TGraph(f1)
g1.SetLineColor(color["relic"]-1)
g1.SetLineStyle(kDashed)

if DijetOnly:
    g1.Draw("same")
    legd=TLatex(1300,680,"M_{Med} = 2 x m_{DM}")
    legd.SetTextAngle(38)
    legd.SetTextFont(42)
    legd.SetTextSize(0.040)
    legd.SetTextColor(color["relic"])
    legd.Draw("same")
elif not METXonly:
    g1.Draw("same")
    legd=TLatex(1600,740,"M_{Med} = 2 x m_{DM}")
    legd.SetTextAngle(45)
    legd.SetTextFont(42)
    legd.SetTextSize(0.040)
    legd.SetTextColor(color["relic"])
    legd.Draw("same")

##################
### Relic text ###
##################

if Mediator=="Vector" and DijetOnly:
    legw=TLatex(3000,540,"#Omega_{c} h^{2} #geq 0.12")
    legw.SetTextAngle(30)
    legw.SetTextSize(0.04)
elif Mediator=="Vector" and not METXonly:
    legw=TLatex(3950,900,"#Omega_{c} h^{2} #geq 0.12")
    legw.SetTextAngle(40)
    legw.SetTextSize(0.03)
elif Mediator=="Axial" and DijetOnly:
    legw  = TLatex(1570,1070,"#Omega_{c} h^{2} #geq 0.12")
    legw.SetTextAngle(34)
    legw2 = TLatex(2900,1070,"#Omega_{c} h^{2} #geq 0.12")
    legw2.SetTextFont(42)
    legw2.SetTextColor(color["relic"])
    legw2.SetTextAngle(34)
    legw.SetTextSize(0.04)
    legw2.SetTextSize(0.04)
    legw2.Draw("same")
elif Mediator=="Axial" and not METXonly:
    legw  = TLatex(1720,1150,"#Omega_{c} h^{2} #geq 0.12")
    legw.SetTextAngle(40)
    legw2 = TLatex(3020,1150,"#Omega_{c} h^{2} #geq 0.12")
    legw2.SetTextFont(42)
    legw2.SetTextColor(color["relic"])
    legw2.SetTextAngle(40)
    legw2.SetTextSize(0.02)
    legw2.Draw("same")
    legw.SetTextSize(0.03)
elif Mediator=="Vector" and METXonly:
    legw=TLatex(1600,160,"#Omega_{c} h^{2} #geq 0.12")
    legw.SetTextAngle(16)
    legw.SetTextSize(0.03)
elif Mediator=="Axial" and METXonly:
    legw=TLatex(1750,600,"#Omega_{c} h^{2} #geq 0.12")
    legw.SetTextSize(0.03)
    legw.SetTextAngle(35)
legw.SetTextFont(42)
legw.SetTextColor(color["relic"])

##################
### Model text ###
##################

if logx:
    leg1=TLatex(250,1300,"#splitline{#bf{"+Mediator+" mediator}}{#bf{Dirac DM}}")
    leg1.SetTextFont(42)
    leg1.SetTextSize(0.030)
    leg4=TLatex(250,1200,"#it{g_{q} = 0.25, g_{DM} = 1}")
    leg4.SetTextFont(42)
    leg4.SetTextSize(0.030)
    leg4.Draw("same")
elif Mediator=="Vector" and DijetOnly:
    leg1=TLatex(2750,1120,"#splitline{#bf{Vector mediator}}{#bf{&}}")
    leg5=TLatex(2750,1000,"#bf{Dirac DM}")
    leg4=TLatex(2750, 850,"#splitline{#it{g_{q} = 0.25}}{#it{g_{DM} = 1.0}}")
    leg1.SetTextFont(42)
    leg4.SetTextFont(42)
    leg5.SetTextFont(42)
    leg1.SetTextSize(0.040)
    leg4.SetTextSize(0.040)
    leg5.SetTextSize(0.040)
    leg4.Draw("same")
    leg5.Draw("same")
elif Mediator=="Axial" and DijetOnly:
    leg1=TLatex(2750, 920,"#splitline{#bf{"+Mediator+"-vector}}{#bf{mediator &}}")
    leg5=TLatex(2750, 800,"#bf{Dirac DM}")
    leg4=TLatex(2750, 650,"#splitline{#it{g_{q} = 0.25}}{#it{g_{DM} = 1.0}}")
    leg1.SetTextFont(42)
    leg4.SetTextFont(42)
    leg5.SetTextFont(42)
    leg1.SetTextSize(0.040)
    leg4.SetTextSize(0.040)
    leg5.SetTextSize(0.040)
    leg4.Draw("same")
    leg5.Draw("same")
elif Mediator=="Vector" and not METXonly:
    leg1=TLatex(2770,1100,"#splitline{#bf{"+Mediator+" mediator, Dirac DM}}{        #it{g_{q} = 0.25, g_{DM} = 1}}")
    leg1.SetTextFont(42)
    leg1.SetTextSize(0.030)
elif Mediator=="Axial" and not METXonly:
    leg1=TLatex(3000,1000,"#splitline{#bf{"+Mediator+"-vector mediator, Dirac DM}}{          #it{g_{q} = 0.25, g_{DM} = 1}}")
    leg1.SetTextFont(42)
    leg1.SetTextSize(0.030)
elif Mediator=="Vector" and METXonly:
    leg1=TLatex(1105,710,"#splitline{#bf{"+Mediator+" mediator, Dirac DM}}{#it{g_{q} = 0.25, g_{DM} = 1}}")
    leg1.SetTextFont(42)
    leg1.SetTextSize(0.030)
elif Mediator=="Axial" and METXonly:
    leg1=TLatex(1105,705,"#splitline{#bf{"+Mediator+"-vector mediator, Dirac DM}}{#it{g_{q} = 0.25, g_{DM} = 1}}")
    leg1.SetTextFont(42)
    leg1.SetTextSize(0.030)

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
elif DijetOnly : 
    # CMS
    leg2=TLatex(100,1470,"#bf{CMS}")
    leg2.SetTextFont(42)
    leg2.SetTextSize(0.045)
    # lumi
    leg3=TLatex(2750,1470,"12.9 fb^{-1} (13 TeV)")
    leg3.SetTextFont(42)
    leg3.SetTextSize(0.045)
#elif Mediator=="Vector" and DijetOnly : 
#    # CMS
#    leg2=TLatex(100,1470,"#bf{CMS}")
#    leg2.SetTextFont(42)
#    leg2.SetTextSize(0.045)
#    # lumi
#    leg3=TLatex(2550,1470,"12.9 fb^{-1} (13 TeV)")
#    leg3.SetTextFont(42)
#    leg3.SetTextSize(0.045)
else         : 
    # CMS
    leg2=TLatex(100,1470,"#bf{CMS} #it{Preliminary}")
    leg2.SetTextFont(42)
    leg2.SetTextSize(0.045)
    # lumi
    leg3=TLatex(2800,1470,"#bf{Dark Matter Summary} #it{ICHEP 2016}")
    leg3.SetTextFont(42)
    leg3.SetTextSize(0.033)

############
### Draw ###
############

for analysis in analyses:
    if not  analysis=="relic":
        leg.AddEntry(tgraph[analysis],text[analysis])

for analysis in analyses:
    tgraph[analysis].SetLineColor(color[analysis])
    tgraph[analysis].SetMarkerSize(0.1)
    tgraph[analysis].SetMarkerColor(color[analysis])
    tgraph[analysis].SetFillColor(color[analysis])
    tgraph[analysis].SetFillStyle(3005)
    tgraph[analysis].SetLineWidth( 202)
    tgraph[analysis].SetLineStyle(linestyle[analysis])
    if analysis == "relic":
        for i in range(0,mylist.GetSize()):
            tgraph["relic"] = mylist.At(i)
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
leg1.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
legw.Draw("same")

C.Update()

############
### Save ###
############

if METXonly    : C.SaveAs(Mediator+"_METX_Summary_ICHEP.pdf")
elif DijetOnly : C.SaveAs(Mediator+"_Dijet_DM.pdf")
else           : C.SaveAs(Mediator+"_EXO_Summary_ICHEP.pdf")

###########
### FIN ###
###########
