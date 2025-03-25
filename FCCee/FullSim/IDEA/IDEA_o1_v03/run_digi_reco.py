import os

from Gaudi.Configuration import *

# Loading the input SIM file, defining output file
from k4FWCore import IOSvc
from Configurables import EventDataSvc
io_svc = IOSvc("IOSvc")
io_svc.Input = "IDEA_sim.root"
io_svc.Output = "IDEA_sim_digi_reco.root"


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
innerVertexResolution_x = 0.003 # [mm], assume 3 µm resolution for ARCADIA sensor
innerVertexResolution_y = 0.003 # [mm], assume 3 µm resolution for ARCADIA sensor
innerVertexResolution_t = 1000 # [ns]
outerVertexResolution_x = 0.050/math.sqrt(12) # [mm], assume ATLASPix3 sensor with 50 µm pitch
outerVertexResolution_y = 0.150/math.sqrt(12) # [mm], assume ATLASPix3 sensor with 150 µm pitch
outerVertexResolution_t = 1000 # [ns]

vtxb_digitizer = VTXdigitizer("VTXBdigitizer",
    inputSimHits = "VertexBarrelCollection",
    outputDigiHits = "VTXBDigis",
    outputSimDigiAssociation = "VTXBSimDigiLinks",
    detectorName = "Vertex",
    readoutName = "VertexBarrelCollection",
    xResolution = [innerVertexResolution_x, innerVertexResolution_x, innerVertexResolution_x, outerVertexResolution_x, outerVertexResolution_x], # mm, r-phi direction
    yResolution = [innerVertexResolution_y, innerVertexResolution_y, innerVertexResolution_y, outerVertexResolution_y, outerVertexResolution_y], # mm, z direction
    tResolution = [innerVertexResolution_t, innerVertexResolution_t, innerVertexResolution_t, outerVertexResolution_t, outerVertexResolution_t],
    forceHitsOntoSurface = False,
    OutputLevel = INFO
)

vtxd_digitizer  = VTXdigitizer("VTXDdigitizer",
    inputSimHits = "VertexEndcapCollection",
    outputDigiHits = "VTXDDigis",
    outputSimDigiAssociation = "VTXDSimDigiLinks",
    detectorName = "Vertex",
    readoutName = "VertexEndcapCollection",
    xResolution = [outerVertexResolution_x, outerVertexResolution_x, outerVertexResolution_x], # mm, r direction
    yResolution = [outerVertexResolution_y, outerVertexResolution_y, outerVertexResolution_y], # mm, phi direction
    tResolution = [outerVertexResolution_t, outerVertexResolution_t, outerVertexResolution_t], # ns
    forceHitsOntoSurface = False,
    OutputLevel = INFO
)

# digitise silicon wrapper hits
siWrapperResolution_x   = 0.050/math.sqrt(12) # [mm]
siWrapperResolution_y   = 1.0/math.sqrt(12) # [mm]
siWrapperResolution_t   = 0.040 # [ns], assume 40 ps timing resolution for a single layer -> Should lead to <30 ps resolution when >1 hit

siwrb_digitizer = VTXdigitizer("SiWrBdigitizer",
    inputSimHits = "SiWrBCollection",
    outputDigiHits = "SiWrBDigis",
    outputSimDigiAssociation = "SiWrBSimDigiLinks",
    detectorName = "SiWrB",
    readoutName = "SiWrBCollection",
    xResolution = [siWrapperResolution_x, siWrapperResolution_x], # mm, r-phi direction
    yResolution = [siWrapperResolution_y, siWrapperResolution_y], # mm, z direction
    tResolution = [siWrapperResolution_t, siWrapperResolution_t],
    forceHitsOntoSurface = False,
    OutputLevel = INFO
)

siwrd_digitizer = VTXdigitizer("SiWrDdigitizer",
    inputSimHits = "SiWrDCollection",
    outputDigiHits = "SiWrDDigis",
    outputSimDigiAssociation = "SiWrDSimDigiLinks",
    detectorName = "SiWrD",
    readoutName = "SiWrDCollection",
    xResolution = [siWrapperResolution_x, siWrapperResolution_x], # mm, r-phi direction
    yResolution = [siWrapperResolution_y, siWrapperResolution_y], # mm, z direction
    tResolution = [siWrapperResolution_t, siWrapperResolution_t],
    forceHitsOntoSurface = False,
    OutputLevel = INFO
)

from Configurables import DCHdigi_v01
dch_digitizer = DCHdigi_v01("DCHdigi",
    DCH_simhits = ["DCHCollection"],
    DCH_name = "DCH_v2",
    fileDataAlg = "DataAlgFORGEANT.root",
    calculate_dndx = False, # cluster counting disabled (to be validated, see FCC-config#239)
    create_debug_histograms = True,
    zResolution_mm = 30., # in mm - Note: At this point, the z resolution comes without the stereo measurement
    xyResolution_mm = 0.1 # in mm
)

# Create tracks from gen particles
from Configurables import TracksFromGenParticles
tracksFromGenParticles = TracksFromGenParticles("CreateTracksFromGenParticles",
                                                InputGenParticles = ["MCParticles"],
                                                InputSimTrackerHits=[
                                                    "VertexBarrelCollection",
                                                    "VertexEndcapCollection",
                                                    "DCHCollection",
                                                    "SiWrBCollection",
                                                    "SiWrDCollection"
                                                ],
                                                OutputTracks = ["TracksFromGenParticles"],
                                                OutputMCRecoTrackParticleAssociation = ["TracksFromGenParticlesAssociation"],
                                                ExtrapolateToECal=False,
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
io_svc.outputCommands = ["keep *"]

# Profiling
from Configurables import AuditorSvc, ChronoAuditor, UniqueIDGenSvc
chra = ChronoAuditor()
audsvc = AuditorSvc()
audsvc.Auditors = [chra]

from k4FWCore import ApplicationMgr
application_mgr = ApplicationMgr(
    TopAlg = [
              vtxb_digitizer,
              vtxd_digitizer,
              siwrb_digitizer,
              siwrd_digitizer,
              dch_digitizer,
              tracksFromGenParticles, 
              plotTrackDCHHitDistances,
              ],
    EvtSel = 'NONE',
    EvtMax   = -1,
    ExtSvc = ['RndmGenSvc', root_hist_svc, EventDataSvc("EventDataSvc"), geoservice, audsvc, UniqueIDGenSvc("uidSvc")],
    StopOnSignal = True,
 )

for algo in application_mgr.TopAlg:
    algo.AuditExecute = True
