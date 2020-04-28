#########################################
#########################################
###                                   ###
### Draw awesome MET+X Summary plots  ###
###                                   ###
### (c) MET+X Combo                   ###
###                                   ###
#########################################
#########################################

import ROOT
ROOT.gROOT.SetBatch(True)
import ast
import os
import sys
from Utilities import *

from ExoDMSummaryPlots.Common.benchmarks import benchmarks

import argparse
parser = argparse.ArgumentParser(description="Make MDM vs MZp plots")
parser.add_argument('--analyses', type=str, required=True, help='List of CMS analyses (comma separated))')
parser.add_argument('--scenario', type=str, required=True, help='Model name (e.g. V1, A2, ...)')
parser.add_argument('--logx', action='store_true', default=False, help='log x axis')
parser.add_argument('--relic', action='store_true', help='Draw relic density')
parser.add_argument('--noexp', action='store_true', help='Skip expected limits')
parser.add_argument('--cms', action='store_true', help='Draw CMS')
parser.add_argument('--cms_label', type=str, help='Draw CMS plus specified text')
parser.add_argument('--conference_label', type=str, help='Conference label')
parser.add_argument('--save_name', type=str, help='Output filename')
parser.add_argument('--save_tag', type=str, help='Tag for saving (e.g. _conferenceName)')
parser.add_argument('--formats', type=str, default='pdf,png', help='Output file formats. PNG is handled through imagemagick.')
args = parser.parse_args()

print "\n*** Welcome to plotMM! It's a wonderful day in the neighborhood! ***\n"
print "\tAnalysis={}".format(args.analyses)
print "\tScenario={}".format(args.scenario)

# ROOT style options for trends (markers, lines, fills)
style = {
    "default":{
        "line_color":ROOT.kBlack,
        "line_style":ROOT.kSolid,
        "line_width":1,
        "fill_style":1001,
        "fill_color":ROOT.kGray,
        "legend":None,
    },
    "dijet":{
        "line_color":ROOT.kYellow+3,
        "line_style":ROOT.kSolid,
        "line_width":2,
        "fill_style":1001,
        "fill_color":ROOT.kYellow-10,
        "legend":"#splitline{#bf{Dijet} (35.9-137 fb^{-1})}{#splitline{#it{[arXiv:1806.00843]}}{#it{[arXiv:1911.03947]}}}",
    },
    "dijetchi":{
        "line_color":ROOT.kAzure,
        "line_style":ROOT.kSolid,
        "line_width":2,
        "fill_style":1001,
        "fill_color":ROOT.kYellow-10,
        "legend":"#bf{Dijet #chi}  (36.5 fb^{-1}) #it{[EXO-16-046]}",
    },
    "dijetbb":{
        "line_color":ROOT.kMagenta-5,
        "line_style":ROOT.kSolid,
        "line_width":2,
        "fill_style":1001,
        "fill_color":ROOT.kYellow-10,
        "legend":"#splitline{#bf{Dijet w/ btag} (19.7 fb^{-1})}{#it{[arXiv:1802.06149]}}",
    },
    "trijet":{
        "line_color":ROOT.kRed-3,
        "line_style":ROOT.kSolid,
        "line_width":2,
        "fill_style":1001,
        "fill_color":ROOT.kYellow-10,
        "legend":"#splitline{#bf{Dijet w/ ISR j} (18.3 fb^{-1})}{#it{[arXiv:1911.03761]}}",
    },
    "dilepton":{
        "line_color":ROOT.kGreen+3,
        "line_style":ROOT.kSolid,
        "line_width":2,
        "fill_style":1001,
        "fill_color":ROOT.kGreen-10,
        "legend":"#splitline{#bf{Dilepton} (137 fb^{-1})}{#it{[EXO-19-019]}}",
        #"legend":"#splitline{#bf{Dilepton} (35.9-36.3 fb^{-1})}{#it{[arXiv:1803.06292]}}",
    },
    "boosted_dijet_isrj":{
        "line_color":ROOT.kCyan-5,
        "line_style":ROOT.kSolid,
        "line_width":2,
        "fill_style":1001,
        "fill_color":ROOT.kYellow-10,
        "legend":"#splitline{#bf{Boosted dijet} (77 fb^{-1})}{#it{[arXiv:1909.04114]}}",
    },

    "monojet":{
        "line_color":ROOT.kRed+2,
        "line_style":ROOT.kSolid,
        "line_width":102,
        "fill_style":3005,
        "fill_color":ROOT.kRed+2,
        "legend":"#splitline{#bf{DM + j/V(qq)} (35.9 fb^{-1})}{#it{[arXiv:1712.02345]}}",
    },
    "monophoton":{
        "line_color":ROOT.kBlue-4,
        "line_style":ROOT.kSolid,
        "line_width":102,
        "fill_style":3005,
        "fill_color":ROOT.kOrange+9,
        "legend":"#splitline{#bf{DM + #gamma} (35.9 fb^{-1})}{#it{[arXiv:1810.00196]}}"
    },
    "monoz":{
        "line_color":ROOT.kOrange+1,
        "line_style":ROOT.kSolid,
        "line_width":-102,
        "fill_style":3005,
        "fill_color":ROOT.kOrange-3,
        "legend":"#splitline{#bf{DM + Z(ll)} (35.9 fb^{-1})}{#it{[arXiv:1711.00431]}}",
    },
    "monoHgg":{
        "line_color":ROOT.kMagenta-7,
        "line_style":ROOT.kSolid,
        "line_width":102,
        "fill_style":3005,
        "fill_color":ROOT.kMagenta-7,
        "legend":"#splitline{#bf{DM + H_{#gamma #gamma}} (35.9 fb^{-1})}{#it{[EXO-16-054]}}"
    },
    "monotop":{
        "line_color":ROOT.kViolet+1,
        "line_style":ROOT.kSolid,
        "line_width":102,
        "fill_style":3005,
        "fill_color":ROOT.kViolet+1,
        "legend":"#splitline{#bf{DM + t} (100% FC, 35.8 fb^{-1}) }{#it{[EXO-16-051]}}"
    },

    "relic":{
        "line_color":ROOT.kGray+1,
        "line_style":ROOT.kSolid,
        "line_width":101,
        "fill_style":3005,
        "fill_color":ROOT.kGray+1,
        "legend":"\Omega_{c} h^{2} \geq 0.12"
    },
}

