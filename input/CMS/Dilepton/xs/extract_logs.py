import os
import sys
import glob
import re
from pprint import pprint

re_logname = re.compile("log_(?P<mmed>\d+)_(?P<mdm>\d+)_(?P<scenario>(A2|V2))")
re_done = re.compile("Collecting events")
re_xs = re.compile("(?P<xs>\d+\.\d*[eE]([+\-])?\d+).*\+\-.*(?P<dxs>\d+\.\d*[eE]([+\-])?\d+)")
#log_${{MMED}}_${{MDM}}_{SCENARIO}.txt

subjob_folders = glob.glob("condor/*subjob*")
bad_subjobs = []
for subjob_folder in subjob_folders:
	subjob_logs = glob.glob(subjob_folder + "/log*txt")
	if len(subjob_logs) == 0:
		bad_subjobs.append(subjob_folder)
if len(bad_subjobs) >= 1:
	print("Some subjobs failed:")
	print(bad_subjobs)
	sys.exit(1)

logs = glob.glob("condor/*/log*txt")
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
		job_done = False
		for line in flog:
			if re_done.search(line):
				job_done = True
			if job_done:
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
	with open("xs_{}.dat".format(scenario), "w") as xsfile:
		for mmed in sorted(xs[scenario].keys()):
			for mdm in sorted(xs[scenario][mmed].keys()):
				xsfile.write("{}\t{}\t{}\n".format(mmed, mdm, xs[scenario][mmed][mdm]))
				
