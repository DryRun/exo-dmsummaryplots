import os
import sys
#sys.path.append("../python/")
from ExoDMSummaryPlots.GQSummary.gq_summary_plot import GQSummaryPlot, seaborn_colors
from ExoDMSummaryPlots.GQSummary.dijet_data import DijetData

# Set all the plot styling here
style = {
	"default":{
		"line_color":1,
		"line_width":402,
		"line_style":1,
		"marker_style":20,
		"marker_size":0,
		"marker_color":1,
		"fill_style":3004,
		"fill_color":0,
	}, "EXO16046_obs":{
		"line_color":seaborn_colors.get_root_color("Blues_d", 1),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Blues_d", 1),		
	}, "EXO16046_exp":{
		"line_color":seaborn_colors.get_root_color("Blues_d", 4),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Blues_d", 4),		
	}, "EXO16056_narrow_obs":{
		"line_color":seaborn_colors.get_root_color("Reds_d", 3),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Reds_d", 3),		
	}, "EXO16056_narrow_exp":{
		"line_color":seaborn_colors.get_root_color("Reds_d", 5),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Reds_d", 5),		
	}, "EXO16056_narrow_lowmass_obs":{
		"line_color":seaborn_colors.get_root_color("Reds_d", 1),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Reds_d", 1),		
	}, "EXO16056_narrow_lowmass_exp":{
		"line_color":seaborn_colors.get_root_color("Reds_d", 3),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Reds_d", 3),		
	}, "EXO16056_narrow_highmass_obs":{
		"line_color":seaborn_colors.get_root_color("Reds_d", 2),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Reds_d", 2),		
	}, "EXO16056_narrow_highmass_exp":{
		"line_color":seaborn_colors.get_root_color("Reds_d", 5),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Reds_d", 5),		
	}, "EXO16056_wide_obs":{
		"line_color":seaborn_colors.get_root_color("Purples_d", 3),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Purples_d", 3),		
	}, "EXO16056_wide_exp":{
		"line_color":seaborn_colors.get_root_color("Purples_d", 5),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Purples_d", 5),		
	}, "EXO16057_SR1_obs":{
		"line_color":seaborn_colors.get_root_color("Oranges_d", 3),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Oranges_d", 3),		
	}, "EXO16057_SR1_exp":{
		"line_color":seaborn_colors.get_root_color("Oranges_d", 5),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Oranges_d", 5),		
	}, "EXO16057_SR2_obs":{
		"line_color":seaborn_colors.get_root_color("Oranges_d", 3),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Oranges_d", 3),		
	}, "EXO16057_SR2_exp":{
		"line_color":seaborn_colors.get_root_color("Oranges_d", 5),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Oranges_d", 5),		
	}, "EXO17001_obs":{
		"line_color":seaborn_colors.get_root_color("Greens_d", 2),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Greens_d", 2),		
	}, "EXO17001_exp":{
		"line_color":seaborn_colors.get_root_color("Greens_d", 5),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Greens_d", 5),		
	}, "EXO14005_obs":{
		"line_color":seaborn_colors.get_root_color("Blues_d", 3),
		"line_style":1, 
		"fill_color":seaborn_colors.get_root_color("Blues_d", 3),
	}, "EXO14005_exp":{
		"line_color":seaborn_colors.get_root_color("Blues_d", 5),
		"line_style":2, 
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Blues_d", 5),
	}, "EXO17026_obs":{
		"line_color":seaborn_colors.get_root_color("Greens_d", 0),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("Greens_d", 0),		
	}, "EXO17026_exp":{
		"line_color":seaborn_colors.get_root_color("Greens_d", 4),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("Greens_d", 4),		
	}, "EXO17027_obs":{
		"line_color":seaborn_colors.get_root_color("RdPu_r", 1),		
		"line_style":1,
		"fill_color":seaborn_colors.get_root_color("RdPu_r", 1),		
	}, "EXO17027_exp":{
		"line_color":seaborn_colors.get_root_color("RdPu_r", 3),		
		"line_style":2,
		"line_width":2,
		"fill_color":seaborn_colors.get_root_color("RdPu_r", 3),		
	}
}

