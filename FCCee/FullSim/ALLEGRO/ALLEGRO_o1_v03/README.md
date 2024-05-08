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
# Retrieve the files needed for digitization/reconstruction (e.g. noise values, machine learning models for calibration, ...)
# NB: if you do not have direct access to eos, you can retrieve those files from here: https://fccsw.web.cern.ch/fccsw/filesForSimDigiReco/ALLEGRO/ 
cp /eos/project/f/fccsw-web/www/filesForSimDigiReco/ALLEGRO/ALLEGRO_o1_v03/* .
# run the digitization and reconstruction
k4run run_digi_reco.py
# you can then print the rootfile content with
podio-dump ALLEGRO_sim_digi_reco.root  
```

## Dirac submission
The following is not yet ready, we have to implement ddsim as a generator in diract to do particle gun transformation
You need to create a tarball containing the files needed for reconstruction and upload it at the right place with dirac commands
```
# In lxplus
source /cvmfs/clicdp.cern.ch/DIRAC/bashrc; dirac-proxy-init -g fcc_prod
./create_dirac_tarball.sh
dirac-dms-add-file LFN:/fcc/prod/software/fccconfig/fccconfig-ALLEGRO_o1_v03-devel.tgz fccconfig-ALLEGRO_o1_v03-devel.tgz CERN-DST-EOS
```
