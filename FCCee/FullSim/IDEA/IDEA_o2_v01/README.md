# IDEA option 2
`IDEA_o2` is a variation of the FCCee IDEA Detector which adopts a dual-readout crystal electromagnetic calorimeter, followed by a dual-readout absorber-tubes-based hadronic calorimeter. Most of the remaining subdetectors are common with the previous IDEA version, `IDEA_o1`.

# Instructions

## Setting the environment
If you need to modify the geometry, follow instructions [here](https://fcc-ee-detector-full-sim.docs.cern.ch/Key4hep/) to set-up the paths to your local k4geo installation. If you want to just use the central version of the detector, directly proceed with the following.

```
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
# Clone this repository if not done yet
git clone https://github.com/HEP-FCC/FCC-config/
cd FCC-config/FCCee/FullSim/IDEA/IDEA_o2_v01/
```

## Running the simulation
It is recommended to run the simulation with the `Steering File` provided here because it associates sensitive actions to calorimeters as intended by the developers.

```
ddsim --enableGun --gun.distribution uniform --gun.energy "10*GeV" --gun.particle e- --crossingAngleBoost 0 --numberOfEvents 10 --random.enableEventSeed --random.seed 42 --outputFile IDEA_sim.root --compactFile $K4GEO/FCCee/IDEA/compact/IDEA_o2_v01/IDEA_o2_v01.xml --steeringFile SteeringFile_IDEA_o2_v01.py
```

## Running the digitization and reconstruction
This section will be included as soon as the `IDEA_o2` specific digitization code will be merged.
