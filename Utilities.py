from ROOT import *
import ast

def extrapolation( tgraph, DijetOnly, Resonances, metless, metx, mDM_lb ):

    DDgraph_extr = {}
    num_extr = 100

####################
## MET+X
#Step1 : Extrapolate from first non -100 point downto mDM_lb)
####################
    if not DijetOnly :
        for analysis in metx :
            print "Analysis ", analysis
            DDgraph_extr[analysis]=TGraph()
            #extrapolation based on the first point
            mDM_ref  = Double(0)
            xsec_ref = Double(0)
            tgraph[analysis].GetPoint(0,mDM_ref,xsec_ref);
            mR_ref = 0.939*mDM_ref/(0.939+mDM_ref);
            for i in range(0, num_extr) :
                mDM_i = mDM_lb + i*(mDM_ref-mDM_lb)/num_extr
                mR_i = 0.939*mDM_i/(0.939+mDM_i);
                xsec_i = xsec_ref*(mR_i*mR_i)/(mR_ref*mR_ref)
                DDgraph_extr[analysis].SetPoint(i,mDM_i,xsec_i)
                for i in range(0,tgraph[analysis].GetN()) :
                    mDM  = Double(0)
                    xsec  = Double(0)
                    tgraph[analysis].GetPoint(i,mDM,xsec)
                    DDgraph_extr[analysis].SetPoint(i+num_extr,mDM,xsec)

            tgraph[analysis] = DDgraph_extr[analysis]
####################


    if not Resonances :
        return

####################
## Dijet,Trijet:
#[N.B: Step 1, 2a, 3 applies to Trijet]
#Step1 : Extrapolate from first non -100 point downto mDM_lb)
#Step2 :
  #a) copy input graphs into new one;
  #b) extrapolate downward from i-1 to mDM_lb (N.B: MDM_i=-100
  #c) extrapolate upward from i+1 to mDM_lb (N.B: MDM_i=-100)
#Step3 : Extrapolate from point N-1 downto mDM_lb
#[N.B: discarding point N since it's equal to N-1]
####################


    index = 0 #keeps track of the index for filling graph
    for analysis in metless :
        index = 0
        print "Analysis ", analysis
        DDgraph_extr[analysis]=TGraph()


        #Step 1

        mDM_ref  = Double(0)
        xsec_ref = Double(0)
        tgraph[analysis].GetPoint(1,mDM_ref,xsec_ref);
        mR_ref = 0.939*mDM_ref/(0.939+mDM_ref);
        for i_extr in range(0, num_extr) :
            mDM_i_extr = mDM_lb + i_extr*(mDM_ref-mDM_lb)/num_extr
            mR_i_extr = 0.939*mDM_i_extr/(0.939+mDM_i_extr);
            xsec_i_extr = xsec_ref*(mR_i_extr*mR_i_extr)/(mR_ref*mR_ref)
#            print "i = ", i_extr, " extrapolating with mDM_i = ", mDM_i_extr, "xsec_i = ", xsec_i_extr
            index = i_extr
