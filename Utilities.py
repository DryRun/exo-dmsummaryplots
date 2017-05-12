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

        extrafac = 10

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

def add_text(x1, x2, y1, y2, TEXT, color=1, alignment=22, angle = 0, argument="NDC"):
   import ROOT as r
   T = r.TPaveText(x1,y1,x2,y2, argument);
   T.SetFillColor(0);
   T.SetFillStyle(0);
   T.SetLineColor(0);
   T.SetTextAlign(alignment);
   T.SetTextColor(color);

   if (not isinstance(TEXT, str)):
      for this_text in TEXT:
         text = T.AddText(this_text);
         text.SetTextAngle(angle);
         text.SetTextAlign(alignment);
   else:
      text = T.AddText(TEXT);
      text.SetTextAngle(angle);
      text.SetTextAlign(alignment);
   T.SetTextFont(42);
   T.Draw("same");
   T.SetBorderSize(0);
   return T
def read_graphs():
    import ROOT as r

    ### Initialize
    graphs = {}
    scenarios = ["A1", "A2", "A3","A4","V1", "V2", "V3","V4"]
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

    graphs["dilepton"]["A2"]["obs"] = rescale_graph_axis(TFile("Dilepton/EXO-16-031/ScanMM/contours_dilepton_A2_smooth.root").Get("obs"),1e3,1e3)
    graphs["dilepton"]["A2"]["exp"] = rescale_graph_axis(TFile("Dilepton/EXO-16-031/ScanMM/contours_dilepton_A2_smooth.root").Get("exp"),1e3,1e3)
    graphs["dilepton"]["V2"]["obs"] = rescale_graph_axis(TFile("Dilepton/EXO-16-031/ScanMM/contours_dilepton_V2_smooth.root").Get("obs"),1e3,1e3)
    graphs["dilepton"]["V2"]["exp"] = rescale_graph_axis(TFile("Dilepton/EXO-16-031/ScanMM/contours_dilepton_V2_smooth.root").Get("exp"),1e3,1e3)


    graphs["monoz"]["A1"]["obs"] = r.TGraph("MonoZll/EXO-16-052/ScanMM/monoz_contour_observed_limit_axial_cl95.txt")
    graphs["monoz"]["A1"]["exp"] = r.TGraph("MonoZll/EXO-16-052/ScanMM/monoz_contour_expected_limit_axial_cl95.txt")
    graphs["monoz"]["V1"]["obs"] = r.TGraph("MonoZll/EXO-16-052/ScanMM/monoz_contour_observed_limit_vector_cl95.txt")
    graphs["monoz"]["V1"]["exp"] = r.TGraph("MonoZll/EXO-16-052/ScanMM/monoz_contour_expected_limit_vector_cl95.txt")

    graphs["monophoton"]["A1"]["obs"] =TFile("Monophoton/ScanMM/Monophoton_A_MM_ICHEP2016_obs.root").Get("monophoton_obs")
    graphs["monophoton"]["A1"]["exp"] =TFile("Monophoton/ScanMM/Monophoton_A_MM_ICHEP2016_exp.root").Get("monophoton_exp")
    graphs["monophoton"]["V1"]["obs"] =TFile("Monophoton/ScanMM/Monophoton_V_MM_ICHEP2016_obs.root").Get("monophoton_obs")
    graphs["monophoton"]["V1"]["exp"] =TFile("Monophoton/ScanMM/Monophoton_V_MM_ICHEP2016_exp.root").Get("monophoton_exp")


    graphs["monoHgg"]["V1"]["obs"] = TFile("MonoHgg/ScanMM/input_combo_MonoHgg_25April.root").Get("observed_baryonic_MonoHgg")
    graphs["monoHgg"]["V1"]["exp"] = TFile("MonoHgg/ScanMM/input_combo_MonoHgg_25April.root").Get("expected_baryonic_MonoHgg")

    graphs["monotop"]["V4"]["obs"] = TFile("Monotop/ScanMM/fcnc2d_obs_vector.root").Get("observed")

    graphs["dijet"]["A1"]["obs"] = TFile("Dijet/ScanMM/Dijet_MM_A_Dijetpaper2016_obs_MT.root").Get("Obs_90")
    graphs["dijet"]["A1"]["exp"] = TFile("Dijet/ScanMM/Dijet_MM_A_Dijetpaper2016_exp.root").Get("Obs_90")
    graphs["dijet"]["A2"]["obs"] = TFile("Dijet/ScanMM/MMedMDM_dijet_av_gq01gl01gDM1_MT.root").Get("obs_025")
    graphs["dijet"]["A2"]["exp"] = TFile("Dijet/ScanMM/MMedMDM_dijet_av_gq01gl01gDM1.root").Get("exp_025")





    graphs["dijet"]["V1"]["obs"] = TFile("Dijet/ScanMM/Dijet_MM_V_Dijetpaper2016_obs_MT.root").Get("Obs_90")
    graphs["dijet"]["V1"]["exp"] = TFile("Dijet/ScanMM/Dijet_MM_V_Dijetpaper2016_exp.root").Get("Obs_90")
    graphs["dijet"]["V2"]["obs"] = TFile("Dijet/ScanMM/MMedMDM_dijet_v_gq01gl001gDM1_MT.root").Get("obs_025")
    graphs["dijet"]["V2"]["exp"] = TFile("Dijet/ScanMM/MMedMDM_dijet_v_gq01gl001gDM1.root").Get("exp_025")

    graphs["dijetchi"]["A3"]["obs"] = TFile("DijetChi/ScanMM/limitsLHC_DMAxial_MDM_MMed_MT.root").Get("obs_MvsM")
    graphs["dijetchi"]["V3"]["obs"] = TFile("DijetChi/ScanMM/limitsLHC_DMVector_MDM_MMed_MT.root").Get("obs_MvsM")

    graphs["trijet"]["A1"]["obs"] = TFile("Trijet/ScanMM/MMedMDM_av.root").Get("obs_025")
    graphs["trijet"]["A1"]["exp"] = TFile("Trijet/ScanMM/MMedMDM_av.root").Get("exp_025")
    graphs["trijet"]["A2"]["obs"] = TFile("Trijet/ScanMM/MMedMDM_trijet_av_gq01gl01gDM1.root").Get("obs_025")
    graphs["trijet"]["A2"]["exp"] = TFile("Trijet/ScanMM/MMedMDM_trijet_av_gq01gl01gDM1.root").Get("exp_025")


    graphs["trijet"]["V1"]["obs"] = TFile("Trijet/ScanMM/MMedMDM_v.root").Get("obs_025")
    graphs["trijet"]["V1"]["exp"] = TFile("Trijet/ScanMM/MMedMDM_v.root").Get("exp_025")
    graphs["trijet"]["V2"]["obs"] = TFile("Trijet/ScanMM/MMedMDM_trijet_v_gq01gl001gDM1.root").Get("obs_025")
    graphs["trijet"]["V2"]["exp"] = TFile("Trijet/ScanMM/MMedMDM_trijet_v_gq01gl001gDM1.root").Get("exp_025")



    graphs["relic"]["A1"]["obs"] = TFile("Relic/madDMv2_0_6/relic_A1.root").Get("mytlist").At(0)
    graphs["relic"]["A2"]["obs"] = TFile("Relic/madDMv2_0_6/relic_A2.root").Get("mytlist").At(0)
    graphs["relic"]["A3"]["obs"] = TFile("Relic/madDMv2_0_6/relic_axial_gq1.root").Get("mytlist").At(0)
    graphs["relic"]["V1"]["obs"] = TFile("Relic/madDMv2_0_6/relic_V1.root").Get("mytlist").At(0)
    graphs["relic"]["V2"]["obs"] = TFile("Relic/madDMv2_0_6/relic_V2.root").Get("mytlist").At(0)
    graphs["relic"]["V3"]["obs"] = TFile("Relic/madDMv2_0_6/relic_vector_gq1.root").Get("mytlist").At(0)
    graphs["relic"]["V4"]["obs"] = TFile("Relic/madDMv2_0_6/relic_V1.root").Get("mytlist").At(0)


    return graphs

