from ROOT import *
import numpy

med = "A"#V/A/SI/SD
quantile = "exp"
for med in ["AV","V"]:
	for quantile in ["exp","obs"]:
		if   med=="V"  : f1=TFile.Open("monophoton_V.root")
		elif med=="AV" : f1=TFile.Open("monophoton_AV.root")
		elif med=="SI" : f1=TFile.Open("monophoton_SI.root")
		elif med=="SD" : f1=TFile.Open("monophoton_SD.root")

		g_exp=f1.Get("g_"+quantile)

		g_clone = g_exp.Clone()

		C=TCanvas()

		a=numpy.ndarray((1))
		a[0]=1

		h_exp=g_exp.GetHistogram()
		h_exp.SetContour(1,a)

		g_exp.Draw("col2z")
		h_exp.Draw("contz list")
		C.Update()

		mycontoursarray=gROOT.GetListOfSpecials().FindObject("contours")
		print "mycontoursarray = ", mycontoursarray
		mylist=mycontoursarray.At(0)
		print "mylist = ", mylist
		print "mylist size = ", mylist.GetSize()

		C2=TCanvas("C2","C2")

		g_clone.Draw("cont3")

		for i in range(0,mylist.GetSize()):
			g_i = mylist.At(i)
			g_i.SetLineWidth(5)
			g_i.SetLineColor(kRed+4)
			g_i.SetLineStyle(kDashed)
			if i==1: g_i.Draw("lp,same")
		C2.SaveAs("control_{MED}_{QUANTILE}.png".format(MED=med,QUANTILE=quantile))
		if   med == "V"  : f_exp = TFile("Monophoton_V_MM_ICHEP2016_{QUANTILE}.root" .format(QUANTILE=quantile),"RECREATE")
		elif med == "AV" : f_exp = TFile("Monophoton_A_MM_ICHEP2016_{QUANTILE}.root" .format(QUANTILE=quantile),"RECREATE")
		elif med == "SI" : f_exp = TFile("Monophoton_SI_MM_ICHEP2016_{QUANTILE}.root".format(QUANTILE=quantile),"RECREATE")
		elif med == "SD" : f_exp = TFile("Monophoton_SD_MM_ICHEP2016_{QUANTILE}.root".format(QUANTILE=quantile),"RECREATE")

		if   med == "V" or med=="AV": mylist.At(0).Write("monophoton_" + quantile)
		elif med == "SI" : mylist.At(1).Write("monophoton_" + quantile)
		elif med == "SD" : mylist.At(1).Write("monophoton_" + quantile)


