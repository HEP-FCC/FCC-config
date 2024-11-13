# Instructions

## Setting the environment
If you need to modify the geometry, follow instructions [here](https://fcc-ee-detector-full-sim.docs.cern.ch/Key4hep/) to set-up the paths to your local k4geo installation. If you want to just use the central version of the detector, directly proceed with the following.

```
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
```


## Running the simulation
You can produce a file containing the Geant4 simulated hits in the detector with:
```
ddsim --enableGun --gun.distribution uniform --gun.energy "10*GeV" --gun.particle e- --numberOfEvents 100 --outputFile ALLEGRO_sim.root --random.enableEventSeed --random.seed 42 --compactFile $K4GEO/FCCee/ALLEGRO/compact/ALLEGRO_o1_v03/ALLEGRO_o1_v03.xml 
```

You can also retrieve a simulation file already produced from here: `https://fccsw.web.cern.ch/fccsw/filesForSimDigiReco/ALLEGRO/ALLEGRO_o1_v03/forTests/pythia_ee_z_qq_10evt_ALLEGRO_sim.root`


## Running the digitization and reconstruction

Retrieve the files needed later for digitization/reconstruction (e.g. noise values, machine learning models for calibration, ...)
NB: if you do not have direct access to eos, you can retrieve those files from here: `https://fccsw.web.cern.ch/fccsw/filesForSimDigiReco/ALLEGRO/`
```
cp /eos/project/f/fccsw-web/www/filesForSimDigiReco/ALLEGRO/ALLEGRO_o1_v03/* .
```
or
```
scp <user>@lxplus.cern.ch:/eos/project/f/fccsw-web/www/filesForSimDigiReco/ALLEGRO/ALLEGRO_o1_v03/* .
```

Run the reconstruction with:
```
k4run run_digi_reco.py
# you can then print the rootfile content with
podio-dump ALLEGRO_sim_digi_reco.root  
```

This will run by default on the `ALLEGRO_sim.root` file. To run on a different file (e.g. `pythia_ee_z_qq_10evt_ALLEGRO_sim.root`) use:
```
k4run run_digi_reco.py --IOSvc.Input <inputfile>
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