# Canvas parameters
canvas_style = {
    "scenario_label":{
        "A1":[ "#bf{Axial-vector mediator}","Dirac DM", "g_{DM} = 1.0","g_{q}  = 0.25","g_{l} = 0" ],
        "A2":[ "#bf{Axial-vector mediator}","Dirac DM", "g_{DM} = 1.0","g_{q}  = 0.1","g_{l} = 0.1" ],
        "A3":[ "#bf{Axial-vector mediator}","Dirac DM", "g_{DM} = 1.0","g_{q}  = 1.0","g_{l} = 0" ],
        "A4":[ "#bf{Axial-vector mediator}","Dirac DM", "g_{DM} = 1.0","g_{q}  = 0.25","g_{l} = 0" ],
        "V1":[ "#bf{Vector mediator}", "Dirac DM","g_{DM} = 1.0","g_{q}  = 0.25","g_{l} = 0" ],
        "V2":[ "#bf{Vector mediator}","Dirac DM", "g_{DM} = 1.0","g_{q}  = 0.1","g_{l} = 0.01" ],
        "V3":[ "#bf{Vector mediator}","Dirac DM", "g_{DM} = 1.0","g_{q}  = 1.0","g_{l} = 0" ],
        "V4":[ "#bf{Vector mediator}", "Dirac DM","g_{DM} = 1.0","g_{q}  = 0.25","g_{l} = 0" ],
    },
    "scenario_coords_linearx":{
        #"A1":(0.2,0.7,0.6,0.85),
        "A1":(0.3,0.8,0.6,0.85),
        "A2":(0.5,0.7,0.6,0.85),
        "A3":(0.1,0.3,0.6,0.85),
        "A4":(0.1,0.3,0.6,0.85),
        "V1":(0.3,0.5,0.6,0.85),
        "V2":(0.5,0.7,0.6,0.85),
        "V3":(0.1,0.3,0.6,0.85),
        "V4":(0.1,0.3,0.6,0.85),
    },
    "scenario_coords_logx":{
        "A1":(0.12,0.62,0.6,0.85),
        "A2":(0.65,0.9,0.7,0.9),
        "A3":(0.1,0.3,0.6,0.85),
        "A4":(0.1,0.3,0.6,0.85),
        "V1":(0.215,0.415,0.6,0.85),
        "V2":(0.55,0.75,0.6,0.85),
        "V3":(0.1,0.3,0.6,0.85),
        "V4":(0.1,0.3,0.6,0.85),
    },
    "relic_coordinate":{
        "A1":[(0.48,0.58,0.67,0.7),(0.46,0.56,0.42,0.45)  ],
        "A2":[(0.48,0.58,0.67,0.7),(0.46,0.56,0.42,0.45)  ],#[(0.1,0.3,0.6,0.85)  ],
        "A3":[(0.1,0.3,0.6,0.85)  ],
        "A4":[(0.1,0.3,0.6,0.85)  ],
        "V1":[(0.57,0.67,0.28,0.36)  ],
        "V2":[(0.57,0.67,0.28,0.36)  ],#[(0.7,0.85,0.5,0.6) ],
        "V3":[(0.1,0.3,0.6,0.85)  ],
        "V4":[(0.1,0.3,0.6,0.85)  ],
    },
    "relic_angle":{
        "A1":30,
        "A2":30,
        "A3":30,
        "A4":30,
        "V1":28,
        "V2":30,
        "V3":30,
        "V4":30,
    },
    "diagonal_coordinates":{
        "A1":(0.4,0.51,0.5,0.55),
        "A2":(0.1,0.3,0.6,0.85),
        "A3":(0.1,0.3,0.6,0.85),
        "A4":(0.1,0.3,0.6,0.85),
        "V1":(0.4,0.51,0.52,0.58),
        "V2":(0.7,0.85,0.5,0.6),
        "V3":(0.1,0.3,0.6,0.85),
        "V4":(0.1,0.3,0.6,0.85),
    },
    "diagonal_angle":{
        "A1":32,
        "A2":30,
        "A3":30,
        "A4":30,
        "V1":32,
        "V2":30,
        "V3":30,
        "V4":30,
    },
    "legend_coordinates":{
        #"A1":(0.68,0.15,0.87,0.65),
        "A1":(0.78, 0.07, 0.99, 0.9),
        "A2":(0.78, 0.3, 0.99, 0.8),#(0.62,0.15,0.87,0.5),
        "A3":(0.4,0.12,0.8,0.3),
        "A4":(0.68,0.15,0.87,0.65),
        #"V1":(0.68,0.15,0.87,0.65),
        "V1":(0.78, 0.07, 0.99, 0.9),
        "V2":(0.78, 0.3, 0.99, 0.8),#(0.62,0.15,0.87,0.5),
        "V3":(0.35,0.67,0.75,0.85),
        "V4":(0.68,0.15,0.87,0.65),
    },
    "legend_textsize":{
        "A1":0.025,
        "A2":0.025,
        "A3":0.035,
        "A4":0.025,
        "V1":0.025,
        "V2":0.025,
        "V3":0.035,
        "V4":0.025,
    },
    "auxlegend_coordinates":{
        #"A1":(0.68,0.7,0.87,0.85),
        "A1":(0.53,0.17,0.72,0.32),
        "A2":(0.53,0.17,0.72,0.32),
        "A3":(0.6,0.33,0.8,0.45),
        "A4":(0.68,0.7,0.87,0.85),
        "V1":(0.53,0.17,0.72,0.32),
        "V2":(0.53,0.17,0.72,0.32),
        "V3":(0.55,0.52,0.75,0.64),
        "V4":(0.68,0.7,0.87,0.85),
    },
    "auxlegend_textsize":{
        "A1":0.035,
        "A2":0.035,
        "A3":0.035,
        "A4":0.035,
        "V1":0.035,
        "V2":0.035,
        "V3":0.035,
        "V4":0.035,
    }
}

