# Convert ATLAS b-tagged dijet results, xs*BR(bb) to xs(qq)
import os
import sys

sys.path.append("../python/")
from zprime_equations import *

xsbrbbs = {
	600 	:8.416040652436278,
	650 	:7.6585906597078335,
	700 	:6.691223761678536,
	750 	:4.655779971209647,
	800 	:5.107625509578944,
	850 	:3.9420291819113036,
	900 	:3.0199895980675637,
	950 	:3.0146524512642423,
	1000 	:3.362777429105319,
	1050 	:3.936030061941626,
	1100 	:3.965602737400202,
	1150 	:3.5033935101644844,
	1200 	:3.135416724584338,
	1250 	:2.993887010389471,
}
xss = {}
for mass, xsbrbb in xsbrbbs.iteritems():
	brbb = Gamma_qq(0.25, mass, "vector", "b") / Gamma_qq_tot(0.25, mass, "vector")
	xss[mass] = xsbrbb / brbb

with open("ATLAS_EXOT2016033_obs_converted.dat", 'w') as f:
	f.write("# m_med xs13\n")
	for mass in sorted(xss.keys()):
		f.write("{} {}\n".format(mass, xss[mass]))
