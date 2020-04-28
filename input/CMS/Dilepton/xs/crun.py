import os
import sys
import numpy as np
import math

import argparse
parser = argparse.ArgumentParser(description="Run many Z'(ll) Madgraph jobs to get cross sections")
parser.add_argument("--scenario", "-s", type=str, help="V2 or A2")
parser.add_argument("--ppj", "-n", type=int, default=10, help="Points per condor job")
parser.add_argument("--test", action="store_true", help="Run small test job")
args = parser.parse_args()

gq_V  = 0.0
gdm_V = 0.0
gl_V  = 0.0
gq_A  = 0.0
gdm_A = 0.0
gl_A  = 0.0
gnu   = 0.0

if args.scenario == "V2":
	gq_V  = 0.1
	gdm_V = 1.0
	gl_V  = 0.01
	gnu   = 0.01
	#mMEDs = range(100, 4000+50, 50)
	#mDMs = range(0, 4000+25, 25)
elif args.scenario == "A2":
	gq_A  = 0.1
	gdm_A = 1.0
	gl_A  = 0.1
	gnu   = 0.1
else:
	raise ValueError("--scenario [-s] must be V2 or A2")
mMEDs = range(100, 5000+50, 50)
mDMs = range(0, 5000+25, 25)

if args.test:
	mMEDs = mMEDs[:1]
	mDMs = mDMs[:1]

pairs = []
for mMED in mMEDs:
	for iDM, mDM in enumerate(mDMs):
		# Skip pairs above the diagonal, ensuring there's at least one point >= diagonal
		if 2*mDM >= mMED and iDM >= 1:
			if 2*(mDMs[iDM-1]) >= mMED:
				continue
		pairs.append((mMED, mDM))

# Finer granularity near the diagonal. The xs changes very rapidly here.
# NOT USED CURRENTLY. A non-uniform grid slows down scipy.interpolate, which is faster for a regular grid.
#fine_mMEDs = range(100, 5000+10, 10)
#for mMED in fine_mMEDs:
#	for i in xrange(15):
#		mDM = mMED/2 - i*10.
#		if not (mMED, mDM) in pairs:
#			pairs.append((mMED, mDM))

target_njobs = int(math.ceil(1. * len(pairs) / args.ppj))
subjob_pairlists = np.array_split(pairs, target_njobs)
print("Running {} points in {} jobs".format(len(pairs), len(subjob_pairlists)))

