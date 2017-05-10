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
import os
from Utilities import *
#################################
### Parameters to be modified ###
#################################

Dijet    = False
Dilepton = False

# Mediator  = raw_input('Choose mediator [Vector or Axial]: ')
# Scenario  = raw_input('Choose Scenario according to 1703.05703 [1 or 2 or dijetchi or Monotop]: ') #1 for Default MET+X, 2 for dil, gq=gDM=1 for dijetchi
# #METXonly  = ast.literal_eval(raw_input('MET+X only? [True or False]: '))
# METX        = ast.literal_eval(raw_input('MET+X? [True or False]: '))
# Resonances  = ast.literal_eval(raw_input('Resonances? [True or False]: '))
# if Resonances :
#     Dijet     = ast.literal_eval(raw_input('Dijet? [True or False]: '))
#     Dilepton  = ast.literal_eval(raw_input('Dilepton? [True or False]: '))

# if Dilepton : gl = ast.literal_eval(raw_input('gl? [0.10 or 0.025 or 0.01]: '))

# logx      = ast.literal_eval(raw_input('Log x? '))

#A1/V1
# Mediator = "Vector"
# Scenario = "1"
# METX = 1
# Resonances = 1
# Dijet = 1
# Dilepton = 0
# logx = 0

#A1/V1 just MET+X
Mediator = "Vector"
Scenario = "1"
METX = 1
Resonances = 1
Dijet = 1
Dilepton = 0
logx = 0

#A2
# Mediator = "Axial"
# #Mediator = "Vector"
# Scenario = "2"
# METX = 0
# Resonances = 1
# Dijet = 0
# Dilepton = 1

# logx = 0

#dijetchi
# Mediator = "Vector"
# Scenario = "dijetchi"
# METX = 0
# Resonances = 1
# Dijet = 1
# Dilepton = 0
# logx = 0


#Monotop
# Mediator = "Vector"
# Scenario = "Monotop"
# METX = 1
# Resonances = 0
# logx = 0


CL = "95"

#################
### Analyses ####
#################

#####DECIDE WHERE TO PUT MONOTOP and DIJETCHI DIJET_EXP

