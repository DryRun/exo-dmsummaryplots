#### Parameter presets
MADGRAPH_VERSION="MG5_aMC_v2_5_2"
WDIR=$(pwd)
EXIT=0

#### Parse Arguments
i=1
GDMV=${!i}; i=$((i+1))
GQV=${!i}; i=$((i+1))
GLV=${!i}; i=$((i+1))

GDMA=${!i}; i=$((i+1))
GQA=${!i}; i=$((i+1))
GLA=${!i}; i=$((i+1))

GNU=${!i}; i=$((i+1))

MMED=${!i}; i=$((i+1))
MDM=${!i}; i=$((i+1))

TAG=${!i}; i=$((i+1))

NEVENTS=${!i}; i=$((i+1))
RUNTAG=${!i}; i=$((i+1))

MLLMIN=$(python -c "print max(${MMED}-650.0,0)")
MLLMAX=$(python -c "print ${MMED}+650.0")


echo "Input parameters:"
for val in GDMV GQV GLV GDMA GQA GLA GNU MMED MDM NEVENTS MLLMIN MLLMAX; do
   echo "     ${val} = ${!val}"
done
### Set up CMSSW
source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ ! -e ./CMSSW_10_6_11 ]; then
   echo "Creating CMSSW directory."
   scramv1 project CMSSW CMSSW_10_6_11
   echo "Done."
fi

echo "Setting CMSSW environment."
pushd CMSSW_10_6_11;
eval `scramv1 runtime -sh`
popd;
echo "Done."


### Fix path problems
pushd ${MADGRAPH_VERSION};

echo "Preparing shower card."
sed -i "s|extrapaths\s*=.*|extrapaths = ../lib ${PWD}/HEPTools/pythia8/lib /usr/lib64/lib ${PWD}/HEPTools/zlib/lib ${PWD}/HEPTools/hepmc/lib|gI" Cards/DM_Dilepton_NLO/shower_card.dat Template/NLO/Cards/shower_card.dat
sed -i "s|extralibs\s*=.*|extralibs = pythia8 boost_iostreams z dl stdc++|gI" Cards/DM_Dilepton_NLO/shower_card.dat Template/NLO/Cards/shower_card.dat

sed -i "s|pythia8_path\s*=.*|pythia8_path = $(readlink -e ./HEPTools/pythia8/)|gI" input/mg5_configuration.txt
sed -i "s|mg5amc_py8_interface_path\s*=.*|mg5amc_py8_interface_path =  $(readlink -e ./HEPTools/MG5aMC_PY8_interface/)|gI" input/mg5_configuration.txt
sed -i "s|/disk1.*HEPTools|${PWD}/HEPTools/|g" ./HEPTools/pythia8/bin/pythia8-config ./HEPTools/pythia8/share/Pythia8/examples/Makefile.inc


### Make the run script
echo "Preparing run script."
SCRIPT=Cards/DM_Dilepton_NLO/run.dat;
cat Cards/DM_Dilepton_NLO/madconfig > ${SCRIPT};
echo "set run_mode 0" >> ${SCRIPT};
echo "set ninja $(readlink -e ./HEPTools/lib)" >> ${SCRIPT};
echo "set collier $(readlink -e ./HEPTools/lib)" >> ${SCRIPT};
echo "set mg5amc_py8_interface_path $(readlink -e ./HEPTools/MG5aMC_PY8_interface)" >> ${SCRIPT};
echo "set pythia8_path $(readlink -e ./HEPTools/pythia8)" >> ${SCRIPT};

cat Cards/DM_Dilepton_NLO/*proc* >> ${SCRIPT};
echo "launch" >> ${SCRIPT};
cat Cards/DM_Dilepton_NLO/*custom* >> ${SCRIPT} ;

echo "Dilepton invariant mass cut: ${MLLMIN} - ${MLLMAX} GeV"
sed -i "s|MLLMIN|${MLLMIN}|g" ./Template/NLO/SubProcesses/cuts.f
sed -i "s|MLLMAX|${MLLMAX}|g" ./Template/NLO/SubProcesses/cuts.f
for val in GDMV GQV GLV GDMA GQA GLA GNU MMED MDM NEVENTS; do
   sed -i "s|${val}|${!val}|g" ${SCRIPT}
done

echo "Done."

### Run it
echo "Start MadGraph."
./bin/mg5_aMC ${SCRIPT};
