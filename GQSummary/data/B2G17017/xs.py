'''
Calculate excluded xs values from B2G-17-017
which has limits on xs*BR for width=1%, 10%, and 30%
'''

import os
import sys
sys.path.append("../../python/")
from zprime_equations import *
#def Gamma_qq(gq, m_med, vtype, qtype):
#def Gamma_qq_tot(gq, m_med, vtype):


masses_0p01 = [500, 750, 1000, 1250, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 6000, 6500, 7000]
xsbr_obs_0p01 = [29.,  1.1, 0.37, 0.31, 0.091, 0.023, 0.018, 0.0042, 0.0046, 0.0041, 0.0030, 0.0023, 0.0013, 0.0012, 0.0012]
xsbr_exp_0p01 = [28.,  2.4,  0.54,  0.16,  0.076,  0.027,  0.012, 0.0075, 0.0052, 0.0042, 0.0035, 0.0032, 0.0027, 0.0026, 0.0024]
f_xs_obs_0p01 = open(os.path.expandvars("$CMSSW_BASE/src/ExoDMSummaryPlots/GQSummary/data/B2G17017_w0p01_obs.dat"), 'w')
f_xs_exp_0p01 = open(os.path.expandvars("$CMSSW_BASE/src/ExoDMSummaryPlots/GQSummary/data/B2G17017_w0p01_exp.dat"), 'w')
f_xs_obs_0p01.write("# m_med xs13\n# Calculated by B2G17017/xs.py using numbers from 1810.05905\n")
f_xs_exp_0p01.write("# m_med xs13\n# Calculated by B2G17017/xs.py using numbers from 1810.05905\n")
for i, mass in enumerate(masses_0p01):
    br = Gamma_qq(0.25, mass, "vector", "t") / Gamma_qq_tot(0.25, mass, "vector")
    f_xs_obs_0p01.write("{} {}\n".format(mass, xsbr_obs_0p01[i] / br))
    f_xs_exp_0p01.write("{} {}\n".format(mass, xsbr_exp_0p01[i] / br))
f_xs_obs_0p01.close()
f_xs_exp_0p01.close()

masses_0p1 = [500, 750, 1000, 1250, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 6000, 6500, 7000]
xsbr_obs_0p1 = [31, 2.9, 0.93, 0.55, 0.17, 0.041, 0.027, 0.0084, 0.0091, 0.0092, 0.0087, 0.0097, 0.015, 0.016, 0.022]
xsbr_exp_0p1 = [22, 3.6, 0.72, 0.24, 0.12, 0.040, 0.020, 0.013, 0.011, 0.010, 0.010, 0.012, 0.021, 0.025, 0.032]
f_xs_obs_0p1 = open(os.path.expandvars("$CMSSW_BASE/src/ExoDMSummaryPlots/GQSummary/data/B2G17017_w0p1_obs.dat"), 'w')
f_xs_exp_0p1 = open(os.path.expandvars("$CMSSW_BASE/src/ExoDMSummaryPlots/GQSummary/data/B2G17017_w0p1_exp.dat"), 'w')
f_xs_obs_0p1.write("# m_med xs13\n# Calculated by B2G17017/xs.py using numbers from 1810.05905\n")
f_xs_exp_0p1.write("# m_med xs13\n# Calculated by B2G17017/xs.py using numbers from 1810.05905\n")
for i, mass in enumerate(masses_0p1):
    br = Gamma_qq(0.25, mass, "vector", "t") / Gamma_qq_tot(0.25, mass, "vector")
    f_xs_obs_0p1.write("{} {}\n".format(mass, xsbr_obs_0p1[i] / br))
    f_xs_exp_0p1.write("{} {}\n".format(mass, xsbr_exp_0p1[i] / br))
f_xs_obs_0p1.close()
f_xs_exp_0p1.close()

masses_0p3 = [1000, 2000, 3000, 4000, 5000, 6000, 6500, 7000]
xsbr_obs_0p3 = [2.0, 0.078, 0.019, 0.019, 0.022, 0.029, 0.030, 0.035]
xsbr_exp_0p3 = [1.1, 0.066, 0.026, 0.023, 0.025, 0.035, 0.040, 0.044]
f_xs_obs_0p3 = open(os.path.expandvars("$CMSSW_BASE/src/ExoDMSummaryPlots/GQSummary/data/B2G17017_w0p3_obs.dat"), 'w')
f_xs_exp_0p3 = open(os.path.expandvars("$CMSSW_BASE/src/ExoDMSummaryPlots/GQSummary/data/B2G17017_w0p3_exp.dat"), 'w')
f_xs_obs_0p3.write("# m_med xs13\n# Calculated by B2G17017/xs.py using numbers from 1810.05905\n")
f_xs_exp_0p3.write("# m_med xs13\n# Calculated by B2G17017/xs.py using numbers from 1810.05905\n")
for i, mass in enumerate(masses_0p3):
    br = Gamma_qq(0.25, mass, "vector", "t") / Gamma_qq_tot(0.25, mass, "vector")
    f_xs_obs_0p3.write("{} {}\n".format(mass, xsbr_obs_0p3[i] / br))
    f_xs_exp_0p3.write("{} {}\n".format(mass, xsbr_exp_0p3[i] / br))
f_xs_obs_0p3.close()
f_xs_exp_0p3.close()
