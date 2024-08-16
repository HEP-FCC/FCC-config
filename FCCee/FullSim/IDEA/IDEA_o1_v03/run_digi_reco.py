import os

from Gaudi.Configuration import *

# For when we will migrate to IOSvc (remove the output below as well)
# Loading the input SIM file, defining output file
#from k4FWCore import IOSvc
#io_svc = IOSvc("IOSvc")
#io_svc.input = "IDEA_sim.root"
#io_svc.output = "IDEA_sim_digi_reco.root"

# For now still use the old IO service
from Configurables import k4DataSvc, PodioInput
evtsvc = k4DataSvc('EventDataSvc')
evtsvc.input = "IDEA_sim.root"
inp = PodioInput('InputReader')
inp.AuditExecute = True


################## Simulation setup
# Detector geometry
from Configurables import GeoSvc
geoservice = GeoSvc("GeoSvc")
path_to_detector = os.environ.get("K4GEO", "")
print(path_to_detector)
detectors_to_use=[
                    'FCCee/IDEA/compact/IDEA_o1_v03/IDEA_o1_v03.xml'
                  ]
# prefix all xmls with path_to_detector
geoservice.detectors = [os.path.join(path_to_detector, _det) for _det in detectors_to_use]
geoservice.OutputLevel = INFO

# digitize vertex hits
from Configurables import VTXdigitizer
import math
innerVertexResolution_x = 0.003 # [mm], assume 5 µm resolution for ARCADIA sensor
innerVertexResolution_y = 0.003 # [mm], assume 5 µm resolution for ARCADIA sensor
innerVertexResolution_t = 1000 # [ns]
outerVertexResolution_x = 0.050/math.sqrt(12) # [mm], assume ATLASPix3 sensor with 50 µm pitch
outerVertexResolution_y = 0.150/math.sqrt(12) # [mm], assume ATLASPix3 sensor with 150 µm pitch
outerVertexResolution_t = 1000 # [ns]

vtxib_digitizer = VTXdigitizer("VTXIBdigitizer",
    inputSimHits = "VTXIBCollection",
    outputDigiHits = "VTXIBDigis",
    outputSimDigiAssociation = "VTXIBSimDigiLinks",
    detectorName = "Vertex",
    readoutName = "VTXIBCollection",
    xResolution = innerVertexResolution_x, # mm, r-phi direction
    yResolution = innerVertexResolution_y, # mm, z direction
    tResolution = innerVertexResolution_t,
    forceHitsOntoSurface = False,
    OutputLevel = INFO
)

vtxob_digitizer = VTXdigitizer("VTXOBdigitizer",
    inputSimHits = "VTXOBCollection",
    outputDigiHits = "VTXOBDigis",
    outputSimDigiAssociation = "VTXOBSimDigiLinks",
    detectorName = "Vertex",
    readoutName = "VTXOBCollection",
    xResolution = outerVertexResolution_x, # mm, r-phi direction
    yResolution = outerVertexResolution_y, # mm, z direction
    tResolution = outerVertexResolution_t, # ns
    forceHitsOntoSurface = False,
    OutputLevel = INFO
)

vtxd_digitizer  = VTXdigitizer("VTXDdigitizer",
    inputSimHits = "VTXDCollection",
    outputDigiHits = "VTXDDigis",
    outputSimDigiAssociation = "VTXDSimDigiLinks",
    detectorName = "Vertex",
    readoutName = "VTXDCollection",
    xResolution = outerVertexResolution_x, # mm, r direction
    yResolution = outerVertexResolution_y, # mm, phi direction
    tResolution = outerVertexResolution_t, # ns
    forceHitsOntoSurface = False,
    OutputLevel = INFO
)

# digitize drift chamber hits, waiting to merge the digitizer for the new drift chamber
#from Configurables import DCHsimpleDigitizerExtendedEdm
#dch_digitizer = DCHsimpleDigitizerExtendedEdm("DCHsimpleDigitizerExtendedEdm",
#    inputSimHits = "CDCHHits",
#    outputDigiHits = "CDCHDigis",
#    outputSimDigiAssociation = "DC_simDigiAssociation",
#    readoutName = "CDCHHits",
#    xyResolution = 0.1, # mm
#    zResolution = 1, # mm
#    debugMode = True,
#    OutputLevel = INFO
#)

# Create tracks from gen particles
from Configurables import TracksFromGenParticles
tracksFromGenParticles = TracksFromGenParticles("TracksFromGenParticles",
                                               InputGenParticles = ["MCParticles"],
                                               OutputTracks = ["TracksFromGenParticles"],
                                               OutputMCRecoTrackParticleAssociation = ["TracksFromGenParticlesAssociation"],
                                               Bz = 2.0,
                                               OutputLevel = INFO)

# produce a TH1 with distances between gen tracks and simTrackerHits
from Configurables import PlotTrackHitDistances, RootHistSvc
from Configurables import Gaudi__Histograming__Sink__Root as RootHistoSink
plotTrackDCHHitDistances = PlotTrackHitDistances("PlotTrackDCHHitDistances",
                                             InputSimTrackerHits = ["DCHCollection"],
                                             InputTracksFromGenParticlesAssociation = tracksFromGenParticles.OutputMCRecoTrackParticleAssociation,
                                             Bz = 2.0)

hps = RootHistSvc("HistogramPersistencySvc")
root_hist_svc = RootHistoSink("RootHistoSink")
root_hist_svc.FileName = "TrackHitDistances.root"

################ Output
from Configurables import PodioOutput
out = PodioOutput("out",
                  OutputLevel=INFO)
out.outputCommands = ["keep *"]
out.filename = "IDEA_sim_digi_reco.root"

# Profiling
from Configurables import AuditorSvc, ChronoAuditor
chra = ChronoAuditor()
audsvc = AuditorSvc()
audsvc.Auditors = [chra]

from Configurables import ApplicationMgr
application_mgr = ApplicationMgr(
    TopAlg = [
			  inp,
              vtxib_digitizer,
              vtxob_digitizer,
              vtxd_digitizer,
              #dch_digitizer,
              tracksFromGenParticles, 
              plotTrackDCHHitDistances,
              out
              ],
    EvtSel = 'NONE',
    EvtMax   = -1,
    #ExtSvc = [root_hist_svc, EventDataSvc("EventDataSvc"), geoservice, audsvc],
    ExtSvc = [root_hist_svc, geoservice, evtsvc, audsvc],
    StopOnSignal = True,
 )

for algo in application_mgr.TopAlg:
    algo.AuditExecute = True
