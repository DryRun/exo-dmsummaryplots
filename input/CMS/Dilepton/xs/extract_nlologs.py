import os
import sys
import glob
import re
from pprint import pprint

re_logname = re.compile("mcatnlo_run_MMED(?P<mmed>\d+)_MDM(?P<mdm>\d+)_(?P<scenario>(A2|V2))\.log")
re_done = re.compile("Collecting events")
re_xs = re.compile("Cross section.*(?P<xs>\d+\.\d*[eE]([+\-])?\d+)")
#log_${{MMED}}_${{MDM}}_{SCENARIO}.txt
logs = glob.glob("condor/*/mcatnlo*log")

xs = {}
dxs = {}
bad_logs = []
for log in logs:
	log_basename = os.path.basename(log)
	match_logname = re_logname.search(log_basename)
	if not match_logname:
		print("Couldn't parse log name: {}".format(log_basename))
		continue
	mmed = int(match_logname.group("mmed"))
	mdm = int(match_logname.group("mdm"))
	scenario = match_logname.group("scenario")
	if not scenario in xs.keys():
		xs[scenario] = {}
		dxs[scenario] = {}
	if not mmed in xs[scenario].keys():
		xs[scenario][mmed] = {}
		dxs[scenario][mmed] = {}
	if not mdm in xs[scenario][mmed].keys():
		xs[scenario][mmed][mdm] = -1.
		xs[scenario][mmed][mdm] = -1.

	with open(log, "r") as flog:
		for line in flog:
			match_xs = re_xs.search(line)
			if match_xs:
				xs[scenario][mmed][mdm] = match_xs.group("xs")
				dxs[scenario][mmed][mdm] = match_xs.group("dxs")
	if xs[scenario][mmed][mdm] == -1.:
		print("WARNING : Failed to find xs for {} {} {}, log {}".format(scenario, mmed, mdm, log))
		bad_logs.append(log)
if len(bad_logs) >= 1:
	print("WARNING : Failed to get some xses. Failed logs:")
	pprint(bad_logs)
for scenario in xs.keys():
	with open("xs_fxfx_{}.dat".format(scenario), "w") as xsfile:
		for mmed in xs[scenario].keys():
			for mdm in xs[scenario][mmed].keys():
				xsfile.write("{}\t{}\t{}".format(mmed, mdm, xs[scenario][mmed][mdm]))
				
