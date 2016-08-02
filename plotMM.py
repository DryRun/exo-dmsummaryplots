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
METXonly  = False
Monotop   = False

#################
### Analyses ####
#################


if Mediator == "Axial": metx = ["monojet","monophoton","monoZ"]
else                  : metx = ["monojet","monophoton","monoZ"]

if Mediator=="Vector" and Monotop : metx+=["monotop"]

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
    filepath["dijet"]      = "Dijet/ScanMM/Dijet_MM_V_2016ICHEP_obs.dat"
    filepath["trijet"]     = "Trijet/ScanMM/Trijet_MM_V_2016ICHEP_obs.dat"
    filepath["monojet"]    = "Monojet/ScanMM/Monojet_V_MM_ICHEP2016_obs.root"
    filepath["monophoton"] = "Monophoton/ScanMM/Monophoton_V_MM_ICHEP2016_obs.root"
    filepath["monoZ"]      = "MonoZll/ScanMM/monoz_vector_gq0p25_cl95_2015.txt"
    filepath["monotop"]    = "Monotop/ScanMM/vector_rebinned.root"
elif Mediator == "Axial":
    filepath["relic"]      = "Relic/relicContour_A_g25.root"
    filepath["dijet"]      = "Dijet/ScanMM/Dijet_MM_A_2016ICHEP_obs.dat"
    filepath["trijet"]     = "Trijet/ScanMM/Trijet_MM_A_2016ICHEP_obs.dat"
    filepath["monojet"]    = "Monojet/ScanMM/Monojet_AV_MM_ICHEP2016_obs.root"
    filepath["monophoton"] = "Monophoton/ScanMM/Monophoton_A_MM_ICHEP2016_obs.root"
    filepath["monoZ"]      = "MonoZll/ScanMM/monoz_axial_gq0p25_cl95_2015.txt"

#####################
### Plot settings ###
#####################

### Planck
linestyle["relic"]      = kDotted
### Met-less
linestyle["dijet"]      = kSolid
linestyle["trijet"]     = kSolid
### MET+X
linestyle["monophoton"] = kSolid
linestyle["monoZ"]      = kSolid
linestyle["monotop"]    = kSolid
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

text["relic"]      = "\Omega_{c} x h^{2} \geq 0.12"
text["dijet"]      = "Dijet obs. [EXO-16-032]"
text["trijet"]     = "Trijet obs. [EXO-16-030]"
text["chi"]        = "chi obs. (exp.excl.)"
text["monojet"]    = "Mono-jet obs. [EXO-16-037]"
text["monoZ"]      = "Mono-Z obs. [EXO-16-010]"
text["monophoton"] = "Mono-\gamma obs. [EXO-16-039]"
text["monotop"]    = "Mono-t (FC) obs. [EXO-16-040]"

####################
### Get datfiles ###
### Get graphs   ###
####################

### to do: make more generic for dat/root formats (if necessary)

for analysis in analyses: 
    if analysis == "relic":
        mylist = TFile(filepath["relic"]).Get("mytlist")
        print "==> Relic list length = ",mylist.GetSize()
        tgraph["relic"] = mylist.At(0)
    elif analysis == "monojet"    : tgraph["monojet"]    = TFile(filepath[analysis]).Get("monojet_obs")
    elif analysis == "monophoton" : tgraph["monophoton"] = TFile(filepath[analysis]).Get("monophoton_obs")
    elif analysis == "monotop"    : tgraph["monotop"]    = TFile(filepath[analysis]).Get("observed")
    else                          : tgraph[analysis]     = TGraph(filepath[analysis])

###################
### Make Canvas ###
### Set ranges  ###
### Add legend  ###
###################

C=TCanvas("C","C",1000,600)
C.cd(1)

tgraph["relic"].SetTitle("CMS Preliminary - EXO DM Summary [ICHEP v1]")
tgraph["relic"].GetXaxis().SetTitle("M_{Med} [GeV]")
tgraph["relic"].GetYaxis().SetTitle("m_{DM} [GeV]")
tgraph["relic"].GetXaxis().SetTitleOffset(1.0)
tgraph["relic"].GetYaxis().SetTitleOffset(1.0)
tgraph["relic"].GetXaxis().SetTitleSize(0.045)
tgraph["relic"].GetYaxis().SetTitleSize(0.045)
if METXonly: 
    tgraph["relic"].GetXaxis().SetRangeUser(0,2000)
    tgraph["relic"].GetYaxis().SetRangeUser(0, 700)
else:        
    tgraph["relic"].GetXaxis().SetRangeUser(0,3800)
    tgraph["relic"].GetYaxis().SetRangeUser(0,1300)
tgraph["relic"].Draw()

if METXonly: leg=C.BuildLegend(0.15,0.60,0.45,0.88)
else:        leg=C.BuildLegend(0.70,0.15,0.88,0.45)
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.Clear()
leg.SetHeader(Mediator+" mediator, Dirac DM (g_{q}=0.25, g_{DM}=1)")

############
### Draw ###
############

for analysis in analyses:
    tgraph[analysis].SetLineColor(color[analysis])
    tgraph[analysis].SetFillColor(color[analysis])
    tgraph[analysis].SetFillStyle(3005)
    tgraph[analysis].SetLineWidth( 404)
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
    leg.AddEntry(tgraph[analysis],text[analysis])
    tgraph[analysis].Draw("same")

leg.Draw()
C.Update()

############
### Save ###
############

if METXonly: C.SaveAs(Mediator+"_METX_Summary_ICHEP.pdf")
else       : C.SaveAs(Mediator+"_EXO_Summary_ICHEP.pdf")

###########
### FIN ###
###########