for isubjob, subjob_pairlist in enumerate(subjob_pairlists):
	subjobdir = "/afs/cern.ch/user/d/dryu/MCI/DMSummaryPlots/src/ExoDMSummaryPlots/input/CMS/Dilepton/xs/condor/{}_subjob{}".format(args.scenario, isubjob)
	os.system("mkdir -pv {}".format(subjobdir))
	with open("{}/run.sh".format(subjobdir), "w") as run_script:
		run_script.write("#!/bin/bash\n")
		run_script.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
		run_script.write("scramv1 project CMSSW CMSSW_10_6_11\n")
		run_script.write("cd CMSSW_10_6_11/src\n")
		run_script.write("eval `scramv1 runtime -sh`\n")
		run_script.write("cd ../..\n")
		run_script.write("tar -xzf gridpack_pythia.tgz\n")
		run_script.write("cd MG5_aMC_v2_6_5\n")
		run_script.write("MGDIR=$(readlink -e .)\n")
		run_script.write("sed -i 's|@MGDIR@|${MGDIR}|g' Cards/shower_card.dat\n")# input/mg5_configuration.txt ./HEPTools/pythia8/bin/pythia8-config ./HEPTools/pythia8/share/Pythia8/examples/Makefile.inc \n")
		run_script.write("LHAPDFCONFIG=`echo \"$LHAPDF_DATA_PATH/../../bin/lhapdf-config\"`\n")
		run_script.write("echo \"lhapdf = $LHAPDFCONFIG\" >> ./Cards/amcatnlo_configuration.txt\n")
		run_script.write("MMEDARRAY=({})\n".format(" ".join(str(x[0]) for x in subjob_pairlist)))
		run_script.write("MDMARRAY=({})\n".format(" ".join(str(x[1]) for x in subjob_pairlist)))
		run_script.write("""
for index in ${{!MMEDARRAY[*]}}; do 
	cd $_CONDOR_SCRATCH_DIR/MG5_aMC_v2_6_5
	MMED=${{MMEDARRAY[$index]}}
	MDM=${{MDMARRAY[$index]}}
	RUN_SCRIPT=run_${{MMED}}_${{MDM}}.txt
	LOG=log_${{MMED}}_${{MDM}}_{SCENARIO}.txt
	MGDIR=$(readlink -e .)

	MLLMIN=$(python -c "print max(${{MMED}}-650.0,0)")
	MLLMAX=$(python -c "print ${{MMED}}+650.0")
	sed -i \"s|MLLMIN|${{MLLMIN}}|g\" ./Template/NLO/SubProcesses/cuts.f
	sed -i \"s|MLLMAX|${{MLLMAX}}|g\" ./Template/NLO/SubProcesses/cuts.f

	cp ../run_template.txt $RUN_SCRIPT
	ll $RUN_SCRIPT
	echo "MMED ${{MMED}}, MDM ${{MDM}}, RUN_SCRIPT ${{RUN_SCRIPT}}"
	echo "PWD:"
	echo $PWD
	ls -lrth
	cat $RUN_SCRIPT
	sed -i \"s|@MGDIR@|${{MGDIR}}|g\" $RUN_SCRIPT
	sed -i \"s|@MMED@|${{MMED}}|g\" $RUN_SCRIPT
	sed -i \"s|@MDM@|${{MDM}}|g\" $RUN_SCRIPT
	sed -i \"s|@GQA@|{GQA}|g\" $RUN_SCRIPT
	sed -i \"s|@GLA@|{GLA}|g\" $RUN_SCRIPT
	sed -i \"s|@GDMA@|{GDMA}|g\" $RUN_SCRIPT
	sed -i \"s|@GQV@|{GQV}|g\" $RUN_SCRIPT
	sed -i \"s|@GLV@|{GLV}|g\" $RUN_SCRIPT
	sed -i \"s|@GDMV@|{GDMV}|g\" $RUN_SCRIPT
	sed -i \"s|@GNU@|{GNU}|g\" $RUN_SCRIPT
	sed -i \"s|@SCENARIO@|{SCENARIO}|g\" $RUN_SCRIPT
	cat $RUN_SCRIPT
	./bin/mg5_aMC $RUN_SCRIPT 2>&1 > ${{LOG}}
	mv Zpll_MMED${{MMED}}_MDM${{MDM}}_{SCENARIO}/MCatNLO/RUN_PYTHIA8_1/mcatnlo_run.log ../mcatnlo_run_MMED${{MMED}}_MDM${{MDM}}_{SCENARIO}.log
done\n""".format(
				GQA=gq_A, GDMA=gdm_A, GLA=gl_A, 
				GQV=gq_V, GDMV=gdm_V, GLV=gl_V,
				GNU=gnu, SCENARIO=args.scenario,
			))
		run_script.write("mv log*txt ..\n")
	files_to_transfer = ["/afs/cern.ch/user/d/dryu/MCI/DMSummaryPlots/src/ExoDMSummaryPlots/input/CMS/Dilepton/xs/gridpack_pythia.tgz", "/afs/cern.ch/user/d/dryu/MCI/DMSummaryPlots/src/ExoDMSummaryPlots/input/CMS/Dilepton/xs/run_template.txt"]
	csub_command = "csub {}/run.sh -t tomorrow -F {} -d {}".format(subjobdir, ",".join(files_to_transfer), subjobdir)
	#print(csub_command)
	os.system(csub_command)
	with open("{}/csub_command.sh".format(subjobdir), "w") as csub_script:
		csub_script.write("#!/bin/bash\n")
		csub_script.write(csub_command + "\n")
