from DDSim.DD4hepSimulation import DD4hepSimulation
SIM = DD4hepSimulation()

## The compact XML file, or multiple compact files, if the last one is the closer.
import os
k4geo = os.getenv("K4GEO")
SIM.compactFile = os.path.join(k4geo, "FCCee/ALLEGRO/compact/ALLEGRO_o2_v01/ALLEGRO_o2_v01.xml")
## Lorentz boost for the crossing angle, in radian!
SIM.crossingAngleBoost = 0.015
SIM.enableDetailedShowerMode = True
## Outputfile from the simulation: .slcio, edm4hep.root and .root output files are supported
SIM.outputFile = "allegro_o2_v01_sim.root"
## Keep all STT hits
SIM.filter.mapDetFilter["STT_o1_v01"] = "edep0"
SIM.action.mapActions["STT_o1_v01"] = "Geant4TrackerAction"
