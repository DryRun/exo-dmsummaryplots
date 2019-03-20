import os
import sys
#sys.path.append("./python/")
from ExoDMSummaryPlots.GQSummary.gq_summary_plot import GQSummaryPlot, seaborn_colors
from ExoDMSummaryPlots.GQSummary.dijet_data import DijetData
import ROOT
from ROOT import TLine

# Set all the plot styling here
style = {
	"default":{
		"line_color":1,
		"line_width":2,
		"line_style":1,
		"marker_style":20,
		"marker_size":0,
		"marker_color":1,
		"fill_style":0,
		"fill_color":0,
	}, "EXO16046_obs":{
		"line_color":seaborn_colors.get_root_color("RdPu_r", 0),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("RdPu_r", 0),		
	}, "EXO16056_narrow_obs":{
		"line_color":seaborn_colors.get_root_color("Reds_d", 2),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Reds_d", 2),		
	}, "EXO16056_narrow_lowmass_obs":{
		"line_color":seaborn_colors.get_root_color("Blues_d", 4),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Blues_d", 4),		
	}, "EXO16056_narrow_highmass_obs":{
		"line_color":seaborn_colors.get_root_color("Reds_d", 2),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Reds_d", 2),		
	}, "EXO16056_wide_obs":{
		"line_color":seaborn_colors.get_root_color("Purples_d", 3),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Purples_d", 3),		
	}, "EXO16057_SR1_obs":{
		"line_color":seaborn_colors.get_root_color("Oranges_d", 3),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Oranges_d", 3),		
	}, "EXO16057_SR2_obs":{
		"line_color":seaborn_colors.get_root_color("Oranges_d", 3),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Oranges_d", 3),		
	}, "EXO17001_obs":{
		"line_color":seaborn_colors.get_root_color("Greens_d", 2),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Greens_d", 2),		
	}, "EXO17026_obs":{
		"line_color":seaborn_colors.get_root_color("Greens_d", 0),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Greens_d", 0),		
	}, "CDF_Run1":{
		"line_color":seaborn_colors.get_root_color("Purples_d", 5),		
		"line_style":8,
		"fill_color":seaborn_colors.get_root_color("Purples_d", 5),		
	}, "CDF_Run2":{
		"line_color":seaborn_colors.get_root_color("Purples_d", 3),		
		"line_style":6,
		"fill_color":seaborn_colors.get_root_color("Purples_d", 3),
	}, "UA2":{
		"line_color":seaborn_colors.get_root_color("Oranges_d", 0),		
		"line_style":4,
		"fill_color":seaborn_colors.get_root_color("Oranges_d", 0),
	}, "EXO14005_obs":{
		"line_color":seaborn_colors.get_root_color("Blues_d", 1),
		"line_style":1, 
		"fill_color":seaborn_colors.get_root_color("Blues_d", 1),
	}, "ATLAS_8TeV":{
		"line_color":seaborn_colors.get_root_color("Greens_d", 4),
		"line_style":3, 
		"fill_color":seaborn_colors.get_root_color("Greens_d", 4),
	}, "ATLAS_EXOT1701_obs":{
		"line_color":seaborn_colors.get_root_color("Greens_d", 4),
		"line_style":2, 
		"fill_color":seaborn_colors.get_root_color("Greens_d", 4),
	}, "ATLAS_EXOT1621_obs":{
		"line_color":seaborn_colors.get_root_color("Reds_d", 3),
		"line_style":2,
		"fill_color":seaborn_colors.get_root_color("Reds_d", 3),
	}, "ATLAS_CONF16030_low_obs":{
		"line_color":seaborn_colors.get_root_color("Blues_d", 4),
		"line_style":2, 
		"fill_color":seaborn_colors.get_root_color("Blues_d", 4),
	}, "ATLAS_CONF16030_high_obs":{
		"line_color":seaborn_colors.get_root_color("Blues_d", 4),
		"line_style":2, 
		"fill_color":seaborn_colors.get_root_color("Blues_d", 4),
	}, "ATLAS_EXOT2016020_low_obs":{
		"line_color":seaborn_colors.get_root_color("Blues_d", 5),
		"line_style":2, 
		"fill_color":seaborn_colors.get_root_color("Blues_d", 5),
	}, "ATLAS_EXOT2016020_high_obs":{
		"line_color":seaborn_colors.get_root_color("Blues_d", 5),
		"line_style":2, 
		"fill_color":seaborn_colors.get_root_color("Blues_d", 5),
	}, "ATLAS_CONF16070_ISRy_obs":{
		"line_color":seaborn_colors.get_root_color("Blues_d", 2),
		"line_style":2, 
		"fill_color":seaborn_colors.get_root_color("Blues_d", 2),
	}, "ATLAS_CONF16070_ISRj_obs":{
		"line_color":seaborn_colors.get_root_color("Reds_d", 1),
		"line_style":2, 
		"fill_color":seaborn_colors.get_root_color("Reds_d", 1),
	}, "ATLAS_EXOT16033_obs":{
		"line_color":ROOT.kMagenta,
		"line_style":2, 
		"fill_color":ROOT.kMagenta,
	}, "EXO17027_obs":{
		"line_color":seaborn_colors.get_root_color("RdPu_r", 1),		
		"line_style":1,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("RdPu_r", 1),		
	}, "ATLAS_EXOT201805_incl_PhoTrig_obs":{
		"line_color":seaborn_colors.get_root_color("Blues_d", 2),
		"line_style":2, 
		"fill_color":seaborn_colors.get_root_color("Blues_d", 2),
	}, "ATLAS_EXOT201805_incl_CombTrig_obs":{
		"line_color":seaborn_colors.get_root_color("Blues_d", 2),
		"line_style":2, 
		"fill_color":seaborn_colors.get_root_color("Blues_d", 2),
	}, "ATLAS_EXOT201805_btag_PhoTrig_obs":{
		"line_color":seaborn_colors.get_root_color("Reds_d", 1),
		"line_style":2, 
		"fill_color":seaborn_colors.get_root_color("Reds_d", 1),
	}, "ATLAS_EXOT201805_btag_CombTrig_obs":{
		"line_color":seaborn_colors.get_root_color("Reds_d", 1),
		"line_style":2, 
		"fill_color":seaborn_colors.get_root_color("Reds_d", 1),
	}
}

