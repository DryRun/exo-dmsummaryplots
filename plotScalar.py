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

Mediator  = "Pseudo"

ObsOnly = False

#################
### Analyses ####
#################

analyses = ["BSM",
            "monojet_obs",
            "DMtt_obs",
            "METbb_DMtt_obs",
            "METbb_DMbb_obs"
            #,"METbb_DMhf_obs"
            ]

if not ObsOnly: analyses=["BSM",
                          "monojet_obs",   "monojet_exp",
                          "DMtt_obs",      "DMtt_exp",
                          #"METbb_DMtt_exp","METbb_DMtt_obs",
                          "METbb_DMbb_obs","METbb_DMbb_exp"
                          #"METbb_DMhf_exp","METbb_DMhf_obs",
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
    filepath["monojet_obs"]    = "Monojet/ScanMM/limit_1D_scalar.root"
    filepath["monojet_exp"]    = "Monojet/ScanMM/limit_1D_scalar.root"
    filepath["DMtt_obs"]       = "DMtt/DMtt_Scalar_ICHEP2016_Mx_obs.txt"
    filepath["DMtt_exp"]       = "DMtt/DMtt_Scalar_ICHEP2016_Mx_exp.txt"
    filepath["METbb_DMtt_obs"] = "DMbb/2015/Limits_hfDMs.root"
    filepath["METbb_DMbb_obs"] = "DMbb/2015/Limits_hfDMs.root"
    filepath["METbb_DMhf_obs"] = "DMbb/2015/Limits_hfDMs.root"
    filepath["METbb_DMtt_exp"] = "DMbb/2015/Limits_hfDMs.root"
    filepath["METbb_DMbb_exp"] = "DMbb/2015/Limits_hfDMs.root"
    filepath["METbb_DMhf_exp"] = "DMbb/2015/Limits_hfDMs.root"
if Mediator == "Pseudo":
    filepath["monojet_obs"]    = "Monojet/ScanMM/limit_1D_ps.root"
    filepath["monojet_exp"]    = "Monojet/ScanMM/limit_1D_ps.root"
    filepath["DMtt_obs"]       = "DMtt/DMtt_Pseudo_ICHEP2016_Mx_obs.txt"
    filepath["DMtt_exp"]       = "DMtt/DMtt_Pseudo_ICHEP2016_Mx_exp.txt"
    filepath["METbb_DMtt_obs"] = "DMbb/2015/Limits_hfDMps.root"
    filepath["METbb_DMbb_obs"] = "DMbb/2015/Limits_hfDMps.root"
    filepath["METbb_DMhf_obs"] = "DMbb/2015/Limits_hfDMps.root"
    filepath["METbb_DMtt_exp"] = "DMbb/2015/Limits_hfDMps.root"
    filepath["METbb_DMbb_exp"] = "DMbb/2015/Limits_hfDMps.root"
    filepath["METbb_DMhf_exp"] = "DMbb/2015/Limits_hfDMps.root"

#####################
### Plot settings ###
#####################

linestyle["BSM" ]           = kDotted
#MET+jets
linestyle["monojet_obs"]    = kSolid
linestyle["monojet_exp"]    = kDashed
# HF
linestyle["DMtt_obs"]       = kSolid
linestyle["METbb_DMtt_obs"] = kSolid
linestyle["METbb_DMbb_obs"] = kSolid
linestyle["METbb_DMhf_obs"] = kSolid
linestyle["DMtt_exp"]       = kDashed
linestyle["METbb_DMtt_exp"] = kDashed
linestyle["METbb_DMbb_exp"] = kDashed
linestyle["METbb_DMhf_exp"] = kDashed

color["BSM"]            = kBlack
color["monojet_obs"]    = kRed+1
color["DMtt_obs"]       = kAzure
color["METbb_DMbb_obs"] = kGreen+2

color["METbb_DMhf_obs"] = kAzure+2
color["METbb_DMtt_obs"] = kAzure+2

color["monojet_exp"]    = color["monojet_obs"]
color["DMtt_exp"]       = color["DMtt_obs"]
color["METbb_DMbb_exp"] = color["METbb_DMbb_obs"]
color["METbb_DMtt_exp"] = color["METbb_DMtt_obs"]
color["METbb_DMhf_exp"] = color["METbb_DMhf_obs"]


### TEXT obs
text["BSM"]            = "BSM Theory DMF"
text["monojet_obs"]    = "Mono-V/j [EXO-16-037] (obs)"
text["DMtt_obs"]       = "DM+tt [EXO-16-005] (obs)"
text["METbb_DMbb_obs"] = "DM+bb [B2G-15-007] (obs)"
text["METbb_DMtt_obs"] = "DM+tt (nj<4) [B2G-15-007] (obs)"
text["METbb_DMhf_obs"] = "MET+bb: DM+HF [B2G-15-007] (obs)"
#exp
text["monojet_exp"]    = "exp.excl 95%CL"
text["DMtt_exp"]       = "exp.excl 95%CL"
text["METbb_DMbb_exp"] = "exp.excl 95%CL"
text["METbb_DMtt_exp"] = "exp.excl 95%CL"
text["METbb_DMhf_exp"] = "exp.excl 95%CL"

####################
### Get datfiles ###
### Get graphs   ###
####################

### to do: make more generic for dat/root formats (if necessary)
f1 = TF1("f1","1",0,1000)

for analysis in analyses: 
    if   analysis == "BSM"            : tgraph[analysis] = TGraph(f1)
    elif analysis == "monojet_obs"    : tgraph[analysis] = TFile(filepath[analysis]).Get("obs")
    elif analysis == "monojet_exp"    : tgraph[analysis] = TFile(filepath[analysis]).Get("exp")
    elif analysis == "METbb_DMbb_obs" : tgraph[analysis] = TFile(filepath[analysis]).Get("bbObs0s")
    elif analysis == "METbb_DMtt_obs" : tgraph[analysis] = TFile(filepath[analysis]).Get("ttObs0s")
    elif analysis == "METbb_DMhf_obs" : tgraph[analysis] = TFile(filepath[analysis]).Get("hfObs0s")
    elif analysis == "METbb_DMbb_exp" : tgraph[analysis] = TFile(filepath[analysis]).Get("bbExp0s")
    elif analysis == "METbb_DMtt_exp" : tgraph[analysis] = TFile(filepath[analysis]).Get("ttExp0s")
    elif analysis == "METbb_DMhf_exp" : tgraph[analysis] = TFile(filepath[analysis]).Get("hfExp0s")
    else                              : tgraph[analysis] = TGraph(filepath[analysis])

###################
### Make Canvas ###
### Set ranges  ###
### Add legend  ###
###################

C=TCanvas("C","C",750,600)
C.cd(1).SetLogx()
C.cd(1).SetLogy()

tgraph["monojet_obs"].SetTitle("CMS Preliminary EXO Scalar Mediator Summary [ICHEP v1]")
tgraph["monojet_obs"].GetXaxis().SetTitle("M_{Med} [GeV]")
tgraph["monojet_obs"].GetYaxis().SetTitle("#sigma / #sigma_{BSM}")
tgraph["monojet_obs"].GetXaxis().SetTitleOffset(1.0)
tgraph["monojet_obs"].GetYaxis().SetTitleOffset(1.0)
tgraph["monojet_obs"].GetXaxis().SetTitleSize(0.045)
tgraph["monojet_obs"].GetYaxis().SetTitleSize(0.045)
tgraph["monojet_obs"].GetXaxis().SetRangeUser(10,    500)
tgraph["monojet_obs"].GetYaxis().SetRangeUser(0.1, 100000)
tgraph["monojet_obs"].Draw()

leg=C.BuildLegend(0.25,0.60,0.75,0.88)
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.Clear()
leg.SetHeader(Mediator+" Mediator, Dirac DM [g=1, m_{DM}=1GeV]")

############
### Draw ###
############

for analysis in analyses:
    tgraph[analysis].SetLineColor(color[analysis])
    if analysis == "BSM" or analysis=="DMtt_exp" or analysis=="METbb_DMtt_exp" or analysis=="METbb_DMbb_exp" or analysis=="METbb_DMhf_exp" or analysis=="monojet_exp":
        tgraph[analysis].SetLineWidth( 4)
        tgraph[analysis].SetFillStyle(3005)
        tgraph[analysis].SetFillColor(kWhite)
    else:
        tgraph[analysis].SetFillColor(color[analysis])
        tgraph[analysis].SetFillStyle(3005)
        tgraph[analysis].SetLineWidth( 404)
    tgraph[analysis].SetLineStyle(linestyle[analysis])
    leg.AddEntry(tgraph[analysis],text[analysis])
    tgraph[analysis].Draw("same")

leg.Draw()
C.Update()

############
### Save ###
############

if ObsOnly: C.SaveAs(Mediator+"_METX_Summary_ICHEP_obsonly.pdf")
else      : C.SaveAs(Mediator+"_METX_Summary_ICHEP_obsnexp.pdf")

###########
### FIN ###
###########
