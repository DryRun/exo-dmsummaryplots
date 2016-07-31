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

#################
### Analyses ####
#################

metx = ["monojet","monophoton","monoZ"]
analyses = ["relic"]+metx
if not METXonly: analyses = ["relic","dijet"]+metx

tgraph    = {}
color     = {}
text      = {}
filepath  = {}
linestyle = {}

############# 
### Files ###
#############

if Mediator == "Vector":
    filepath["dijet"]      = "Dijet/ScanMM/Dijet_MM_V_2016ICHEP_obs.dat"
    filepath["monophoton"] = "Monophoton/ScanMM/monophoton_dummy.dat"
    filepath["relic"]      = "Relic/relicContour_V_g25.root"
    filepath["monojet"]    = "Monojet/ScanMM/monojet_dummy.dat"
    filepath["monoZ"]      = "MonoZll/ScanMM/monoz_vector_gq0p25_cl95_2015.txt"
elif Mediator == "Axial":
    filepath["dijet"]      = "Dijet/ScanMM/Dijet_MM_A_2016ICHEP_obs.dat"
    filepath["monophoton"] = "Monophoton/ScanMM/monophoton_dummy.dat"
    filepath["relic"]      = "Relic/relicContour_A_g25.root"
    filepath["monojet"]    = "Monojet/ScanMM/monojet_dummy.dat"
    filepath["monoZ"]      = "MonoZll/ScanMM/monoz_axial_gq0p25_cl95_2015.txt"

#####################
### Plot settings ###
#####################

linestyle["relic"]      = kDotted
linestyle["dijet"]      = kSolid
linestyle["monoZ"]      = kSolid
### dummies dashed
linestyle["monojet"]    = kDashed
linestyle["monophoton"] = kDashed

color["monojet"]    = kRed
color["monophoton"] = kOrange
color["monoZ"]      = kYellow
color["relic"]      = kGray
color["chi"]        = kBlack
color["dijet"]      = kBlue

text["monojet"]    = "Mono-jet [DUMMY - EXO-16-037]"
text["monoZ"]      = "Mono-Z [EXO-16-038]"
text["monophoton"] = "Mono-\gamma  [DUMMY - EXO-16-039]"
text["relic"]      = "\Omega_{c} x h^{2} \geq 0.12"
text["chi"]        = "chi (exp.excl.)"
text["dijet"]      = "Dijet [EXO-16-032]"

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
    else :
        tgraph[analysis] = TGraph(filepath[analysis])

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
    tgraph["relic"].GetXaxis().SetRangeUser(0,4000)
    tgraph["relic"].GetYaxis().SetRangeUser(0,1200)
tgraph["relic"].Draw()

if METXonly: leg=C.BuildLegend(0.15,0.60,0.40,0.88)
else:        leg=C.BuildLegend(0.63,0.15,0.90,0.45)
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.Clear()
leg.SetHeader(Mediator+" (g_{q}=0.25, g_{DM}=1) obs.excl.95%CL")

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
