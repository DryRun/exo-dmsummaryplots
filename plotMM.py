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

################
### Settings ###
################

Mediator  = "Axial"
METXonly  = True

#################
### Analyses ####
#################


if Mediator == "Axial": metx = ["monojet","monophoton","monoZ"]
else                  : metx = ["monojet","monophoton","monoZ"]

if Mediator=="Vector" and METXonly : metx+=["monotop"]

if METXonly: analyses = ["relic"]+metx
else       : analyses = ["relic","dijet","trijet"]+metx

tgraph    = {}
color     = {}
text      = {}
filepath  = {}
linestyle = {}

############# 
### Files ###
#############

if Mediator == "Vector":
    filepath["relic"]      = "Relic/relicContour_V_g25.root"
    filepath["dijet"]      = "Dijet/ScanMM/MMedMDM_dijet_v.root"
    filepath["trijet"]     = "Trijet/ScanMM/MMedMDM_v.root"
    filepath["monojet"]    = "Monojet/ScanMM/Monojet_V_MM_ICHEP2016_obs.root"
    filepath["monophoton"] = "Monophoton/ScanMM/Monophoton_V_MM_ICHEP2016_obs.root"
    #2015: filepath["monoZ"]      = "MonoZll/ScanMM/monoz_vector_gq0p25_cl95_2015.txt"
    filepath["monoZ"]      = "MonoZll/ScanMM/monoz_vector_gq0p25_cl95_2016.txt"
    filepath["monotop"]    = "Monotop/ScanMM/vector_rebinned.root"
elif Mediator == "Axial":
    filepath["relic"]      = "Relic/relicContour_A_g25.root"
    filepath["dijet"]      = "Dijet/ScanMM/MMedMDM_dijet_av.root"
    filepath["trijet"]     = "Trijet/ScanMM/MMedMDM_av.root"
    filepath["monojet"]    = "Monojet/ScanMM/Monojet_AV_MM_ICHEP2016_obs.root"
    filepath["monophoton"] = "Monophoton/ScanMM/Monophoton_A_MM_ICHEP2016_obs.root"
    #2015: filepath["monoZ"]      = "MonoZll/ScanMM/monoz_axial_gq0p25_cl95_2015.txt"
    filepath["monoZ"]      = "MonoZll/ScanMM/monoz_axial_gq0p25_cl95_2016.txt"

###################
### Plot colors ###
###################

### Planck
linestyle["relic"]      = kDotted
### Met-less
linestyle["dijet"]      = kSolid
linestyle["trijet"]     = kSolid
### MET+X
linestyle["monophoton"] = kSolid
linestyle["monoZ"]      = kSolid
linestyle["monotop"]    = kDashed
### dummies dashed
linestyle["monojet"]    = kSolid

### Planck
color["relic"]      = kGray
### Met-less
color["dijet"]      = kAzure
color["trijet"]     = kAzure+1
color["chi"]        = kBlue
### MET+X
color["monojet"]    = kRed+1#kRed+1
color["monophoton"] = kOrange+10#kRed+2
color["monoZ"]      = kOrange-3#kRed+3
color["monotop"]    = kViolet+1

##################
### Plot texts ###
##################

if not METXonly:
    text["relic"]      = "\Omega_{c} h^{2} \geq 0.12"
    text["dijet"]      = "#splitline{Dijet #it{[EXO-16-032]}}{+ #it{[arXiv:1604.08907]}}"
    text["trijet"]     = "#splitline{Boosted dijet}{#it{[EXO-16-030]}}"
    text["chi"]        = "chi obs. (exp.excl.)"
    text["monojet"]    = "#splitline{DM + j/V_{qq}}{#it{[EXO-16-037]}}"
    text["monoZ"]      = "#splitline{DM + Z_{ll}}{#it{[EXO-16-038]}}"
    text["monophoton"] = "#splitline{DM + #gamma}{#it{[EXO-16-039]}}"
    text["monotop"]    = "#splitline{DM + t (100% FC)}{#it{[EXO-16-040]}}"
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
### Get datfiles ###
### Get graphs   ###
####################

for analysis in analyses: 
    if analysis == "relic":
        mylist = TFile(filepath["relic"]).Get("mytlist")
        print "==> Relic list length = ",mylist.GetSize()
        tgraph["relic"] = mylist.At(0)
    elif analysis == "dijet"      : tgraph["dijet"]      = TFile(filepath[analysis]).Get("obs_025")  
    elif analysis == "trijet"     : tgraph["trijet"]     = TFile(filepath[analysis]).Get("obs_025")  
    elif analysis == "monojet"    : tgraph["monojet"]    = TFile(filepath[analysis]).Get("monojet_obs")
    elif analysis == "monophoton" : tgraph["monophoton"] = TFile(filepath[analysis]).Get("monophoton_obs")
    #2015: elif analysis == "monoZ"      : tgraph["monoZ"]      = TFile(filepath[analysis]).Get("monoz_obs")
    elif analysis == "monotop"    : tgraph["monotop"]    = TFile(filepath[analysis]).Get("observed")
    else                          : tgraph[analysis]     = TGraph(filepath[analysis])

###################
### Make Canvas ###
### Set ranges  ###
### Add legend  ###
###################

C=TCanvas("C","C",1000,600)
C.cd(1)

tgraph["relic"].SetTitle("")
tgraph["relic"].GetXaxis().SetTitle("M_{Med} [GeV]")
tgraph["relic"].GetYaxis().SetTitle("m_{DM} [GeV]")
tgraph["relic"].GetXaxis().SetTitleOffset(1.0)
tgraph["relic"].GetYaxis().SetTitleOffset(1.0)
tgraph["relic"].GetXaxis().SetTitleSize(0.045)
tgraph["relic"].GetYaxis().SetTitleSize(0.045)
if METXonly: 
    tgraph["relic"].GetXaxis().SetRangeUser(0,2000)
    tgraph["relic"].GetYaxis().SetRangeUser(0, 780)
