'''
Inputs from dilepton analyzers = limit curves for a range of widths
This class computes the 2D limit contours for the mDM vs mZ' plot.
'''
import numpy as np 
import os
import sys

class DileptonConverter:
	def __init__(self, scenario):
		self._scenario = scenario
		if not self._scenario in ["V2", "A2"]:
			raise ValueError("Unknown scenario {}".format(self._scenario))

		if self._scenario == "V2":
			self._gq = 0.25
			self._gl = 0.1
			self._gDM = 1.0
			self._vtype = "vector"
		elif self._scenario == "A2":
			self._gq = 0.25
			self._gl = 0.1
			self._gDM = 1.0
			self._vtype = "axial"

	def load_lllimits(self, input_path_dict):
		# input_path_dict = {0.01: path_to_0.01_limits, ...}
		# Returns dict {width: TGraph}

		width_graphs = {}
		for width, path in input_path_dict.iteritems():
			data = np.loadtxt(path)
			limits = 








			   data = numpy.loadtxt(path_to_file)

   limit = {}
   for entry in data:
      mass = int(entry[0])
      lim = float(entry[1])
      if(not (mass in limit.keys())):
         limit[mass]=[]
      limit[mass].append(lim)

   for key in limit.keys():
      limit[key] = numpy.percentile(limit[key],quantile,interpolation="midpoint")

   return limit


def load_dilepton_limits(path_to_file,quantile=50):
   import numpy
   data = numpy.loadtxt(path_to_file)

   limit = {}
   for entry in data:
      mass = int(entry[0])
      lim = float(entry[1])
      if(not (mass in limit.keys())):
         limit[mass]=[]
      limit[mass].append(lim)

   for key in limit.keys():
      limit[key] = numpy.percentile(limit[key],quantile,interpolation="midpoint")

   return limit





def make_contour_plot(scenario,dmsimp_xs,limits,smooth,tag):
	### Setup
	output_folder = "./output/variable_width/{TAG}/contour_plot".format(TAG=tag)
	if ( not os.path.exists(output_folder) ): os.makedirs(output_folder)
	create_tdr_style()

	graphs_xs = make_xs_graphs(dmsimp_xs,scenario)




	contours = {}
	for quantile in limits.keys():
		mmeds = set()
		for l in limits[quantile].values():
			mmeds = mmeds.union(set(l.keys()))
		if(quantile != "obs"):
			mmeds = range(min(mmeds),max(mmeds),10)
		graphs_limit = get_variable_width_limit_graph(graphs_xs,limits[quantile],scenario,output_folder+"/control_"+quantile,False)


                find_exclusion_control(mmeds,graphs_xs, graphs_limit,output_folder,tag=scenario+"_"+quantile)

		graphs_outline = find_contour(mmeds,graphs_xs,graphs_limit)
                for g in graphs_outline:
                        g.SetMarkerStyle(25)
                        g.SetMarkerSize(1)
                        g.SetLineWidth(3)
                        g.SetMarkerColor(r.kBlack)
		contours[quantile] = graphs_outline


	contours_smoothed = {}
	if(smooth):
		for quantile, graphs in contours.items():
                        if(not quantile in contours_smoothed.keys()):
                                contours_smoothed[quantile] = []
                        for g in graphs:
                                g_smooth = do_smoothing(g)
                                contours_smoothed[quantile].append(g_smooth)
                                g_smooth.SetLineWidth(3)

        f = r.TFile("{OUT}/contours_dilepton_{SCENARIO}{SMOOTH}.root".format(OUT=output_folder,SCENARIO=scenario,SMOOTH=("_smooth" if smooth else "")),"RECREATE")
	f.cd()
	if(smooth):
		for quantile,contourlist in contours_smoothed.items():
                        for i,contour in enumerate(contourlist):
                                contour.Write(quantile+str(i))
	else:
		for quantile,contourlist in contours.items():
                        for i,contour in enumerate(contourlist):
                                contour.Write(quantile+str(i))
	f.Close()