def read_relic_lists():
    import ROOT as r
    lists = {}
    lists["A1"] = TFile("Relic/madDMv2_0_6/relic_A1.root").Get("mytlist")
    lists["A2"] = TFile("Relic/madDMv2_0_6/relic_A2.root").Get("mytlist")
    lists["A3"] = TFile("Relic/madDMv2_0_6/relic_axial_gq1.root").Get("mytlist")
    lists["V1"] = TFile("Relic/madDMv2_0_6/relic_V1.root").Get("mytlist")
    lists["V2"] = TFile("Relic/madDMv2_0_6/relic_V2.root").Get("mytlist")
    lists["V3"] = TFile("Relic/madDMv2_0_6/relic_vector_gq1.root").Get("mytlist")
    lists["V4"] = TFile("Relic/madDMv2_0_6/relic_V1.root").Get("mytlist")
    return lists

def get_line_style():
    import ROOT as r
    linestyle = {}
    ### Planck
    linestyle["relic"]          = 1
    ### Met-less
    linestyle["dijet"]          = r.kSolid
    linestyle["dijetchi"]       = r.kSolid
    linestyle["dijet_2016"]     = r.kSolid
    linestyle["dijet_2016_exp"] = r.kDashed
    linestyle["dilepton"]       = r.kSolid
    linestyle["trijet"]         = r.kSolid
    ### MET+X
    linestyle["monophoton"]     = r.kSolid
    linestyle["monoz"]          = r.kSolid
    linestyle["monoHgg"]        = r.kSolid
    linestyle["monotop"]        = r.kSolid
    ### dummies dashed
    linestyle["monojet"]        = r.kSolid

    return linestyle
