# Instructions


<sub>These instructions (and the ctest) are taken from IDEA/ALLEGRO and modified where relevant.</sub>

## Setting the environment
If you need to modify the geometry, follow instructions [here](https://fcc-ee-detector-full-sim.docs.cern.ch/Key4hep/) to set-up the paths to your local k4geo installation. If you want to just use the central version of the detector, directly proceed with the following.

```
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
# Clone this repository if not done yet
git clone https://github.com/HEP-FCC/FCC-config/
cd FCC-config/FCCee/FullSim/ALFA/ALFA_o1_v00/
```

## Running the simulation
You can produce a file containing the Geant4 simulated hits in the detector with:
```
ddsim --enableGun --gun.distribution uniform --gun.energy "10*GeV" --gun.particle e- --numberOfEvents 100 --outputFile ALFA_o1_v00_sim.root --random.enableEventSeed --random.seed 42 --compactFile $K4GEO/FCCee/ALFA/compact/ALFA_o1_v00/ALFA_o1_v00.xml 
```

## Running the digitization and reconstruction
[To be implemented]


