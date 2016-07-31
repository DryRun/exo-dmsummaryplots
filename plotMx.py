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

#################
### Analyses ####
#################

analyses = ["LUX","PandaX"]

filename = {}
tgraph   = {}
text     = {}
color    = {}

####################
### Get datfiles ###
### Get graphs   ###
####################

filename["LUX"]    = "DD/LUX_SI_DMTools_Jul2016.dat"
filename["PandaX"] = "DD/PandaX_SI_arxiv_Jul2016.dat"

text["LUX"] = "LUX"
text["PandaX"] = "PandaX"

color["LUX"] = kBlue
color["PandaX"] = kRed

### to do: make more generic for dat/root formats

for analysis in analyses: 
    tgraph[analysis] = TGraph(filename[analysis])

###################
### Make Canvas ###
### Set ranges  ###
### Add legend  ###
###################

C=TCanvas("C","C",1000,600)
C.cd(1)
C.cd(1).SetLogx()
C.cd(1).SetLogy()

tgraph["LUX"].SetTitle("DD Summer 2016")
tgraph["LUX"].GetXaxis().SetTitle("m_{DM} [GeV]")
tgraph["LUX"].GetYaxis().SetTitle("#sigma_{SI} [cm^{2}]")
tgraph["LUX"].GetXaxis().SetTitleOffset(1.0)
tgraph["LUX"].GetYaxis().SetTitleOffset(1.0)
tgraph["LUX"].GetXaxis().SetTitleSize(0.045)
tgraph["LUX"].GetYaxis().SetTitleSize(0.045)
tgraph["LUX"].GetXaxis().SetRangeUser(0,1000)
#tgraph[""].GetYaxis().SetRangeUser(0,1200)
tgraph["LUX"].Draw()

leg=C.BuildLegend(0.50,0.50,0.80,0.88)
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.Clear()
leg.SetHeader("#sigma_{SI}")

############
### Draw ###
############

for analysis in analyses:
    tgraph[analysis].SetLineColor(color[analysis])
    tgraph[analysis].SetFillColor(color[analysis])
    tgraph[analysis].SetFillStyle(3005)
    tgraph[analysis].SetLineWidth( 404)
    if analysis == "LUX":
        tgraph[analysis].SetFillColor(color[analysis])
        tgraph[analysis].SetLineStyle(kDotted)
        tgraph[analysis].SetLineWidth(404)
        tgraph[analysis].SetFillStyle(3005)
    elif analysis == "PandaX":
        tgraph[analysis].SetLineWidth(-404)
    leg.AddEntry(tgraph[analysis],text[analysis])
    tgraph[analysis].Draw("same")

leg.Draw()
C.Update()

#################
### Save plot ###
#################

C.SaveAs("DD.pdf")

###########
### FIN ###
###########