legend_entries = {
	"EXO16046_obs":"#splitline{Dijet #chi #it{[EXO-16-046]}}{35.9 fb^{-1}, 13 TeV}",
	"EXO16046_exp":False,
	"EXO16056_narrow_obs":"#splitline{Dijet #it{[arXiv:1806.00843]}}{35.9 fb^{-1}, 13 TeV}",
	"EXO16056_narrow_lowmass_obs":"#splitline{Dijet scouting #it{[arXiv:1806.00843]}}{35.9 fb^{-1}, 13 TeV}",
	"EXO16056_narrow_highmass_obs":"#splitline{Dijet #it{[arXiv:1806.00843]}}{35.9 fb^{-1}, 13 TeV}",
	"EXO16056_narrow_exp":False,
	"EXO16056_narrow_lowmass_exp":False,
	"EXO16056_narrow_highmass_exp":False,
	"EXO16056_wide_obs":"#splitline{Broad Dijet #it{[arXiv:1806.00843]}}{35.9 fb^{-1}, 13 TeV}",
	"EXO16056_wide_exp":False,
	"EXO16057_SR1_obs":"#splitline{Dijet b-tagged #it{[arXiv:1802.06149]}}{19.7 fb^{-1}, 8 TeV}",
	"EXO16057_SR1_exp":False,
	"EXO16057_SR2_obs":False, # Only need one of SR1/SR2 for the legend
	"EXO16057_SR2_exp":False,
	"EXO17001_obs":"#splitline{Boosted Dijet #it{[arXiv:1710.00159]}}{35.9 fb^{-1}, 13 TeV}",
	"EXO17001_exp":False,
	"EXO14005_obs":"#splitline{Dijet scouting #it{[arXiv:1604.08907]}}{19.7 fb^{-1}, 8 TeV}",
	"EXO14005_exp":False,
	"EXO17026_obs":"#splitline{Dijet #it{[EXO-17-026]}}{77.8 fb^{-1}, 13 TeV}",
	"EXO17026_exp":False,
	"EXO17027_obs":"#splitline{Boosted Dijet+#gamma #it{[EXO-17-027]}}{35.9 fb^{-1}, 13 TeV}",
	"EXO17027_exp":False,
	"_GOM100":"#frac{#scale[1.1]{#bf{#Gamma_{Z'}#kern[-0.5]{ }/#kern[-0.5]{ }M_{Z'}#kern[-0.5]{ }<#kern[-0.5]{ }~100%}}}{}",
	"_GOM30":"#frac{#scale[1.1]{#bf{#Gamma_{Z'}#kern[-0.5]{ }/#kern[-0.5]{ }M_{Z'}#kern[-0.5]{ }<#kern[-0.5]{ }~30%}}}{}",
	"_GOM10":"#frac{#scale[1.1]{#bf{#Gamma_{Z'}#kern[-0.5]{ }/#kern[-0.5]{ }M_{Z'}#kern[-0.5]{ }<#kern[-0.5]{ }~10%}}}{}",
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
}

# Maximum gq values 
max_gq = {
	"EXO16046_obs":1.45,
}

analyses = "_GOM10,EXO17027_obs,EXO17027_exp,\
EXO17001_obs,EXO17001_exp,\
EXO16057_SR1_obs,EXO16057_SR1_exp,\
EXO16057_SR2_obs,EXO16057_SR2_exp,\
EXO14005_obs,EXO14005_exp,\
EXO16056_narrow_lowmass_obs,\
EXO16056_narrow_lowmass_exp,\
EXO16056_narrow_highmass_obs,\
EXO16056_narrow_highmass_exp,\
EXO17026_obs,EXO17026_exp,\
_GOM30,EXO16056_wide_obs,\
EXO16056_wide_exp,\
_GOM100,EXO16046_obs,\
EXO16046_exp"



