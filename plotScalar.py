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

Mediator  = "Scalar"

ObsOnly = False

#################
### Analyses ####
#################

analyses = ["BSM",
            "monojet",
            "DMtt_obs",
            "METbb_DMtt_obs",
            "METbb_DMbb_obs"
            #,"METbb_DMhf_obs"
            ]

if not ObsOnly: analyses=["BSM","monojet",
                          "DMtt_exp","DMtt_obs",
                          "METbb_DMtt_exp","METbb_DMtt_obs",
                          "METbb_DMbb_exp","METbb_DMbb_obs"
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
    filepath["monojet"]        = "DMtt/DMtt_Scalar_ICHEP2016_Mx_obs.txt"
    filepath["DMtt_obs"]       = "DMtt/DMtt_Scalar_ICHEP2016_Mx_obs.txt"
    filepath["DMtt_exp"]       = "DMtt/DMtt_Scalar_ICHEP2016_Mx_exp.txt"
    filepath["METbb_DMtt_obs"] = "DMbb/2015/Limits_hfDMs.root"
    filepath["METbb_DMbb_obs"] = "DMbb/2015/Limits_hfDMs.root"
    filepath["METbb_DMhf_obs"] = "DMbb/2015/Limits_hfDMs.root"
    filepath["METbb_DMtt_exp"] = "DMbb/2015/Limits_hfDMs.root"
    filepath["METbb_DMbb_exp"] = "DMbb/2015/Limits_hfDMs.root"
    filepath["METbb_DMhf_exp"] = "DMbb/2015/Limits_hfDMs.root"

#####################
### Plot settings ###
#####################

linestyle["BSM" ]           = kDotted
linestyle["monojet"]        = kDotted
linestyle["DMtt_obs"]       = kSolid
linestyle["METbb_DMtt_obs"] = kSolid
linestyle["METbb_DMbb_obs"] = kSolid
linestyle["METbb_DMhf_obs"] = kSolid
linestyle["DMtt_exp"]       = kDashed
linestyle["METbb_DMtt_exp"] = kDashed
linestyle["METbb_DMbb_exp"] = kDashed
linestyle["METbb_DMhf_exp"] = kDashed

color["BSM"]            = kBlack
color["monojet"]        = kBlue
color["DMtt_obs"]       = kRed
color["METbb_DMbb_obs"] = kGreen
color["METbb_DMtt_obs"] = kGreen+1
color["METbb_DMhf_obs"] = kGreen-1
color["DMtt_exp"]       = kRed
color["METbb_DMbb_exp"] = kGreen
color["METbb_DMtt_exp"] = kGreen+1
color["METbb_DMhf_exp"] = kGreen-1

text["BSM"]        = "BSM Theory DMF"
text["monojet"]    = "Mono-V/j [EXO-16-037] (obs)"
text["DMtt_obs"]       = "DM+tt [EXO-16-005] (obs)"
text["METbb_DMbb_obs"] = "DM+bb [B2G-15-007] (obs)"
text["METbb_DMtt_obs"] = "DM+tt (nj<4) [B2G-15-007] (obs)"
text["METbb_DMhf_obs"] = "MET+bb: DM+HF [B2G-15-007] (obs)"
text["DMtt_exp"]       = "DM+tt [EXO-16-005] (exp)"
text["METbb_DMbb_exp"] = "DM+bb [B2G-15-007] (exp)"
text["METbb_DMtt_exp"] = "DM+tt (nj<4) [B2G-15-007] (exp)"
text["METbb_DMhf_exp"] = "MET+bb: DM+HF [B2G-15-007] (exp)"

####################
### Get datfiles ###
### Get graphs   ###
####################

### to do: make more generic for dat/root formats (if necessary)
f1 = TF1("f1","1",0,1000)

for analysis in analyses: 
    if analysis == "BSM"          : tgraph[analysis] = TGraph(f1)
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

tgraph["DMtt_obs"].SetTitle("CMS Preliminary EXO Scalar Mediator Summary [ICHEP v1]")
tgraph["DMtt_obs"].GetXaxis().SetTitle("M_{Med} [GeV]")
tgraph["DMtt_obs"].GetYaxis().SetTitle("#sigma / #sigma_{BSM}")
tgraph["DMtt_obs"].GetXaxis().SetTitleOffset(1.0)
tgraph["DMtt_obs"].GetYaxis().SetTitleOffset(1.0)
tgraph["DMtt_obs"].GetXaxis().SetTitleSize(0.045)
tgraph["DMtt_obs"].GetYaxis().SetTitleSize(0.045)
tgraph["DMtt_obs"].GetXaxis().SetRangeUser(10,     500)
tgraph["DMtt_obs"].GetYaxis().SetRangeUser(0.1, 100000)
tgraph["DMtt_obs"].Draw()

leg=C.BuildLegend(0.15,0.60,0.50,0.88)
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.Clear()
leg.SetHeader(Mediator+" [g=1, m_{DM}=1GeV], obs.excl.95%CL")

############
### Draw ###
############

for analysis in analyses:
    tgraph[analysis].SetLineColor(color[analysis])
    if analysis == "BSM" or analysis=="DMtt_exp" or analysis=="METbb_DMtt_exp" or analysis=="METbb_DMbb_exp" or analysis=="METbb_DMhf_exp":
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