def style_graph(analysis, tgraph, obsexp):
    if not tgraph:
        raise ValueError("[style_graph] TGraph for analysis {} doesn't exist".format(analysis))
    if not analysis in style:
        raise ValueError("[style_graph] Analysis {} is not in the style dictionary.".format(analysis))
    default_style = style["default"]
    this_style = style[analysis]

    if "fill_color" in this_style:
        tgraph.SetFillColor(this_style["fill_color"])
    else:
        tgraph.SetFillColor(default_style["fill_color"])
    if "fill_style" in this_style:
        tgraph.SetFillStyle(this_style["fill_style"])
    else:
        tgraph.SetFillStyle(default_style["fill_style"])

    if "line_color" in this_style:
        tgraph.SetLineColor(this_style["line_color"])
    else:
        tgraph.SetLineColor(default_style["line_color"])
    if "line_width" in this_style:
        tgraph.SetLineWidth(this_style["line_width"])
    else:
        tgraph.SetLineWidth(default_style["line_width"])
    if obsexp == "obs":
        tgraph.SetLineStyle(ROOT.kSolid)
    elif obsexp == "exp":
        tgraph.SetLineStyle(ROOT.kDashed)
    else:
        raise ValueError("[style_graph] obsexp is not 'obs' or 'exp'")

    tgraph.SetMarkerStyle(20)
    tgraph.SetMarkerSize(0.)