if __name__ == "__main__":
	from argparse import ArgumentParser
	parser = ArgumentParser(description='Make g_q summary plot')
	parser.add_argument('--analyses', type=str, default=analyses, help="Analyses to plot (CADI lines, comma-separated)") 
	# _GOM30,EXO16056_wide_obs,EXO16056_wide_exp - didn't make Moriond
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

	gq_plot = GQSummaryPlot("gq_cms{}".format(args.save_tag))

	# If args.goms_fills is specified, don't draw the "line_width=402" style fill
	if args.gom_fills:
		for style_name in style:
			style[style_name]["line_width"] = 2

	# Load data
	analysis_data = {}
	analyses = args.analyses.split(",")
	for analysis in analyses:
		# Dummy entries: just go in legend, no actual data
		if analysis[0] == "_":
			gq_plot.add_legend_only(analysis, legend_entries[analysis])
			continue

		analysis_data[analysis] = DijetData(analysis)
		analysis_data[analysis].load_data(os.path.expandvars("$CMSSW_BASE/src/ExoDMSummaryPlots/GQSummary/data/{}.dat".format(analysis)))
		# Max Gamma/M fill
		if args.gom_fills and analysis in max_gom:
			this_max_gom_fill = max_gom[analysis]
		else:
			this_max_gom_fill = False

		# Max gq and fill
		this_max_gq_fill = False
		this_max_gq = False
		if analysis in max_gq:
			this_max_gq = max_gq[analysis]
			if args.gom_fills:
				this_max_gq_fill = max_gq[analysis]

		gq_plot.add_data(analysis_data[analysis], analysis, legend_entries[analysis], max_gom_fill=this_max_gom_fill, max_gq=this_max_gq, max_gq_fill=this_max_gq_fill)

	# Style the plot
	gq_plot.set_style(style)
	gq_plot.set_width_curves([float(x) for x in args.goms.split(",")])
	if args.cms:
		cms_label_option = ""
	elif args.cms_text:
		cms_label_option = args.cms_text
	else:
		cms_label_option = False
	if args.logy:
		y_range = [0.03, 2.]
	else:
		y_range = [0., 1.7]
	if args.logx:
		gq_plot.draw(
			logx=args.logx, 
			logy=args.logy, 
			draw_cms=cms_label_option,
			x_title="M_{Z'} [GeV]",
			y_title="g'_{q}",
			x_range=[6., 8000.],
			y_range=y_range,
			canvas_dim=[1800, 1200],
			legend_coords=[0.69, 0.02, 0.99, 0.95],
			legend_text_size=0.025,
			legend_obsexp=True,
			model_label={"x":2000., "y":0.05, "text":"Z'#rightarrowq#bar{q}"},
			gom_x=60.,
			gom_fills=args.gom_fills,
			conference_label={"x":900., "y":y_range[1] * 1.1, "text":args.conference_label}
			)
	else:
		gq_plot.draw(
			logx=args.logx, 
			logy=args.logy, 
			draw_cms=cms_label_option,
			x_title="M_{Z'} [GeV]",
			y_title="g'_{q}",
			x_range=[0., 6000.],
			y_range=y_range,
			canvas_dim=[1800, 1200],
			legend_coords=[0.69, 0.02, 0.99, 0.95],
			legend_text_size=0.025,
			legend_obsexp=True,
			model_label={"x":4500., "y":0.05, "text":"Z'#rightarrowq#bar{q}"},
			gom_x=1250.,
			gom_fills=args.gom_fills,
			conference_label={"x":4000., "y":y_range[1] * 1.1, "text":args.conference_label},
			)
	gq_plot.save(os.path.expandvars("$CMSSW_BASE/src/ExoDMSummaryPlots/GQSummary/plots"), exts=["pdf", "png", "eps"])