#            print "index ", index
            DDgraph_extr[analysis].SetPoint(index,mDM_i_extr,xsec_i_extr)

        #Step2

        for i in range(1,tgraph[analysis].GetN()-2) :
            mDM_i  = Double(0)
            xsec_i  = Double(0)
            mDM_im1  = Double(0)
            xsec_im1  = Double(0)
            mDM_ip1  = Double(0)
            xsec_ip1  = Double(0)
            tgraph[analysis].GetPoint(i,mDM_i,xsec_i)
            if i != 0 :
                tgraph[analysis].GetPoint(i-1,mDM_im1,xsec_im1)
            else :
                mDM_im1 = -999
                xsec_im1 = -999
            if i != tgraph[analysis].GetN()-1 :
                tgraph[analysis].GetPoint(i+1,mDM_ip1,xsec_ip1)
            else :
                mDM_ip1 = -999
                xsec_ip1 = -999

            #copy input graphs
            if mDM_i != -100 :
                #print "Step 2a: Copy input graphs"
                index = index + 1
                DDgraph_extr[analysis].SetPoint(index,mDM_i,xsec_i)


            #extrapolation:
            if mDM_i == -100 :
                #from previous point (i-1) down mDM_lb
                if mDM_im1 !=-100 :
                    #print "Step 2b: Extrpolate downward from i-1 to mDM_lb"
                    mDM_ref  = Double(0)
                    xsec_ref  = Double(0)
                    tgraph[analysis].GetPoint(i-1,mDM_ref,xsec_ref);
                    mR_ref = 0.939*mDM_ref/(0.939+mDM_ref);
                    for i_extr in range(0, num_extr+1) :
                        mDM_i_extr = mDM_lb + (num_extr-i_extr)*(mDM_ref-mDM_lb)/(num_extr)
                        mR_i_extr = 0.939*mDM_i_extr/(0.939+mDM_i_extr);
                        xsec_i_extr = xsec_ref*(mR_i_extr*mR_i_extr)/(mR_ref*mR_ref)
                        index = index + 1
                        DDgraph_extr[analysis].SetPoint(index,mDM_i_extr,xsec_i_extr)

                #from subsequent point (i+1) up to mDM_lb
                elif mDM_ip1 !=-100 :
                    #print "Step 2b: Extrpolate Upward from i+1 to mDM_lb"
                    mDM_ref  = Double(0)
                    xsec_ref  = Double(0)
                    tgraph[analysis].GetPoint(i+1,mDM_ref,xsec_ref);
                    mR_ref = 0.939*mDM_ref/(0.939+mDM_ref);
                    for i_extr in range(0, num_extr) :
                        mDM_i_extr = mDM_lb + i_extr*(mDM_ref-mDM_lb)/(num_extr)
                        mR_i_extr = 0.939*mDM_i_extr/(0.939+mDM_i_extr);
                        xsec_i_extr = xsec_ref*(mR_i_extr*mR_i_extr)/(mR_ref*mR_ref)
                        index = index + 1
                        DDgraph_extr[analysis].SetPoint(index,mDM_i_extr,xsec_i_extr)


        tgraph[analysis] = DDgraph_extr[analysis]


    #Step 3

    for analysis in metless :
        DDgraph_extr[analysis]=TGraph()
        #copy the graph up to N-3 included (lower xsec band)
        for i in range(0,tgraph[analysis].GetN()-2) :
            mDM  = Double(0)
            xsec  = Double(0)
            tgraph[analysis].GetPoint(i,mDM,xsec)
            DDgraph_extr[analysis].SetPoint(i,mDM,xsec)
        #remove the last -100
        for i in range(tgraph[analysis].GetN()-2,tgraph[analysis].GetN()-1) :
            mDM  = Double(0)
            xsec  = Double(0)
            tgraph[analysis].GetPoint(i,mDM,xsec)
            DDgraph_extr[analysis].SetPoint(i,mDM,xsec)

        extrafac = 5000

        mDM_ref  = Double(0)
        xsec_ref = Double(0)
        tgraph[analysis].GetPoint(tgraph[analysis].GetN()-2,mDM_ref,xsec_ref);
        mR_ref = 0.939*mDM_ref/(0.939+mDM_ref); #~ mn
        for i in range(0, num_extr*extrafac) :
            mDM_i = mDM_lb + (num_extr*extrafac-1-i)*(mDM_ref-mDM_lb)/(num_extr*extrafac)
            mR_i = 0.939*mDM_i/(0.939+mDM_i);
            xsec_i = xsec_ref*(mR_i*mR_i)/(mR_ref*mR_ref)
            DDgraph_extr[analysis].SetPoint(i+1+tgraph[analysis].GetN()-2,mDM_i,xsec_i)

        tgraph[analysis] = DDgraph_extr[analysis]

        # print "REPRINT GRAPH"
        # for i in range(0,tgraph[analysis].GetN()) :
        #     mDM  = Double(0)
        #     xsec  = Double(0)
        #     tgraph[analysis].GetPoint(i,mDM,xsec)
        #     print "REPRINT: mDM = ", mDM, "xsec = ", xsec



def rescale_graph_axis(graph,rescale_x=1,rescale_y=1):
	import ROOT as r
	g = r.TGraph()
	for i in range(graph.GetN()):
		x = r.Double()
		y = r.Double()
		graph.GetPoint(i,x,y)
		g.SetPoint(i,rescale_x * x, rescale_y * y)
	return g


