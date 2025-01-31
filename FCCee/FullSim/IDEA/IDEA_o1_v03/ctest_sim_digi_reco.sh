#!/bin/bash

# set-up the Key4hep environment if not already set
if [[ -z "${KEY4HEP_STACK}" ]]; then
  source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
else
  echo "The Key4hep stack was already loaded in this environment."
fi

# run the SIM step
ddsim --enableGun --gun.distribution uniform --gun.energy "10*GeV" --gun.particle e- --numberOfEvents 10 --outputFile IDEA_sim.root --random.enableEventSeed --random.seed 42 --compactFile $K4GEO/FCCee/IDEA/compact/IDEA_o1_v03/IDEA_o1_v03.xml --steeringFile $K4GEO/example/SteeringFile_IDEA_o1_v03.py

# run the DIGI/RECO step
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd ) # workaround to have ctests working
k4run $SCRIPT_DIR/run_digi_reco.py
