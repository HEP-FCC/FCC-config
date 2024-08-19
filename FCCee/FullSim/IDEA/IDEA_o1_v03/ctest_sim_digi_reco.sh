#!/bin/bash

# set-up the environment
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh || true # if the key4hep env is loaded twice, it returns a non zero exit code, '|| true' ensures it returns 0 to avoid stopping pipelines

# run the SIM step
ddsim --enableGun --gun.distribution uniform --gun.energy "10*GeV" --gun.particle e- --numberOfEvents 10 --outputFile IDEA_sim.root --random.enableEventSeed --random.seed 42 --compactFile $K4GEO/FCCee/IDEA/compact/IDEA_o1_v03/IDEA_o1_v03.xml

# run the DIGI/RECO step
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd ) # workaround to have ctests working
k4run $SCRIPT_DIR/run_digi_reco.py