output_directory = os.path.expandvars("$CMSSW_BASE/src/ExoDMSummaryPlots/output/")
if not os.path.exists(output_directory):
    os.system("mkdir -pv {}".format(output_directory))

analyses = args.analyses.split(",")

if args.save_name:
    canvas_name = args.save_name
else:
    canvas_name = "MM_{}".format(args.scenario)
    if args.logx:
        canvas_name += "_logx"
    else:
        canvas_name += "_linearx"
    for analysis in analyses:
        if not "mono" in analysis:
            canvas_name += "_{}".format(analysis)
    if args.save_tag:
        canvas_name += args.save_tag
canvas = ROOT.TCanvas(canvas_name, canvas_name, 1000, 600)
canvas.SetRightMargin(0.25)
pad = canvas.cd(1)
pad.SetTickx()
pad.SetTicky()

if args.logx:
    frame = pad.DrawFrame(40,0,4e4,2000)
    pad.SetLogx()
else :
    if args.scenario in ["A3","V3"]:
        frame = pad.DrawFrame(0,0,5500,2000)
    elif args.scenario in ["A4","V4"]:
        frame = pad.DrawFrame(0,0,2900,800)
    elif args.scenario in ["A2"]:
        frame = pad.DrawFrame(0,0,5000,2500)
    else :
        frame = pad.DrawFrame(0,0,4500,2000)

frame.SetXTitle("Mediator mass M_{ med} [GeV]")
frame.SetYTitle("Dark matter mass m_{ DM} [GeV]")
frame.GetXaxis().SetTitleSize(0.052)
frame.GetYaxis().SetTitleSize(0.052)
frame.GetXaxis().SetTitleOffset(0.85)
frame.GetYaxis().SetTitleOffset(0.85)

#### Legend
leg = ROOT.TLegend(*canvas_style["legend_coordinates"][args.scenario])
leg.SetBorderSize(1)
leg.SetTextFont(42)
leg.SetTextSize(canvas_style["legend_textsize"][args.scenario])
leg.SetFillColor(ROOT.kWhite)
leg.SetFillStyle(1001)
leg.SetHeader("#bf{Exclusion at 95% CL}")

auxleg = ROOT.TLegend(*canvas_style["auxlegend_coordinates"][args.scenario])
auxleg.SetBorderSize(1)
auxleg.SetTextFont(42)
auxleg.SetFillColor(ROOT.kWhite)
auxleg.SetFillStyle(1001)
auxleg.SetTextSize(canvas_style["auxlegend_textsize"][args.scenario])

# Dummy entries for observed (solid) and expected (dashed) legend entries
if not args.noexp:
    dummies = make_dummy_entries(leg)

############
### Draw ###
############

### Read graphs:
all_graphs = read_graphs()
reliclist = read_relic_lists()