else:        
    tgraph["relic"].GetXaxis().SetRangeUser(0,4500)
    tgraph["relic"].GetYaxis().SetRangeUser(0,1300)
tgraph["relic"].Draw()

##############
### Legend ###
##############

f1 = TF1("f1","x/2.",0,4000)
g1 = TGraph(f1)
g1.SetLineColor(kGray)
g1.SetLineStyle(kDashed)

if  not METXonly:
    g1.Draw("same")
    legd=TLatex(1600,740,"M_{Med} = 2 x m_{DM}")
    legd.SetTextAngle(45)
    legd.SetTextFont(42)
    legd.SetTextSize(0.025)
    legd.SetTextColor(kGray)
    legd.Draw("same")


if METXonly: leg=C.BuildLegend(0.15,0.55,0.45,0.88)
else:        leg=C.BuildLegend(0.67,0.12,0.89,0.57)

leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.SetFillColor(0)
leg.Clear()
leg.SetHeader("#bf{Observed exclusion 95% CL}")

##################
### Relic text ###
##################

if Mediator=="Vector" and not METXonly:
    legw=TLatex(3950,900,"#Omega_{c} h^{2} #geq 0.12")
    legw.SetTextAngle(40)
elif Mediator=="Axial" and not METXonly:
    legw  = TLatex(1720,1150,"#Omega_{c} h^{2} #geq 0.12")
    legw.SetTextAngle(40)
    legw2 = TLatex(3020,1150,"#Omega_{c} h^{2} #geq 0.12")
    legw2.SetTextFont(42)
    legw2.SetTextColor(color["relic"])
    legw2.SetTextAngle(40)
    legw2.SetTextSize(0.02)
    legw2.Draw("same")
elif Mediator=="Vector" and METXonly:
    legw=TLatex(1600,160,"#Omega_{c} h^{2} #geq 0.12")
    legw.SetTextAngle(16)
elif Mediator=="Axial" and METXonly:
    legw=TLatex(1750,600,"#Omega_{c} h^{2} #geq 0.12")
    legw.SetTextAngle(35)
legw.SetTextFont(42)
legw.SetTextSize(0.02)
legw.SetTextColor(color["relic"])

legw.Draw("same")

##################
### Model text ###
##################

if Mediator=="Vector" and not METXonly:
    leg1=TLatex(2770,1100,"#splitline{#bf{"+Mediator+" mediator, Dirac DM}}{        #it{g_{q} = 0.25, g_{DM} = 1}}")
elif Mediator=="Axial" and not METXonly:
    leg1=TLatex(3000,1000,"#splitline{#bf{"+Mediator+"-vector mediator, Dirac DM}}{          #it{g_{q} = 0.25, g_{DM} = 1}}")
elif Mediator=="Vector" and METXonly:
    leg1=TLatex(1105,710,"#splitline{#bf{"+Mediator+" mediator, Dirac DM}}{#it{g_{q} = 0.25, g_{DM} = 1}}")
elif Mediator=="Axial" and METXonly:
    leg1=TLatex(1105,705,"#splitline{#bf{"+Mediator+"-vector mediator, Dirac DM}}{#it{g_{q} = 0.25, g_{DM} = 1}}")
leg1.SetTextFont(42)
leg1.SetTextSize(0.030)

##############
### Legend ###
##############

leg2=C.BuildLegend(0.10,0.905,0.90,0.955)
leg2.SetBorderSize(0)
leg2.SetTextFont(42)
leg2.SetFillColor(0)
leg2.Clear()
leg2.SetHeader("#bf{CMS} #it{Preliminary}")

leg3=C.BuildLegend(0.52,0.905,1.32,0.955)
leg3.SetBorderSize(0)
leg3.SetTextFont(42)
leg3.SetFillColor(0)
leg3.Clear()
leg3.SetHeader("#bf{Dark Matter Summary} #it{ICHEP 2016}")

############
### Draw ###
############

for analysis in analyses:
    if not  analysis=="relic":
        leg.AddEntry(tgraph[analysis],text[analysis])

leg.Draw("same")

for analysis in analyses:
    tgraph[analysis].SetLineColor(color[analysis])
    tgraph[analysis].SetMarkerSize(0.1)
    tgraph[analysis].SetMarkerColor(color[analysis])
    tgraph[analysis].SetFillColor(color[analysis])
    tgraph[analysis].SetFillStyle(3005)
    tgraph[analysis].SetLineWidth( 203)
    tgraph[analysis].SetLineStyle(linestyle[analysis])
    if analysis == "relic":
        for i in range(0,mylist.GetSize()):
            tgraph["relic"] = mylist.At(i)
            tgraph["relic"].SetLineColor(color[analysis])
            tgraph["relic"].SetFillColor(color[analysis])
            tgraph["relic"].SetLineStyle(linestyle[analysis])
            tgraph["relic"].SetLineWidth(-404)
            tgraph["relic"].SetFillStyle(3005)
            tgraph["relic"].Draw("same")
    elif analysis == "chi":
        tgraph[analysis].SetLineWidth(-404)
    tgraph[analysis].Draw("same")

leg1.Draw("same")
leg2.Draw("same")
leg3.Draw("same")
C.Update()

############
### Save ###
############

if METXonly: C.SaveAs(Mediator+"_METX_Summary_ICHEP.pdf")
else       : C.SaveAs(Mediator+"_EXO_Summary_ICHEP.pdf")

###########
### FIN ###
###########