def get_fill_style():
    import ROOT as r
    fillstyle = {}
    ### Planck
    fillstyle["relic"]          = 9
    ### Met-less
    fillstyle["dijet"]          = 1001
    fillstyle["dijetchi"]       = 1001
    fillstyle["dilepton"]       = 1001
    fillstyle["trijet"]         = 1001
    ### MET+X
    fillstyle["monophoton"]     = 3005
    fillstyle["monoz"]          = 3005
    fillstyle["monoHgg"]        = 3005
    fillstyle["monotop"]        = 3005
    ### dummies dashed
    fillstyle["monojet"]        = 3005

    return fillstyle

def get_line_width():
    linewidth = {}
    ### Planck
    linewidth["relic"]          = 1
    ### Met-less
    linewidth["dijet"]          = 2
    linewidth["dijetchi"]       = 2
    linewidth["dilepton"]       = 2
    linewidth["trijet"]         = 2
    ### MET+X
    linewidth["monophoton"]     = 102
    linewidth["monoz"]          = -102
    linewidth["monoHgg"]        = 102
    linewidth["monotop"]        = 102
    ### dummies dashed
    linewidth["monojet"]        = 102

    return linewidth

def get_color():
    import ROOT as r
    color = {}

    ### Planck
    color["relic"]          = r.kGray+1
    ### Met-less
    color["dijet"]          = r.kYellow-10
    color["dijetchi"]       = r.kAzure
    color["dilepton"]       = r.kGreen-10
    color["trijet"]         = r.kCyan-10
    color["chi"]            = r.kBlue
    ### MET+X
    color["monojet"]        = r.kRed+2#kRed+1
    color["monophoton"]     = r.kOrange+9#kRed+2
    color["monoz"]          = r.kOrange-3#kRed+3
    color["monoHgg"]        = r.kMagenta-7#kRed+3
    color["monotop"]        = r.kViolet+1

    return color

def get_line_color():
    import ROOT as r
    color = {}

    ### Planck
    color["relic"]          = r.kBlack
    ### Met-less
    color["dijet"]          = r.kAzure+4
    color["dijet"]          = r.kYellow+3
    color["dijetchi"]       = r.kAzure
    color["dilepton"]       = r.kGreen+3
    color["dijet_2016"]     = r.kAzure
    color["dijet_2016_exp"] = r.kAzure+1
    color["trijet"]         = r.kAzure+1
    color["trijet"]         = r.kCyan-5
    color["chi"]            = r.kBlue
    ### MET+X
    color["monojet"]        = r.kRed+2#kRed+1
    color["monophoton"]     = r.kOrange+9#kRed+2
    color["monoz"]          = r.kOrange+1#kRed+3
    color["monoHgg"]        = r.kMagenta-7#kRed+3
    color["monotop"]        = r.kViolet+1

    return color

def get_text():
    text = {}
    text["relic"]          = "\Omega_{c} h^{2} \geq 0.12"
    text["dijet"]          = "#splitline{#bf{Dijet} (35.9 fb^{-1})}{#it{[EXO-16-056]}}"
    text["dijetchi"]       = "#bf{Dijet #chi}  (36.5 fb^{-1}) #it{[EXO-16-046]}"
    #~ text["dilepton"]       = "#splitline{Dilepton: ee (12.4 fb^{-1}) + #mu#mu (13.0 fb^{-1})}{#it{[EXO-16-031]}}"
    text["dilepton"]       = "#splitline{#bf{Dilepton} (12.4 fb^{-1} / 13.0 fb^{-1})}{#it{[EXO-16-031]}}"
    text["dijet_2016"]     = "Observed"
    text["dijet_2016_exp"] = "Expected"
    text["trijet"]         = "#splitline{#bf{Boosted dijet} (35.9 fb^{-1})}{#it{[EXO-17-001]}}"
    text["chi"]            = "chi obs. (exp.excl.)"
    text["monojet"]        = "#splitline{#bf{DM + j/V(qq)} (35.9 fb^{-1})}{#it{[EXO-16-048]}}"
    text["monoz"]          = "#splitline{#bf{DM + Z(ll)} (35.9 fb^{-1})}{#it{[EXO-16-052]}}"
    text["monoHgg"]        = "#splitline{#bf{DM + H_{#gamma #gamma}} (35.9 fb^{-1})}{#it{[EXO-16-054]}}"
    text["monophoton"]     = "#splitline{#bf{DM + #gamma} (12.9 fb^{-1})}{#it{[EXO-16-039]}}"
    text["monotop"]        = "#splitline{#bf{DM + t} (100% FC, 35.8 fb^{-1}) }{#it{[EXO-16-051]}}"
    return text