def read_graphs():
	import ROOT as r

	### Initialize
	graphs = {}
	scenarios = ["A1", "A2", "V1", "V2"]
	quantiles = ["obs", "exp"]
	analyses = ["monojet","monophoton","monoz","dilepton","dijet","monoHgg","monotop","dijet","trijet","dijetchi","relic"]
	for a in analyses:
		graphs[a] = {}
		for s in scenarios:
			graphs[a][s] = {}
			for q in quantiles:
				graphs[a][s][q] = None


	graphs["monojet"]["A1"]["obs"] = TFile("Monojet/EXO-16-048/ScanMM/scan2D_axial.root").Get("contour_observed")
	graphs["monojet"]["A1"]["exp"] = TFile("Monojet/EXO-16-048/ScanMM/scan2D_axial.root").Get("contour_expected")
	graphs["monojet"]["V1"]["obs"] = TFile("Monojet/EXO-16-048/ScanMM/scan2D_vector.root").Get("contour_observed")
	graphs["monojet"]["V1"]["exp"] = TFile("Monojet/EXO-16-048/ScanMM/scan2D_vector.root").Get("contour_expected")

	graphs["dilepton"]["A2"]["obs"] = rescale_graph_axis(TFile("Dilepton/EXO-16-031/ScanMM/contours_dilepton_A2_smooth.root").Get("obs"),1e-3,1e-3)
	graphs["dilepton"]["A2"]["exp"] = rescale_graph_axis(TFile("Dilepton/EXO-16-031/ScanMM/contours_dilepton_A2_smooth.root").Get("exp"),1e-3,1e-3)
	graphs["dilepton"]["V2"]["obs"] = rescale_graph_axis(TFile("Dilepton/EXO-16-031/ScanMM/contours_dilepton_V2_smooth.root").Get("obs"),1e-3,1e-3)
	graphs["dilepton"]["V2"]["exp"] = rescale_graph_axis(TFile("Dilepton/EXO-16-031/ScanMM/contours_dilepton_V2_smooth.root").Get("exp"),1e-3,1e-3)


	graphs["monoz"]["A1"]["obs"] = r.TGraph("MonoZll/EXO-16-052/ScanMM/monoz_contour_observed_limit_axial_cl95.txt")
	graphs["monoz"]["A1"]["exp"] = r.TGraph("MonoZll/EXO-16-052/ScanMM/monoz_contour_observed_limit_axial_cl95.txt")
	graphs["monoz"]["V1"]["obs"] = r.TGraph("MonoZll/EXO-16-052/ScanMM/monoz_contour_observed_limit_vector_cl95.txt")
	graphs["monoz"]["V1"]["exp"] = r.TGraph("MonoZll/EXO-16-052/ScanMM/monoz_contour_observed_limit_vector_cl95.txt")

	graphs["monophoton"]["A1"]["obs"] =TFile("Monophoton/ScanMM/Monophoton_A_MM_ICHEP2016_obs.root").Get("monophoton_obs")
	graphs["monophoton"]["V1"]["obs"] =TFile("Monophoton/ScanMM/Monophoton_V_MM_ICHEP2016_obs.root").Get("monophoton_obs")


	graphs["monoHgg"]["V1"]["obs"] = TFile("MonoHgg/ScanMM/input_combo_MonoHgg_25April.root").Get("observed_baryonic_MonoHgg")

	graphs["monotop"]["V1"]["obs"] = TFile("Monotop/ScanMM/fcnc2d_obs_vector.root").Get("observed")

	graphs["dijet"]["A1"]["obs"] = TFile("Dijet/ScanMM/Dijet_MM_A_Dijetpaper2016_obs.root").Get("Obs_90")
	graphs["dijet"]["V1"]["obs"] = TFile("Dijet/ScanMM/Dijet_MM_A_Dijetpaper2016_obs.root").Get("Obs_90")

	graphs["dijetchi"]["A1"]["obs"] = TFile("DijetChi/ScanMM/limitsLHC_DMAxial_MDM_MMed_MT.root").Get("obs_MvsM")
	graphs["dijetchi"]["V1"]["obs"] = TFile("DijetChi/ScanMM/limitsLHC_DMVector_MDM_MMed_MT.root").Get("obs_MvsM")

	graphs["trijet"]["V1"]["obs"] = TFile("Trijet/ScanMM/MMedMDM_av.root").Get("obs_025")
	graphs["trijet"]["V1"]["obs"] = TFile("Trijet/ScanMM/MMedMDM_v.root").Get("obs_025")

	graphs["relic"]["A1"]["obs"] = TFile("Relic/madDMv2_0_6/relic_A1.root").Get("mytlist").At(0)
	graphs["relic"]["A2"]["obs"] = TFile("Relic/madDMv2_0_6/relic_A2.root").Get("mytlist").At(0)
	graphs["relic"]["V1"]["obs"] = TFile("Relic/madDMv2_0_6/relic_V1.root").Get("mytlist").At(0)
	graphs["relic"]["V2"]["obs"] = TFile("Relic/madDMv2_0_6/relic_V2.root").Get("mytlist").At(0)


	return graphs

def read_relic_lists():
	import ROOT as r
	lists = {}
	lists["A1"] = TFile("Relic/madDMv2_0_6/relic_A1.root").Get("mytlist")
	lists["A2"] = TFile("Relic/madDMv2_0_6/relic_A2.root").Get("mytlist")
	lists["V1"] = TFile("Relic/madDMv2_0_6/relic_V1.root").Get("mytlist")
	lists["V2"] = TFile("Relic/madDMv2_0_6/relic_V2.root").Get("mytlist")
	return lists