for analysis in analyses:
    obs_graph = all_graphs[analysis][args.scenario]["obs"]
    exp_graph = all_graphs[analysis][args.scenario]["exp"]

    if not obs_graph:
        print "ERROR : obs_graph doesn't exist! Analysis = {}, scenario = {}".format(analysis, args.scenario)
        sys.exit(1)

    if not exp_graph:
        print "ERROR : exp_graph doesn't exist! Analysis = {}, scenario = {}".format(analysis, args.scenario)
        sys.exit(1)

    if obs_graph.GetN() == 0 and exp_graph.GetN() == 0:
        print "ERROR : obs_graph and exp_graph have zero points! This probably means the analysis isn't sensitive to this scenario."
        print "ERROR : analysis = {}".format(analysis)
        sys.exit(1)

    style_graph(analysis, all_graphs[analysis][args.scenario]["obs"], "obs")
    style_graph(analysis, all_graphs[analysis][args.scenario]["exp"], "exp")

    if style[analysis]["fill_style"] == 1001:
        obs_graph.Draw("F,same")
        obs_graph.Draw("L,same")
        leg.AddEntry(obs_graph, style[analysis]["legend"], "FL")
    else:
        obs_graph.Draw("L,same")
        leg.AddEntry(obs_graph, style[analysis]["legend"], "L")

    if not args.noexp:
        exp_graph.Draw("L,same")

# Redraw lines on top of fills
for analysis in analyses:
    obs_graph = all_graphs[analysis][args.scenario]["obs"]
    obs_graph.Draw("L,same")
    if not args.noexp:
        exp_graph = all_graphs[analysis][args.scenario]["exp"]
        exp_graph.Draw("L,same")


# Draw relic density lines
if args.relic:
    for i in range(0,reliclist[args.scenario].GetSize()):
        obs = reliclist[args.scenario].At(i)
        obs.SetLineColor(style["relic"]["line_color"])
        obs.SetFillColor(style["relic"]["fill_color"])
        obs.SetLineStyle(style["relic"]["line_style"])
        obs.SetLineWidth(style["relic"]["line_width"]) # 101
        obs.SetFillStyle(style["relic"]["fill_style"]) # 3005
        obs.Draw("same")

# Draw diagonal
f1 = ROOT.TF1("f1","x/2.",0,4000)
diagonal_line = ROOT.TGraph(f1)
diagonal_line.SetLineColor(style["relic"]["line_color"])
diagonal_line.SetMarkerColor(style["relic"]["line_color"])
diagonal_line.SetLineStyle(7)
diagonal_line.SetLineWidth(1)
diagonal_line.Draw("L")
diagonal_line.Draw("same")
    
# auxleg entries
auxleg.AddEntry(diagonal_line, "M_{Med} = 2 x m_{ DM}", "L")
if args.relic:
    auxleg.AddEntry(reliclist[args.scenario].At(0),"#Omega_{c} h^{2} #geq 0.12","L")

########################
### Write some texts ###
########################
texts = [] # Save ROOT text objects so they don't disappear

# Conference label
if args.conference_label:
    # def add_text(x1, x2, y1, y2, text, color=1, alignment=22, angle = 0, argument="NDC"):
    texts.append(add_text(0.58, 0.75, 0.92, 1.0, args.conference_label))
    texts[-1].Draw("same")

# Scenario label
if args.logx:
    scenario_coords = canvas_style["scenario_coords_logx"][args.scenario]
else:
    scenario_coords = canvas_style["scenario_coords_linearx"][args.scenario]
texts.append(add_text(*scenario_coords, text=canvas_style["scenario_label"][args.scenario], alignment=12))
texts[-1].Draw("same")

# CMS label
if args.cms:
    texts.append(add_text(0.08,0.33,0.9,1.0,"#bf{CMS}"))
    texts[-1].Draw("same")
elif args.cms_label:
    texts.append(add_text(0.08,0.33,0.9,1.0,"#bf{{CMS}} {}".format(args.cms_label)))
    texts[-1].Draw("same")

leg.Draw("same")
auxleg.Draw("same")
pad.RedrawAxis()

canvas.Update()

############
### Save ###
############
formats = args.formats.split(",")
if "png" in formats:
    if "eps" in formats:
        formats.remove("eps")
    formats.insert(formats.index("png"), "eps")
for ext in formats:
    if ext == "png":
        os.system("convert -density 600 -trim {}/{}.eps  {}/{}.png".format(output_directory, canvas.GetName(), output_directory, canvas.GetName()))
    else:
        canvas.SaveAs("{}/{}.{}".format(output_directory, canvas.GetName(), ext))

###########
### FIN ###
###########