def get_scenario_label_coordinates(metxonly=False,logx=False):
    coords = {}
    coords["A1"] = (0.2,0.7,0.6,0.85)
    coords["A2"] = (0.37,0.87,0.6,0.85)
    coords["A3"] = (0.1,0.3,0.6,0.85)
    coords["A4"] = (0.1,0.3,0.6,0.85)
    coords["V1"] = (0.215,0.415,0.6,0.85)
    coords["V2"] = (0.4,0.6,0.6,0.85)
    coords["V3"] = (0.1,0.3,0.6,0.85)
    coords["V4"] = (0.1,0.3,0.6,0.85)

    if(metxonly):
        coords["A1"] = (0.12,0.62,0.6,0.85)
        coords["V1"] = (0.12,0.62,0.6,0.85)

    if(logx):
        coords["A1"] = (0.12,0.62,0.6,0.85)
        coords["A2"] = (0.1,0.5,0.6,0.85)
        coords["A3"] = (0.1,0.3,0.6,0.85)
        coords["A4"] = (0.1,0.3,0.6,0.85)
        coords["V1"] = (0.215,0.415,0.6,0.85)
        coords["V2"] = (0.55,0.75,0.6,0.85)
        coords["V3"] = (0.1,0.3,0.6,0.85)
        coords["V4"] = (0.1,0.3,0.6,0.85)
    return coords

def get_relic_coordinates():
    coords = {}
    coords["A1"] = [(0.48,0.58,0.67,0.7),(0.46,0.56,0.42,0.45)  ]
    coords["A2"] = [(0.1,0.3,0.6,0.85)  ]
    coords["A3"] = [(0.1,0.3,0.6,0.85)  ]
    coords["A4"] = [(0.1,0.3,0.6,0.85)  ]
    coords["V1"] = [(0.57,0.67,0.28,0.36)  ]
    coords["V2"] = [(0.7,0.85,0.5,0.6) ]
    coords["V3"] = [(0.1,0.3,0.6,0.85)  ]
    coords["V4"] = [(0.1,0.3,0.6,0.85)  ]
    return coords
def get_relic_angles():
    coords = {}
    coords["A1"] = 30
    coords["A2"] = 30
    coords["A3"] = 30
    coords["A4"] = 30
    coords["V1"] = 28
    coords["V2"] = 30
    coords["V3"] = 30
    coords["V4"] = 30
    return coords
def get_diagonal_angles():
    coords = {}
    coords["A1"] = 32
    coords["A2"] = 30
    coords["A3"] = 30
    coords["A4"] = 30
    coords["V1"] = 32
    coords["V2"] = 30
    coords["V3"] = 30
    coords["V4"] = 30
    return coords

def get_diagonal_coordinates():
    coords = {}
    coords["A1"] = (0.4,0.51,0.5,0.55)
    coords["A2"] = (0.1,0.3,0.6,0.85)
    coords["A3"] = (0.1,0.3,0.6,0.85)
    coords["A4"] = (0.1,0.3,0.6,0.85)
    coords["V1"] = (0.4,0.51,0.52,0.58)
    coords["V2"] = (0.7,0.85,0.5,0.6)
    coords["V3"] = (0.1,0.3,0.6,0.85)
    coords["V4"] = (0.1,0.3,0.6,0.85)
    return coords
def get_scenario_labels():
    label = {}
    label["A1"] = [ "#bf{Axial-vector mediator}","Dirac DM", "g_{DM} = 1.0","g_{q}  = 0.25","g_{l} = 0" ]
    label["A2"] = [ "#bf{Axial-vector mediator}","Dirac DM", "g_{DM} = 1.0","g_{q}  = 0.1","g_{l} = 0.1" ]
    label["A3"] = [ "#bf{Axial-vector mediator}","Dirac DM", "g_{DM} = 1.0","g_{q}  = 1.0","g_{l} = 0" ]
    label["A4"] = label["A1"]
    label["V1"] = [ "#bf{Vector mediator}", "Dirac DM","g_{DM} = 1.0","g_{q}  = 0.25","g_{l} = 0" ]
    label["V2"] = [ "#bf{Vector mediator}","Dirac DM", "g_{DM} = 1.0","g_{q}  = 0.1","g_{l} = 0.01" ]
    label["V3"] = [ "#bf{Vector mediator}","Dirac DM", "g_{DM} = 1.0","g_{q}  = 1.0","g_{l} = 0" ]
    label["V4"] = label["V1"]

    return label