legend_entries = {
	"EXO16046_obs":"#splitline{CMS Dijet #chi, 13 TeV}{#it{[EXO-16-046]}}",
	"EXO16056_narrow_obs":"#splitline{CMS Dijet '16, 13 TeV}{#it{[arXiv:1806.00843]}}",
	"EXO16056_narrow_lowmass_obs":"#splitline{CMS Dijet Scouting '16, 13 TeV}{#it{[arXiv:1806.00843]}}",
	"EXO16056_narrow_highmass_obs":"#splitline{CMS Dijet '16, 13 TeV}{#it{[arXiv:1806.00843]}}",
	"EXO16056_wide_obs":"#splitline{CMS Broad Dijet, 13 TeV}{#it{[arXiv:1806.00843]}}",
	"EXO16057_SR1_obs":"#splitline{CMS Dijet b tagged, 8 TeV}{#it{[arXiv:1802.06149]}}",
	"EXO16057_SR2_obs":False, # Only need one of SR1/SR2 for the legend
	"EXO17001_obs":"#splitline{CMS Boosted Dijet, 13 TeV}{#it{[arXiv:1710.00159]}}",
	"EXO17026_obs":"#splitline{CMS Dijet '16+'17, 13 TeV}{#it{[EXO-17-026]}}",
	"EXO17027_obs":"#splitline{CMS Boosted Dijet+#gamma, 13 TeV}{#it{[EXO-17-027]}}",
	"CDF_Run1":"#splitline{CDF Run1}{#it{[arXiv:hep-ex/9702004]}}", # Phys. Rev. D 55, 5263 (1997)
	"CDF_Run2":"#splitline{CDF Run2}{#it{[arXiv:0812.4036]}}", # Phys. Rev. D 79, 112002 (2009)
	"UA2":"#splitline{UA2}{#it{[Nucl. Phys. B 400, 3 (1993)]}}",
	"EXO14005_obs":"#splitline{CMS Dijet, 8 TeV}{#it{[arXiv:1604.08907]}}",
	"ATLAS_8TeV":"#splitline{ATLAS Dijet, 8 TeV}{#it{[arXiv:1407.1376]}}",
	"ATLAS_EXOT1701_obs":"#splitline{ATLAS Boosted Dijet, 13 TeV}{#it{[arXiv:1801.08769]}}",
	"ATLAS_EXOT1621_obs":"#splitline{ATLAS Dijet, 13 TeV}{#it{[arXiv:1703.09127]}}",
	"ATLAS_CONF16030_low_obs":"#splitline{ATLAS Dijet TLA, 13 TeV}{#it{[ATLAS-CONF-2016-030]}}",
	"ATLAS_CONF16030_high_obs":False,
	"ATLAS_EXOT2016020_low_obs":"#splitline{ATLAS Dijet TLA, 13 TeV}{#it{[arXiv:1804.03496]}}",
	"ATLAS_EXOT2016020_high_obs":False,
	"ATLAS_EXOT16033_obs":"#splitline{ATLAS Dijet b tagged, 13 TeV}{#it{[arXiv:1805.09299]}}",
	"ATLAS_CONF16070_ISRy_obs":"#splitline{ATLAS Dijet+ISR #gamma, 13 TeV}{#it{[ATLAS-CONF-2016-070]}}",
	"ATLAS_CONF16070_ISRj_obs":"#splitline{ATLAS Dijet+ISR j, 13 TeV}{#it{[ATLAS-CONF-2016-070]}}",
	"ATLAS_EXOT201805_incl_PhoTrig_obs":"#splitline{ATLAS Dijet+ISR #gamma, 13 TeV}{#it{[arXiv:1901.10917]}}",
	"ATLAS_EXOT201805_incl_CombTrig_obs":False,
	"ATLAS_EXOT201805_btag_PhoTrig_obs":"#splitline{ATLAS bb+ISR #gamma, 13 TeV}{#it{[arXiv:1901.10917]}}",
	"ATLAS_EXOT201805_btag_CombTrig_obs":False,
	"_GOM100":"#frac{#scale[1.1]{#bf{#Gamma_{Z'}#kern[-0.5]{ }/#kern[-0.5]{ }M_{Z'}#kern[-0.5]{ }<#kern[-0.5]{ }~100%}}}{}",
	"_GOM30":"#frac{#scale[1.1]{#bf{#Gamma_{Z'}#kern[-0.5]{ }/#kern[-0.5]{ }M_{Z'}#kern[-0.5]{ }<#kern[-0.5]{ }~30%}}}{}",
	"_GOM10":"#frac{#scale[1.1]{#bf{#Gamma_{Z'}#kern[-0.5]{ }/#kern[-0.5]{ }M_{Z'}#kern[-0.5]{ }<#kern[-0.5]{ }~10%}}}{}",
	"_GOMall":"#frac{#scale[1.1]{#bf{All #Gamma_{Z'}#kern[-0.5]{ }/#kern[-0.5]{ }M_{Z'}}}}{}",
	"_empty":"",
}

