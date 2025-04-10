# Instructions

## Setting the environment
If you need to modify the geometry, follow instructions [here](https://fcc-ee-detector-full-sim.docs.cern.ch/Key4hep/) to set-up the paths to your local k4geo installation. If you want to just use the central version of the detector, directly proceed with the following.

```
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
# Clone this repository if not done yet
git clone https://github.com/HEP-FCC/FCC-config/
cd FCC-config/FCCee/FullSim/IDEA/IDEA_o1_v03/
```

## Running the simulation
```
ddsim --enableGun --gun.distribution uniform --gun.energy "10*GeV" --gun.particle e- --numberOfEvents 10 --outputFile IDEA_sim.root --random.enableEventSeed --random.seed 42 --compactFile $K4GEO/FCCee/IDEA/compact/IDEA_o1_v03/IDEA_o1_v03.xml --steeringFile SteeringFile_IDEA_o1_v03.py
```

## Running the digitization and reconstruction
```
# First get the data needed for the DCH cluster counting parametrization (still work in progress)
wget --no-clobber https://fccsw.web.cern.ch/fccsw/filesForSimDigiReco/IDEA/DataAlgFORGEANT.root
k4run run_digi_reco.py
# you can then print the rootfile content with
podio-dump IDEA_sim_digi_reco.root  
```
