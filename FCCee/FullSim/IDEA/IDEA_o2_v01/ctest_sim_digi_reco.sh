#!/bin/bash
# CI: IDEA_o2_v01 sim + digi/reco on the reduced barrel wedge.
set -e

# --- Default Values ---
PARTICLE="pi-"
ENERGY="10*GeV"
INPUT_FILE=""
OUTPUT_FILE="o2_v01"
N_EVENTS=5
RANDOM_SEED=""

# --- Help Function ---
print_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo "  --particle    Particle type for ddsim gun (default: pi-)"
    echo "  --energy      Energy for ddsim gun (default: 10*GeV)"
    echo "  --inputFile   Path to an input file (disables particle gun)"
    echo "  --outputFile  Base name for output files (default: o2_v01)"
    echo "  --nEvents     Number of events to simulate (default: 5)"
    echo "  --seed        Random seed for ddsim (optional)"
    exit 1
}

# --- Parse Keyword Arguments ---
while [[ $# -gt 0 ]]; do
    case $1 in
        --particle)
            PARTICLE="$2"; shift 2 ;;
        --energy)
            ENERGY="$2"; shift 2 ;;
        --inputFile)
            INPUT_FILE="$2"; shift 2 ;;
        --outputFile)
            OUTPUT_FILE="$2"; shift 2 ;;
        --nEvents)
            N_EVENTS="$2"; shift 2 ;;
        --seed)
            RANDOM_SEED="$2"; shift 2 ;;
        -h|--help)
            print_usage ;;
        *)
            echo "Error: Unknown option $1"
            print_usage ;;
    esac
done

# --- Key4hep Setup ---
if [[ -z "${KEY4HEP_STACK}" ]]; then
    echo "Sourcing Key4hep environment..."
    source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
else
    echo "The Key4hep stack is already loaded."
fi

# Workaround to have ctests working (get the directory of this script)
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

# --- Build ddsim command ---
DDSIM_CMD=(
ddsim
--outputFile "IDEA_${OUTPUT_FILE}_sim.root"
--compactFile "${K4GEO}/FCCee/IDEA/compact/IDEA_o2_v01_CI/IDEA_o2_v01_CI.xml"
--steeringFile "${SCRIPT_DIR}/SteeringFile_IDEA_o2_v01.py"
--numberOfEvents "${N_EVENTS}"
)

# Append seed flags if a seed is specified
if [[ -n "${RANDOM_SEED}" ]]; then
    DDSIM_CMD+=(
    --random.enableEventSeed
    --random.seed "${RANDOM_SEED}"
    )
fi

if [[ -n "${INPUT_FILE}" ]]; then
    echo "Using input file: ${INPUT_FILE} (Particle gun disabled)"
    DDSIM_CMD+=(--inputFiles "${INPUT_FILE}")
else
    echo "Using particle gun: ${N_EVENTS} event(s) of ${PARTICLE} at ${ENERGY}"
    # fixed direction: the reduced geometry only covers a barrel wedge
    DDSIM_CMD+=(
    --enableGun
    --gun.direction "0.966,0.259,0.01"
    --gun.energy "${ENERGY}"
    --gun.particle "${PARTICLE}"
    --crossingAngleBoost 0.0
    )
fi

# Run the SIM step
echo "Running: ${DDSIM_CMD[*]}"
"${DDSIM_CMD[@]}"

# --- DIGI/RECO Step ---
DIGI_CMD=(
k4run "${SCRIPT_DIR}/run_digi_reco.py"
--ci
--IOSvc.Input "IDEA_${OUTPUT_FILE}_sim.root"
--IOSvc.Output "IDEA_${OUTPUT_FILE}_digi_reco.root"
)

echo "Running: ${DIGI_CMD[*]}"
"${DIGI_CMD[@]}"

# Sanity: the two final products -- truth tracks and topo clusters.
python3 "${SCRIPT_DIR}/check_digi_reco.py" "IDEA_${OUTPUT_FILE}_digi_reco.root"

echo "Completed successfully"
