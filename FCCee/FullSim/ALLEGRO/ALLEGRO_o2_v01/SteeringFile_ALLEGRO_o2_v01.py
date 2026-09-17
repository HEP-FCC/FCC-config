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

def Geant4Output2EDM4hep_DRC_plugin(dd4hepSimulation):
    from DDG4 import EventAction, Kernel

    shared = dd4hepSimulation.numberOfThreads > 1
    evt_root = EventAction(
        Kernel(), "Geant4Output2EDM4hep_DRC/" + dd4hepSimulation.outputFile, shared
    )
    evt_root.Control = True
    output = dd4hepSimulation.outputFile
    evt_root.Output = output
    evt_root.enableUI()
    Kernel().eventAction().add(evt_root)
    return None

SIM.outputConfig.userOutputPlugin = Geant4Output2EDM4hep_DRC_plugin