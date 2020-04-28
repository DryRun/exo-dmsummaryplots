# PYTHIA configuration file.
# Generated on Tue Feb 7 18:27:12 CET 2017 with the user supplied options:
# --prefix=@MGDIR@/HEPTools///////////////////////////////////////////////////////pythia8/
# --with-hepmc2=@MGDIR@/HEPTools///////////////////////////////////////////////////////hepmc
# --with-hepmc2-include=@MGDIR@/HEPTools///////////////////////////////////////////////////////hepmc/include
# --with-gzip=@MGDIR@/HEPTools///////////////////////////////////////////////////////zlib
# --with-lhapdf6=/cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/lhapdf/6.1.6-ikhhed2
# --with-lhapdf6-plugin=LHAPDF6.h
# --with-boost=/usr/lib64
# --cxx-common='-ldl -fPIC -lstdc++ -DHEPMC2HACK'

# Install directory prefixes.
PREFIX_BIN=@MGDIR@/HEPTools///////////////////////////////////////////////////////pythia8//bin
PREFIX_INCLUDE=@MGDIR@/HEPTools///////////////////////////////////////////////////////pythia8//include
PREFIX_LIB=@MGDIR@/HEPTools///////////////////////////////////////////////////////pythia8//lib
PREFIX_SHARE=@MGDIR@/HEPTools///////////////////////////////////////////////////////pythia8//share/Pythia8

# Compilation flags (see ./configure --help for further documentation).
ENABLE_SHARED=false
CXX=g++
CXX_COMMON=-ldl -fPIC -lstdc++ -DHEPMC2HACK
CXX_SHARED=-shared
CXX_SONAME=-Wl,-soname
LIB_SUFFIX=.so

# EVTGEN configuration.
EVTGEN_USE=false
EVTGEN_BIN=
EVTGEN_INCLUDE=./
EVTGEN_LIB=./

# FASTJET3 configuration.
FASTJET3_USE=false
FASTJET3_BIN=
FASTJET3_INCLUDE=./
FASTJET3_LIB=./

# HEPMC2 configuration.
HEPMC2_USE=true
HEPMC2_BIN=@MGDIR@/HEPTools///////////////////////////////////////////////////////hepmc/bin/
HEPMC2_INCLUDE=@MGDIR@/HEPTools///////////////////////////////////////////////////////hepmc/include
HEPMC2_LIB=@MGDIR@/HEPTools///////////////////////////////////////////////////////hepmc/lib

# HEPMC3 configuration.
HEPMC3_USE=false
HEPMC3_BIN=
HEPMC3_INCLUDE=./
HEPMC3_LIB=./

# LHAPDF5 configuration.
LHAPDF5_USE=false
LHAPDF5_BIN=
LHAPDF5_INCLUDE=./
LHAPDF5_LIB=./
LHAPDF5_PLUGIN=LHAPDF5.h

# LHAPDF6 configuration.
LHAPDF6_USE=true
LHAPDF6_BIN=/cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/lhapdf/6.1.6-ikhhed2/bin/
LHAPDF6_INCLUDE=/cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/lhapdf/6.1.6-ikhhed2/include
LHAPDF6_LIB=/cvmfs/cms.cern.ch/slc6_amd64_gcc530/external/lhapdf/6.1.6-ikhhed2/lib
LHAPDF6_PLUGIN=LHAPDF6.h

# POWHEG configuration.
POWHEG_USE=false
POWHEG_BIN=
POWHEG_INCLUDE=./
POWHEG_LIB=./

# PROMC configuration.
PROMC_USE=false
PROMC_BIN=
PROMC_INCLUDE=./
PROMC_LIB=./

# ROOT configuration.
ROOT_USE=false
ROOT_BIN=
ROOT_INCLUDE=./
ROOT_LIB=./

# GZIP configuration.
GZIP_USE=true
GZIP_BIN=@MGDIR@/HEPTools///////////////////////////////////////////////////////zlib//
GZIP_INCLUDE=@MGDIR@/HEPTools///////////////////////////////////////////////////////zlib/include
GZIP_LIB=@MGDIR@/HEPTools///////////////////////////////////////////////////////zlib/lib

# BOOST configuration.
BOOST_USE=true
BOOST_BIN=/usr/lib64/bin/
BOOST_INCLUDE=/usr/lib64/include
BOOST_LIB=/usr/lib64/lib

# PYTHON configuration.
PYTHON_USE=false
PYTHON_BIN=
PYTHON_INCLUDE=./
PYTHON_LIB=./
