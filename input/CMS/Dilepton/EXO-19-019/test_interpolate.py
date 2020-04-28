import os
import sys
import ROOT
import numpy as np

x_arr = np.arange(0., 100., 1.)
y_arr = np.arange(0., 1000., 10.)
tg = ROOT.TGraph2D()
for x in x_arr:
	for y in y_arr:
		tg.SetPoint(tg.GetN(), x, y, x*y)
print("tg extrapolated to (200, 500):")
print(tg.Interpolate(200., 500.))