# Maximum Gamma/M values
max_gom = {
	"EXO16056_narrow_obs":0.12,
	"EXO16056_narrow_lowmass_obs":0.12,
	"EXO16056_narrow_highmass_obs":0.12,
	"EXO16056_wide_obs":0.3,
	"EXO16057_SR1_obs":0.12,
	"EXO16057_SR2_obs":0.12,
	"EXO17001_obs":0.12,
	"EXO14005_obs":0.12,
	"CDF_Run1":0.12,
	"CDF_Run2":0.12,
	"UA2":0.12,
	"ATLAS_8TeV":0.12,
	"ATLAS_EXOT1621_obs":0.12,
	"ATLAS_EXOT1701_obs":0.12,
	"ATLAS_EXOT201805_incl_PhoTrig_obs":0.12,
	"ATLAS_EXOT201805_incl_CombTrig_obs":0.12,
	"ATLAS_EXOT201805_btag_PhoTrig_obs":0.12,
	"ATLAS_EXOT201805_btag_CombTrig_obs	":0.12,
	"EXO16046_obs":1.0,
}

# Maximum gq values 
max_gq = {
	"EXO16046_obs":1.45,
	"CDF_Run1":2.5/6,
	"CDF_Run2":2.5/6,
	"UA2":2.5/6,
}