def make_dummy_entries(legend):

    dummy_obs = TGraph()
    dummy_obs.SetLineWidth(202)

    dummy_obs.SetLineColor(kBlack)
    dummy_obs.SetMarkerSize(0)
    dummy_obs.SetFillColor(kBlack)
    dummy_obs.SetFillStyle(3005)

    legend.AddEntry(dummy_obs,"Observed","L")

    dummy_exp = TGraph()

    dummy_exp.SetLineStyle(kDashed)

    dummy_exp.SetLineColor(kBlack)
    dummy_exp.SetMarkerSize(0)
    dummy_exp.SetFillColor(kBlack)
    dummy_exp.SetFillStyle(0)
    dummy_exp.SetLineWidth(2)

    legend.AddEntry(dummy_exp,"Expected","L")

    return [dummy_obs,dummy_exp]

def make_legend(scenario_name,logx=False):
    import ROOT as r
    coords = {}
    coords["A1"] = (0.68,0.15,0.87,0.65)
    coords["A2"] = (0.62,0.15,0.87,0.5)
    coords["A3"] = (0.4,0.12,0.8,0.3)
    coords["A4"] = (0.68,0.15,0.87,0.65)
    coords["V1"] = (0.68,0.15,0.87,0.65)
    coords["V2"] = (0.62,0.15,0.87,0.5)
    coords["V3"] = (0.35,0.67,0.75,0.85)
    coords["V4"] = (0.68,0.15,0.87,0.65)

    textsize = {}
    textsize["A1"] = 0.025
    textsize["A2"] = 0.025
    textsize["A3"] = 0.035
    textsize["A4"] = 0.025
    textsize["V1"] = 0.025
    textsize["V2"] = 0.025
    textsize["V3"] = 0.035
    textsize["V4"] = 0.025

    leg = r.TLegend(*coords[scenario_name])
    leg.SetBorderSize(1)
    leg.SetTextFont(42)
    leg.SetTextSize(textsize[scenario_name])
    leg.SetFillColor(r.kWhite)
    leg.SetFillStyle(1001)
    leg.SetHeader("#bf{Exclusion at 95% CL}")

    return leg

def make_auxiliary_legend(scenario_name,logx=False):
    import ROOT as r
    coords = {}
    coords["A1"] = (0.68,0.7,0.87,0.85)
    coords["A2"] = (0.68,0.53,0.87,0.68)
    coords["A3"] = (0.6,0.33,0.8,0.45)
    coords["A4"] = (0.68,0.7,0.87,0.85)
    coords["V1"] = (0.68,0.7,0.87,0.85)
    coords["V2"] = (0.68,0.53,0.87,0.68)
    coords["V3"] = (0.55,0.52,0.75,0.64)
    coords["V4"] = (0.68,0.7,0.87,0.85)

    textsize = {}
    textsize["A1"] = 0.035
    textsize["A2"] = 0.035
    textsize["A3"] = 0.035
    textsize["A4"] = 0.035
    textsize["V1"] = 0.035
    textsize["V2"] = 0.035
    textsize["V3"] = 0.035
    textsize["V4"] = 0.035


    leg = r.TLegend(*coords[scenario_name])
    leg.SetBorderSize(1)
    leg.SetTextFont(42)
    leg.SetFillColor(r.kWhite)
    leg.SetFillStyle(1001)
    leg.SetTextSize(textsize[scenario_name])
    #~ leg.SetHeader("#bf{Exclusion at 95% CL}")

    return leg

def check_graph_orientation(graph):
    import ROOT as r
    n = graph.GetN()
    xfirst = r.Double()
    yfirst = r.Double()
    xlast = r.Double()
    ylast = r.Double()
    graph.GetPoint(0,xfirst,yfirst)
    graph.GetPoint(n-1,xlast,ylast)
    print xfirst, xlast
    return xfirst < xlast

def convert_spline_to_graph(spline,xmin,xmax):
	import ROOT as r
	import numpy
	g = r.TGraph()

	for x in numpy.linspace(xmin,xmax,100):
		g.SetPoint(g.GetN(),x,spline.Eval(x))
	return g
