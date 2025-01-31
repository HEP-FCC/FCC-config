# Instructions

## Setting the environment
If you need to modify the geometry, follow instructions [here](https://fcc-ee-detector-full-sim.docs.cern.ch/Key4hep/) to set-up the paths to your local k4geo installation. If you want to just use the central version of the detector, directly proceed with the following.

```
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
# Clone this repository if not done yet
git clone https://github.com/HEP-FCC/FCC-config/
cd FCC-config/FCCee/FullSim/ALLEGRO/ALLEGRO_o1_v02/
```

## Running the simulation
```
ddsim --enableGun --gun.distribution uniform --gun.energy "10*GeV" --gun.particle e- --numberOfEvents 100 --outputFile ALLEGRO_sim.root --random.enableEventSeed --random.seed 42 --compactFile $K4GEO/FCCee/ALLEGRO/compact/ALLEGRO_o1_v02/ALLEGRO_o1_v02.xml 
```

## Running the digitization and reconstruction
```
mkdir data
cd data
curl -O -L http://fccsw.web.cern.ch/fccsw/filesForSimDigiReco/ALLEGRO/ALLEGRO_o1_v02/elecNoise_ecalBarrelFCCee_theta.root
curl -O -L http://fccsw.web.cern.ch/fccsw/filesForSimDigiReco/ALLEGRO/ALLEGRO_o1_v02/cellNoise_map_electronicsNoiseLevel_thetamodulemerged.root
curl -O -L http://fccsw.web.cern.ch/fccsw/filesForSimDigiReco/ALLEGRO/ALLEGRO_o1_v02/neighbours_map_barrel_thetamodulemerged.root
cd ..
k4run run_digi_reco.py
# you can then print the rootfile content with
podio-dump ALLEGRO_sim_digi_reco.root  
```
