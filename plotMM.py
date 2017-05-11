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
def make_plot(Mediator, Scenario, METX, Resonances, Dijet, Dilepton, logx, CL,do_expected=False):
    output = "./output"
    if(not os.path.exists(output)): os.makedirs(output)
    texts = []


    if(  Mediator == "Axial"  and Scenario == "1"): scenario_name = "A1"
    elif(Mediator == "Axial"  and Scenario == "2"): scenario_name = "A2"
    elif(Mediator == "Axial"  and Scenario == "3"): scenario_name = "A3"
    elif(Mediator == "Axial"  and Scenario == "4"): scenario_name = "A3"
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



    analyses = []

    if Dilepton  : analyses += ["dilepton"]
    if Dijet :
        if scenario_name in ["A3","V3"] : analyses += ["dijetchi"]
        else : analyses += ["dijet","trijet"]
    analyses.append("relic")
    if METX: analyses += metx

    if(len(analyses)<2):return None


    ### Get plotting parameters
    linestyle = get_line_style()
    fillstyle = get_fill_style()
    linewidth = get_line_width()
    color = get_color()
    linecolor = get_line_color()
    text = get_text()



    ### Make Canvas
    C=TCanvas("C","C",1000,600)
    C.cd(1)

    C.cd(1).SetTickx()
    C.cd(1).SetTicky()

    if logx:
        frame = C.cd(1).DrawFrame(90,0,3700, 1450)
        C.cd(1).SetLogx()
    else :
        if scenario_name in ["A3","V3"]:
            frame = C.cd(1).DrawFrame(0,0,5500,2000)
        elif scenario_name in ["A4","V4"]:
            frame = C.cd(1).DrawFrame(0,0,2900,800)
        elif scenario_name in ["A2"]:
            frame = C.cd(1).DrawFrame(0,0,4500,2000)
        elif Dilepton :
            frame = C.cd(1).DrawFrame(0,0,4500,2000)

        elif Scenario=="1" and Resonances==0 and Dijet==0 and Dilepton==0 :
            frame = C.cd(1).DrawFrame(0,0,2800,1000)
        else :
            frame = C.cd(1).DrawFrame(0,0,5200,2000)

    frame.SetXTitle("Mediator mass [GeV]")
    frame.SetYTitle("m_{DM} [GeV]")
    frame.GetXaxis().SetTitleSize(0.052)
    frame.GetYaxis().SetTitleSize(0.052)
    frame.GetXaxis().SetTitleOffset(0.85)
    frame.GetYaxis().SetTitleOffset(0.85)


    ### Diagonal
    f1 = TF1("f1","x/2.",0,4000)
    g1 = TGraph(f1)
    g1.SetLineColor(color["relic"])
    g1.SetMarkerColor(color["relic"])
    g1.SetLineStyle(7)
    g1.SetLineWidth(1)
    g1.Draw("L")

    #### Legend
    leg = make_legend(scenario_name)
    auxleg = make_auxiliary_legend(scenario_name)
    auxleg.AddEntry(g1,"M_{Med} = 2 x m_{DM}","L")
    # Dummy entries are non-colored lines
    # Do not need to do anything with them
    # just keep them around
    if(do_expected):
        dummies = make_dummy_entries(leg)



    ### Labeling
    texts.append(add_text(0.7,0.85,0.9,1.0,"LHCP 2017"))

    #~ # Relic
    #~ relic_coords = get_relic_coordinates()
    #~ relic_angles = get_relic_angles()
    #~ for coord in relic_coords[scenario_name]:
        #~ texts.append(add_text(*coord,TEXT="#Omega_{c} h^{2} #geq 0.12",color=color["relic"],angle=relic_angles[scenario_name]))

    #~ # Diagonal
    #~ diagonal_coords = get_diagonal_coordinates()
    #~ diagonal_angles = get_diagonal_angles()
    #~ texts.append(add_text(*diagonal_coords[scenario_name],TEXT="M_{Med} = 2 x m_{DM}",color=color["relic"],angle=diagonal_angles[scenario_name]))

    # Scenario
    scenario_coords = get_scenario_label_coordinates(not Dijet)
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

    reliclist = read_relic_lists()
    for analysis in analyses:

        ### Observed limit
        obs = all_graphs[analysis][scenario_name]["obs"]
        if( not obs ): continue
        print "analysis "+analysis
        obs.SetFillColor(color[analysis])
        obs.SetLineColor(linecolor[analysis])
        obs.SetMarkerSize(0.1)
        obs.SetMarkerColor(color[analysis])
        obs.SetFillColor(color[analysis])
        obs.SetFillStyle(fillstyle[analysis])

        obs.SetLineWidth(linewidth[analysis])
        obs.SetLineStyle(linestyle[analysis])

        if(analysis in ["dijet","dilepton","trijet"]):
            leg.AddEntry(obs,text[analysis],"FL")
        elif not  analysis=="relic":
            leg.AddEntry(obs,text[analysis],"L")

        if analysis == "relic":
            for i in range(0,reliclist[scenario_name].GetSize()):
                obs = reliclist[scenario_name].At(i)
                obs.SetLineColor(color[analysis])
                obs.SetFillColor(color[analysis])
                obs.SetLineStyle(linestyle[analysis])
                obs.SetLineWidth(101)
                obs.SetFillStyle(3005)
                obs.Draw("same")
            auxleg.AddEntry(obs,"#Omega_{c} h^{2} #geq 0.12","LF")
            g1.Draw("same")
        #~ elif analysis == "dijetchi":
            #~ obs.SetLineWidth(-404)
        if(analysis in ["dijet","dilepton","trijet"]):
            obs.Draw("F,same")
            obs.Draw("L,same")

        else: obs.Draw("same")

        ### Expected limit
        exp = all_graphs[analysis][scenario_name]["exp"]
        if( not do_expected or not exp ): continue
        exp.SetLineColor(linecolor[analysis])
        exp.SetMarkerSize(0.1)
        exp.SetMarkerColor(color[analysis])
        exp.SetFillColor(color[analysis])
        exp.SetFillStyle(fillstyle[analysis])
        exp.SetLineWidth(2)
        exp.SetLineStyle(kDashed)
        exp.Draw("same")

    ########################
    ### Write some texts ###
    ########################


    leg.Draw("same")
    auxleg.Draw("same")
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
    C.cd(1).RedrawAxis()
    #~ if(scenario_name in ["A2","V2"]):
        #~ C.cd(1).SetLogx(1)
    C.SaveAs("{OUTPUT}/{FILE}".format(OUTPUT=output,FILE=figname))
    C.Close()

for Mediator in ["Axial", "Vector"]:
    for Scenario in ["1", "2"]:
        for Resonances in [0,1]:
            make_plot(Mediator, Scenario, METX=True, Resonances=Resonances, Dijet=Resonances, Dilepton=Resonances, logx=False, CL="95",do_expected=True)


###########
### FIN ###
###########