if __name__ == "__main__":
	from argparse import ArgumentParser
	parser = ArgumentParser(description='Make g_q summary plot')
	parser.add_argument('--analyses', type=str, default="\
_GOM100,ATLAS_EXOT1701_obs,\
EXO16046_obs,ATLAS_EXOT1621_obs,\
_GOM10,ATLAS_CONF16030_low_obs,ATLAS_CONF16030_high_obs,\
EXO16056_narrow_obs,ATLAS_CONF16070_ISRy_obs,\
EXO14005_obs,ATLAS_CONF16070_ISRj_obs,\
EXO16057_SR1_obs,UA2,\
EXO17001_obs,CDF_Run1,\
CDF_Run2,EXO16057_SR2_obs", 
		help="Analyses to plot (CADI lines, comma-separated)") 
	# _GOM30,EXO16056_wide_obs - didn't make Moriond
	parser.add_argument('--logx', action='store_true', help='Log x')
	parser.add_argument('--logy', action='store_true', help='Log y')
	parser.add_argument('--goms', type=str, default="0.1,0.3", help='List of Gamma/M values to draw')
	parser.add_argument('--gom_fills', action='store_true', help='Draw fills for exclusions with Gamma/M or gq upper bound')	
	parser.add_argument('--save_tag', type=str, default="", help='Tag for saving')
	cms_label_group = parser.add_mutually_exclusive_group(required=False)
	cms_label_group.add_argument('--cms', action='store_true', help="Draw CMS label")
	cms_label_group.add_argument('--cms_text', type=str, help="Draw CMS label with extra text")
	parser.add_argument('--conference_label', type=str, default="", help="Text for specifying conference or time period")
	args = parser.parse_args()

	gq_plot = GQSummaryPlot("gq_all_2c{}".format(args.save_tag))

	# If args.goms_fills is specified, don't draw the "line_width=402" style fill
	if args.gom_fills:
		for style_name in style:
			style[style_name]["line_width"] = 2

	# Load data
	analysis_data = {}
	analyses = args.analyses.split(",")
	for analysis in analyses:
		# Dummy entries: just go in legend, no actual data
		if len(analysis) == 0:
			print "ERROR : analyses contains zero length string."
			print analyses
		if analysis[0] == "_":
			gq_plot.add_legend_only(analysis, legend_entries[analysis])
			continue

		analysis_data[analysis] = DijetData(analysis)
		if args.gom_fills and analysis in max_gom:
			this_max_gom_fill = max_gom[analysis]
		else:
			this_max_gom_fill = False
		if args.gom_fills and analysis in max_gq:
			this_max_gq_fill = max_gq[analysis]
		else:
			this_max_gq_fill = False

		# Max g_q values for curves, if not drawing fills
		if not args.gom_fills:
			if analysis in max_gq:
				this_max_gq = max_gq[analysis]
			else:
				this_max_gq = False
		analysis_data[analysis].load_data(os.path.expandvars("$CMSSW_BASE/src/ExoDMSummaryPlots/GQSummary/data/{}.dat".format(analysis)))
		gq_plot.add_data(analysis_data[analysis], analysis, legend_entries[analysis], max_gq=this_max_gq, max_gom_fill=this_max_gom_fill, max_gq_fill=this_max_gq_fill)

	# Style the plot
	gq_plot.set_style(style)
	gq_plot.set_width_curves([float(x) for x in args.goms.split(",")])
	if args.cms:
		cms_label_option = ""
	elif args.cms_text:
		cms_label_option = args.cms_text
	else:
		cms_label_option = False

	if args.logx:
		gq_plot.draw(
			logx=args.logx, 
			logy=args.logy, 
			draw_cms=cms_label_option,
			x_title="M_{Z'} [GeV]",
			y_title="g'_{q}",
			x_range=[7., 8000.],
			y_range=[0.03, 2.],
			canvas_dim=[2640, 1200],
			canvas_rm=0.4,
			legend_coords=[0.61, 0.02, 0.99, 0.98],
			legend_text_size=0.024,
			legend_ncolumns=2,
			legend_header="#scale[1.2]{#bf{95% CL exclusions}}",
			draw_Z_constraint=True,
			draw_upsilon_constraint=True,
			gom_x=60.,
			model_label={"x":2100., "y":0.045, "text":"Z'#rightarrowq#bar{q}", "size_modifier":1.5},
			gom_fills=args.gom_fills,
			conference_label={"x":1500., "y":2. * 1.1, "text":args.conference_label}			
			)
	else:
		gq_plot.draw(
			logx=args.logx, 
			logy=args.logy, 
			draw_cms=cms_label_option,
			x_title="M_{Z'} [GeV]",
			y_title="g'_{q}",
			x_range=[0., 5500.],
			y_range=[0.03, 2.],
			canvas_dim=[2640, 1200],
			canvas_rm=0.4,
			legend_coords=[0.61, 0.02, 0.99, 0.98],
			legend_text_size=0.024,
			legend_ncolumns=2,
			legend_header="#scale[1.2]{#bf{95% CL exclusions}}",
			draw_Z_constraint=True,
			draw_upsilon_constraint=True,
			gom_x=4500.,
			model_label={"x":4200., "y":0.05, "text":"Z'#rightarrowq#bar{q}", "size_modifier":1.5},
			gom_fills=args.gom_fills,
			conference_label={"x":3900., "y":2. * 1.1, "text":args.conference_label}
			)

	gq_plot.save(os.path.expandvars("$CMSSW_BASE/src/ExoDMSummaryPlots/GQSummary/plots"), exts=["pdf", "png", "eps"])


