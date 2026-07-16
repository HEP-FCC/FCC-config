from DDSim.DD4hepSimulation import DD4hepSimulation
SIM = DD4hepSimulation()

## The compact XML file, or multiple compact files, if the last one is the closer.
import os
k4geo = os.getenv("K4GEO")
SIM.compactFile = os.path.join(k4geo, "FCCee/ALLEGRO/compact/ALLEGRO_o1_v03/ALLEGRO_o1_v03.xml")
## Lorentz boost for the crossing angle, in radian!
SIM.crossingAngleBoost = 0.015
SIM.enableDetailedShowerMode = True
## Outputfile from the simulation: .slcio, edm4hep.root and .root output files are supported
SIM.outputFile = "ALLEGRO_o1_v03_sim.root"
## Keep all DCH hits
SIM.filter.mapDetFilter["DCH_v2"] = "edep0"
SIM.action.mapActions["DCH_v2"] = "Geant4TrackerAction"
