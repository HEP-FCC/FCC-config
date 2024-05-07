# Instructions

## Setting the environment
If you need to modify the geometry, follow instructions [here](https://fcc-ee-detector-full-sim.docs.cern.ch/Key4hep/) to set-up the paths to your local k4geo installation. If you want to just use the central version of the detector, directly proceed with the following.

```
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
```

## Running the simulation
```
ddsim --enableGun --gun.distribution uniform --gun.energy "10*GeV" --gun.particle e- --numberOfEvents 100 --outputFile ALLEGRO_sim.root --random.enableEventSeed --random.seed 42 --compactFile $K4GEO/FCCee/ALLEGRO/compact/ALLEGRO_o1_v03/ALLEGRO_o1_v03.xml 
```

## Running the digitization and reconstruction
```
mkdir data
# Retrieve the files needed for digitization/reconstruction (e.g. noise values, machine learning models for calibration, ...)
# NB: if you do not have direct access to eos, you can retrieve those files from here: https://fccsw.web.cern.ch/fccsw/filesForSimDigiReco/ALLEGRO/ 
cp /eos/project/f/fccsw-web/www/filesForSimDigiReco/ALLEGRO/ALLEGRO_o1_v03/* data/
# run the digitization and reconstruction
k4run run_digi_reco.py
# you can then print the rootfile content with
podio-dump ALLEGRO_sim_digi_reco.root  
```