#if Mediator == "Axial": metx = ["monojet","monophoton","monoz"]
#else                  : metx = ["monojet","monophoton","monoz","monoHgg"]
def make_plot(Mediator, Scenario, METX, Resonances, Dijet, Dilepton, logx, CL):
    output = "./output"
    if(not os.path.exists(output)): os.makedirs(output)
    texts = []


    if(  Mediator == "Axial"  and Scenario == "1"): scenario_name = "A1"
    elif(Mediator == "Axial"  and Scenario == "2"): scenario_name = "A2"
    elif(Mediator == "Axial"  and Scenario == "3"): scenario_name = "A3"
    elif(Mediator == "Vector" and Scenario == "1"): scenario_name = "V1"
    elif(Mediator == "Vector" and Scenario == "2"): scenario_name = "V2"
    elif(Mediator == "Vector" and Scenario == "3"): scenario_name = "V3"
    elif(Mediator == "Vector" and Scenario == "4"): scenario_name = "V4"



    metx = []
    if   scenario_name in ["A1","V1"]:
        metx = ["monojet","monophoton","monoz"]
    elif scenario_name in ["A1","V2"]:
        metx = []
    elif scenario_name in ["A3","V3"]:
        metx = []
    elif  scenario_name in ["V4"]:
        metx = ["monotop"]



    analyses = ["relic"]
    if METX: analyses += metx
    if Dilepton  : analyses += ["dilepton"]
    if Dijet :
        if scenario_name in ["A3","V3"] : analyses += ["dijetchi"]
        else : analyses += ["dijet","trijet"]





    ### Get plotting parameters
    linestyle = get_line_style()
    color = get_color()
    text = get_text()



    ###################
    ### Recast ###
    ###################




    ###################
    ### Make Canvas ###
    ### Set ranges  ###
    ###################

    C=TCanvas("C","C",1000,600)
    C.cd(1)

    C.cd(1).SetTickx()
    C.cd(1).SetTicky()

    if logx       : frame = C.cd(1).DrawFrame(90,0,3700, 1450)
    #elif METXonly : frame = C.cd(1).DrawFrame(0,0,2000, 780)
    #elif Dilepton : frame = C.cd(1).DrawFrame(0,0,5000,2000)
    #else          : frame = C.cd(1).DrawFrame(0,0,3700,1450)
    else :
        if Dilepton :
            frame = C.cd(1).DrawFrame(0,0,4200,2000)
        elif Scenario=="dijetchi":
            frame = C.cd(1).DrawFrame(0,0,5500,2000)
        elif Scenario=="1" and Resonances==0 and Dijet==0 and Dilepton==0 :
            frame = C.cd(1).DrawFrame(0,0,2000,1000)
        else :
            frame = C.cd(1).DrawFrame(0,0,5200,2000)

    if logx : C.cd(1).SetLogx()

    frame.SetXTitle("Mediator mass [GeV]")
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

    leg = make_legend(scenario_name)



    dummies = make_dummy_entries(leg)
    ####################
    ### Add diagonal ###
    ####################

    f1 = TF1("f1","x/2.",0,4000)
    g1 = TGraph(f1)
    g1.SetLineColor(color["relic"]-1)
    g1.SetLineStyle(kDashed)
    g1.Draw()

    ### Labeling

    # Relic
    relic_coords = get_relic_coordinates()
    relic_angles = get_relic_angles()
    for coord in relic_coords[scenario_name]:
        texts.append(add_text(*coord,TEXT="#Omega_{c} h^{2} #geq 0.12",color=color["relic"],angle=relic_angles[scenario_name]))

    # Diagonal
    diagonal_coords = get_diagonal_coordinates()
    texts.append(add_text(*diagonal_coords[scenario_name],TEXT="M_{Med} = 2 x m_{DM}",color=color["relic"],angle=30))

    # Scenario
    scenario_coords = get_scenario_label_coordinates()
    scenario_label = get_scenario_labels()
    texts.append(add_text(0.1,0.2,0.9,0.97,"#bf{CMS}"))
    try:
        texts.append(add_text(*scenario_coords[scenario_name],TEXT=scenario_label[scenario_name]))
    except KeyError:
        pass






    ############
    ### Draw ###
    ############

    ### Read graphs:
    all_graphs = read_graphs()

    tgraph = {}
    for a in analyses:
        print a
        tgraph[a] = all_graphs[a][scenario_name]["obs"]


    reliclist = read_relic_lists()
    for analysis in analyses:

        ### Observed limit
        obs = all_graphs[analysis][scenario_name]["obs"]
        if( not obs ): continue
        print "analysis "+analysis
        obs.SetLineColor(color[analysis])
        obs.SetMarkerSize(0.1)
        obs.SetMarkerColor(color[analysis])
        obs.SetFillColor(color[analysis])
        obs.SetFillStyle(3005)
        obs.SetLineWidth( 202)
        obs.SetLineStyle(linestyle[analysis])

        if not  analysis=="relic":
            leg.AddEntry(obs,text[analysis],"L")

        if analysis == "relic":
            for i in range(0,reliclist[scenario_name].GetSize()):
                obs = reliclist[scenario_name].At(i)
                obs.SetLineColor(color[analysis]-1)
                obs.SetFillColor(color[analysis]-1)
                obs.SetLineStyle(linestyle[analysis])
                obs.SetLineWidth(202)
                obs.SetFillStyle(3005)
                obs.Draw("same")
        elif analysis == "dijetchi":
            obs.SetLineWidth(-404)
        obs.Draw("same")

        ### Expected limit
        exp = all_graphs[analysis][scenario_name]["exp"]
        if( not exp ): continue
        exp.SetLineColor(color[analysis])
        exp.SetMarkerSize(0.1)
        exp.SetMarkerColor(color[analysis])
        exp.SetFillColor(color[analysis])
        exp.SetFillStyle(3005)
        exp.SetLineWidth(202)
        exp.SetLineStyle(kDashed)
        exp.Draw("same")

    ########################
    ### Write some texts ###
    ########################


    leg.Draw("same")
    for t in texts: t.Draw("same")

    C.Update()

    ############
    ### Save ###
    ############

    figname = Mediator
    if METX      : figname += "_METX"
    if Dilepton  : figname += "_Dilepton"
    if Dijet     : figname += "_Multijet"
    figname += "_Scenario"+Scenario+"_Summary.pdf"

    C.SaveAs("{OUTPUT}/{FILE}".format(OUTPUT=output,FILE=figname))
    C.Close()

for Mediator in ["Axial", "Vector"]:
    for Scenario in ["1", "2","3"]:
        for Resonances in [0,1]:
            make_plot(Mediator, Scenario, METX=True, Resonances=Resonances, Dijet=Resonances, Dilepton=Resonances, logx=False, CL="95")


###########
### FIN ###
###########
