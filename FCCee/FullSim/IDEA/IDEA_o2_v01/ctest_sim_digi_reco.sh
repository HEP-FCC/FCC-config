#!/bin/bash
# CI: IDEA_o2_v01 sim + digi/reco on the reduced barrel wedge.
#   ddsim a pi- into the wedge -> tracker digi, truth tracks, optical calo digi, clustering.
set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

ddsim --compactFile "${K4GEO}/FCCee/IDEA/compact/IDEA_o2_v01_CI/IDEA_o2_v01_CI.xml" \
      --steeringFile "${SCRIPT_DIR}/SteeringFile_IDEA_o2_v01.py" \
      --enableGun --gun.particle pi- --gun.energy 10*GeV \
      --gun.direction "0.966,0.259,0.01" --crossingAngleBoost 0.0 \
      --numberOfEvents 5 --random.enableEventSeed --random.seed 42 \
      --outputFile IDEA_o2_v01_sim.root

k4run "${SCRIPT_DIR}/run_digi_reco.py" \
      --IOSvc.Input IDEA_o2_v01_sim.root \
      --IOSvc.Output IDEA_o2_v01_digi_reco.root

# Sanity: at least one topo cluster must have been grown.
python3 - <<'EOF'
import sys, podio.reading
r = podio.reading.get_reader("IDEA_o2_v01_digi_reco.root")
n = sum(len(f.get("TopoGrownClusters")) for f in r.get("events"))
print("TopoGrownClusters produced:", n)
sys.exit(0 if n > 0 else 1)
EOF
