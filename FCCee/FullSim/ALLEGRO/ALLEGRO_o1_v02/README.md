# Instructions

## Setting the environment
If you need to modify the geometry, follow instructions [here](https://fcc-ee-detector-full-sim.docs.cern.ch/Key4hep/) to set-up the paths to your local k4geo installation. If you want to just use the central version of the detector, directly proceed with the following.

```
source /cvmfs/sw-nightlies.hsf.org/key4hep/setup.sh
```

## Running the simulation
```
ddsim --enableGun --gun.distribution uniform --gun.energy "10*GeV" --gun.particle e- --numberOfEvents 100 --outputFile ALLEGRO_sim.root --random.enableEventSeed --random.seed 42 --compactFile $K4GEO/FCCee/ALLEGRO/compact/ALLEGRO_o1_v02/ALLEGRO_o1_v02.xml 
```

## Running the digitization and reconstruction
```
# if eos is mounted
mkdir data
cp /eos/user/b/brfranco/rootfile_storage/elecNoise_ecalBarrelFCCee_theta.root data/
cp /eos/user/g/gmarchio/rootfile_storage/neighbours_map_barrel_thetamodulemerged.root data/
cp /eos/user/g/gmarchio/rootfile_storage/cellNoise_map_electronicsNoiseLevel_thetamodulemerged.root data/
# if not, do the same as above with scp yourlogin@lxplus.cern.ch:/eos/user/b/brfranco/rootfile_storage/elecNoise_ecalBarrelFCCee_theta.root data/ etc
k4run run_digi_reco.py 
# you can inspect the rootfile content with 
podio-dump ALLEGRO_sim_digi_reco.root  
```
