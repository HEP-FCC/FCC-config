import os
import subprocess

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

############### Vertex Digitizer
from Configurables import DDPlanarDigi
import math
innerVertexResolution_x = 0.003 # [mm], assume 3 µm resolution for ARCADIA sensor
innerVertexResolution_y = 0.003 # [mm], assume 3 µm resolution for ARCADIA sensor
innerVertexResolution_t = 1000 # [ns]
outerVertexResolution_x = 0.050/math.sqrt(12) # [mm], assume ATLASPix3 sensor with 50 µm pitch
outerVertexResolution_y = 0.150/math.sqrt(12) # [mm], assume ATLASPix3 sensor with 150 µm pitch
outerVertexResolution_t = 1000 # [ns]

vtxb_digitizer = DDPlanarDigi("VTXBdigitizer")
vtxb_digitizer.SubDetectorName = "Vertex"
vtxb_digitizer.IsStrip = False
vtxb_digitizer.ResolutionU = [innerVertexResolution_x, innerVertexResolution_x, innerVertexResolution_x, outerVertexResolution_x, outerVertexResolution_x]
vtxb_digitizer.ResolutionV = [innerVertexResolution_y, innerVertexResolution_y, innerVertexResolution_y, outerVertexResolution_y, outerVertexResolution_y]
vtxb_digitizer.ResolutionT = [innerVertexResolution_t, innerVertexResolution_t, innerVertexResolution_t, outerVertexResolution_t, outerVertexResolution_t]
vtxb_digitizer.SimTrackHitCollectionName = ["VertexBarrelCollection"]
vtxb_digitizer.SimTrkHitRelCollection = ["VTXBSimDigiLinks"]
vtxb_digitizer.TrackerHitCollectionName = ["VTXBDigis"]
vtxb_digitizer.ForceHitsOntoSurface = True

vtxd_digitizer = DDPlanarDigi("VTXDdigitizer")
vtxd_digitizer.SubDetectorName = "Vertex"
vtxd_digitizer.IsStrip = False
vtxd_digitizer.ResolutionU = [outerVertexResolution_x, outerVertexResolution_x, outerVertexResolution_x]
vtxd_digitizer.ResolutionV = [outerVertexResolution_y, outerVertexResolution_y, outerVertexResolution_y]
vtxd_digitizer.ResolutionT = [outerVertexResolution_t, outerVertexResolution_t, outerVertexResolution_t]
vtxd_digitizer.SimTrackHitCollectionName = ["VertexEndcapCollection"]
vtxd_digitizer.SimTrkHitRelCollection = ["VTXDSimDigiLinks"]
vtxd_digitizer.TrackerHitCollectionName = ["VTXDDigis"]
vtxd_digitizer.ForceHitsOntoSurface = True

############### Wrapper Digitizer
siWrapperResolution_x   = 0.050/math.sqrt(12) # [mm]
siWrapperResolution_y   = 1.0/math.sqrt(12) # [mm]
siWrapperResolution_t   = 0.040 # [ns], assume 40 ps timing resolution for a single layer -> Should lead to <30 ps resolution when >1 hit

siwrb_digitizer = DDPlanarDigi("SiWrBdigitizer")
siwrb_digitizer.SubDetectorName = "SiWrB"
siwrb_digitizer.IsStrip = False
siwrb_digitizer.ResolutionU = [siWrapperResolution_x, siWrapperResolution_x]
siwrb_digitizer.ResolutionV = [siWrapperResolution_y, siWrapperResolution_y]
siwrb_digitizer.ResolutionT = [siWrapperResolution_t, siWrapperResolution_t]
siwrb_digitizer.SimTrackHitCollectionName = ["SiWrBCollection"]
siwrb_digitizer.SimTrkHitRelCollection = ["SiWrBSimDigiLinks"]
siwrb_digitizer.TrackerHitCollectionName = ["SiWrBDigis"]
siwrb_digitizer.ForceHitsOntoSurface = True

siwrd_digitizer = DDPlanarDigi("SiWrDdigitizer")
siwrd_digitizer.SubDetectorName = "SiWrD"
siwrd_digitizer.IsStrip = False
siwrd_digitizer.ResolutionU = [siWrapperResolution_x, siWrapperResolution_x]
siwrd_digitizer.ResolutionV = [siWrapperResolution_y, siWrapperResolution_y]
siwrd_digitizer.ResolutionT = [siWrapperResolution_t, siWrapperResolution_t]
siwrd_digitizer.SimTrackHitCollectionName = ["SiWrDCollection"]
siwrd_digitizer.SimTrkHitRelCollection = ["SiWrDSimDigiLinks"]
siwrd_digitizer.TrackerHitCollectionName = ["SiWrDDigis"]
siwrd_digitizer.ForceHitsOntoSurface = True

############### DCH Digitizer
from Configurables import DCHdigi_v02

dch_digitizer = DCHdigi_v02(
    "DCHdigi2",
    InputSimHitCollection=["DCHCollection"],
    OutputDigihitCollection = ["DCH_DigiCollection"],
    OutputLinkCollection = ["DCH_DigiSimAssociationCollection"],
    DCH_name="DCH_v2",
    zResolution_mm = 30.,               # in mm
    xyResolution_mm = 0.1,              # in mm
    Deadtime_ns = 400.0,                # in ns
    GasType=0,                          # 0: He(90%)-Isobutane(10%), 1: pure He, 2: Ar(50%)-Ethane(50%), 3: pure Ar
    ReadoutWindowStartTime_ns=1.0,      # in ns (taking into account time of flight, drift, and signal travel)
    ReadoutWindowDuration_ns=450.0,     # in ns
    DriftVelocity_um_per_ns=-1.0,       # in um/ns, if negative, automatically chosen based on GasType
    SignalVelocity_mm_per_ns=200.0,     # in mm/ns (Default: 2/3 of the speed of light)
    OutputLevel=INFO,
)

from Configurables import DDPlanarDigi

muon_digitizer = DDPlanarDigi()
muon_digitizer.SubDetectorName = "Muon-System"
muon_digitizer.EncodingStringParameterName = "MuonSystemReadoutID"
muon_digitizer.CellIDBits = "23"
muon_digitizer.IsStrip = False
muon_digitizer.ResolutionU = [0.4] # in mm, one value for all layers, or different values on the # of layers
muon_digitizer.ResolutionV = [0.4] # in mm, one value for all layers, or different values on the # of layers
muon_digitizer.ForceHitsOntoSurface = True
muon_digitizer.SimTrackHitCollectionName = ["MuonSystemCollection"]
muon_digitizer.SimTrkHitRelCollection = ["MSTrackerHitRelations"]
muon_digitizer.TrackerHitCollectionName = ["MSTrackerHits"]
#muon_digitizer.OutputLevel = 1  # DEBUG level

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

# Calculate dNdx from tracks
from Configurables import TrackdNdxDelphesBased
dNdxFromTracks = TrackdNdxDelphesBased("dNdxFromTracks",
                                  InputLinkCollection=tracksFromGenParticles.OutputMCRecoTrackParticleAssociation,
                                  OutputCollection=["DCHdNdxCollection"],
                                  ZmaxParameterName="DCH_gas_Lhalf",
                                  ZminParameterName="DCH_gas_Lhalf",
                                  RminParameterName="DCH_gas_inner_cyl_R",
                                  RmaxParameterName="DCH_gas_outer_cyl_R",
                                  FillFactor=1.0,
                                  OutputLevel=ERROR)


# Load the Geometric Graph Track Finder (GGTF), following example from:
# k4RecTracker/Tracking/test/testTrackFinder/runTestTrackFinder.py
from Configurables import GGTFTrackFinder

url = "https://key4hep.web.cern.ch/testFiles/k4RecTracker/SimpleGatrIDEAv3o1.onnx"
filename = "SimpleGatrIDEAv3o1.onnx"
subprocess.run(["wget", url, "-O", filename], check=True)
absolute_path = os.path.abspath(filename)

trackFinder = GGTFTrackFinder(
    "GGTFTrackFinder",
    InputPlanarHitCollections=["VTXBDigis", "VTXDDigis", "SiWrDDigis", "SiWrBDigis"],
    InputWireHitCollections=["DCH_DigiCollection"],
    OutputTracksGGTF=["CDCHTracks"],
    ModelPath=absolute_path,
    Tbeta=0.6,    # default clustering parameters
    Td=0.3,       # form the example in k4RecTracker
    OutputLevel=INFO,
)

# Track fitter using Genfit2, following example from
# k4RecTracker/Tracking/test/testTrackFitter/runTestTrackFitter.py
from Configurables import GenfitTrackFitter

trackFitter = GenfitTrackFitter(
    "GenfitTrackFitter",
    
    InputTracks=["CDCHTracks"],
    OutputFittedTracks=["CDCHFittedTracks"],
    RunSingleEvaluation = True,
    UseBrems = True,
    BetaInit = 100,
    BetaFinal = 0.1,
    BetaSteps = 15,
    InitializationType = 1,
    SkipTrackOrdering = False,
    FilterTrackHits = True,
    OutputLevel=INFO,
)

################ Dual-readout calorimeter
# SiPM emulation
from Configurables import SimulateSiPMwithEdep
sipmEdep = SimulateSiPMwithEdep("SimulateSiPMwithEdep",
    OutputLevel=DEBUG,
    inputHitCollection = "DRcaloSiPMreadout_scint",
    outputHitCollection = "DRcaloSiPMreadoutDigiHit_scint",
    outputTimeStructCollection = "DRcaloSiPMreadoutDigiWaveform_scint",
    readoutName = "DRcaloSiPMreadout",
    # wavelength in nm (decreasing order)
    wavelength = [
        900., 850., 800., 750., 725.,
        700., 675., 650., 625., 600.,
        590., 580., 570., 560., 550.,
        540., 530., 520., 510., 500.,
        490., 480., 470., 460., 450.,
        440., 430., 420., 400., 350.,
        300.
    ],
    # Hamamatsu S14160-1310PS
    sipmEfficiency = [
        0.02, 0.025, 0.045, 0.06, 0.0675,
        0.075, 0.0925, 0.11, 0.125, 0.14,
        0.146, 0.152, 0.158, 0.164, 0.17,
        0.173, 0.176, 0.178, 0.179, 0.18,
        0.181, 0.182, 0.183, 0.184, 0.18,
        0.173, 0.166, 0.158, 0.15, 0.12,
        0.05
    ],
    # Kuraray SCSF-78
    scintSpectrum = [
        0., 0., 0., 0., 0.,
        0., 0., 0.0003, 0.0008, 0.0032,
        0.0057, 0.0084, 0.0153, 0.0234, 0.0343,
        0.0604, 0.0927, 0.1398, 0.2105, 0.2903,
        0.4122, 0.5518, 0.7086, 0.8678, 1.,
        0.8676, 0.2311, 0.0033, 0.0012, 0.,
        0.
    ],
    # Kuraray SCSF-78
    absorptionLength = [
        2.714, 3.619, 5.791, 4.343, 7.896,
        5.429, 36.19, 17.37, 36.19, 5.429,
        13., 14.5, 16., 18., 16.5,
        17., 14., 16., 15., 14.5,
        13., 12., 10., 8., 7.238,
        4., 1.2, 0.5, 0.2, 0.2,
        0.1
    ],
    # Kodak Wratten 9
    filterEfficiency = [
        0.903, 0.903, 0.903, 0.903, 0.903,
        0.903, 0.902, 0.901, 0.898, 0.895,
        0.893, 0.891, 0.888, 0.883, 0.87,
        0.838, 0.76, 0.62, 0.488, 0.345,
        0.207, 0.083, 0.018, 0., 0.,
        0., 0., 0., 0., 0.,
        0.
    ],
    # empirical value to keep (scint npe / ceren npe) =~ 5
    scintYield = 0.565, # effective scintillation yield (k*13.6/keV)
                        # k responsible for numerical aperture
    scaleADC = 0.0003897, # equalization constant from ADC to GeV
    threshold = 1.5, # ADC integration threshold
    params = {"ccgv" : 0.25}, # cell-to-cell gain variation (and others if needed)
    gateLength = 80., # ns
    SNR = 14., # gain(10um)/gain(15um) = 0.5
)

from Configurables import SimulateSiPMwithOpticalPhoton
sipmOptical = SimulateSiPMwithOpticalPhoton("SimulateSiPMwithOpticalPhoton",
    OutputLevel=DEBUG,
    inputHitCollection = "DRcaloSiPMreadoutSimHit",
    inputTimeStructCollection = "DRcaloSiPMreadoutTimeStruct",
    inputWavlenCollection = "DRcaloSiPMreadoutWaveLen",
    outputHitCollection = "DRcaloSiPMreadoutDigiHit",
    outputTimeStructCollection = "DRcaloSiPMreadoutDigiWaveform",
    # wavelength in nm (decreasing order)
    wavelength = [
        900., 850., 800., 750., 725.,
        700., 675., 650., 625., 600.,
        590., 580., 570., 560., 550.,
        540., 530., 520., 510., 500.,
        490., 480., 470., 460., 450.,
        440., 430., 420., 400., 350.,
        300., 280.
    ],
    # Hamamatsu S14160-1315PS
    sipmEfficiency = [
        0.03, 0.05, 0.07, 0.1, 0.13,
        0.14, 0.16, 0.19, 0.21, 0.23,
        0.238, 0.246, 0.254, 0.262, 0.27,
        0.28, 0.29, 0.3, 0.31, 0.32,
        0.322, 0.324, 0.326, 0.328, 0.33,
        0.33, 0.32, 0.30, 0.27, 0.22,
        0.12, 0.
    ],
    scaleADC = 0.0005762, # equalization constant from ADC to GeV
    threshold = 1.5,
    cellpitch = 15., # um
    falltimeFast = 1.7, # ns
    gateLength = 80., # ns
    params = {
        "ccgv" : 0.15, # cell-to-cell gain variation
                       # responsible for a single photon peak std. dev.
        "falltimeslow" : 15., # ns
        "slowcomponentfraction" : 0.5 # signal = (1-f)*fast + f*slow
    },
)

# RNG for sipm emulation (TODO harmonize RNG with other modules)
from Configurables import HepRndm__Engine_CLHEP__RanluxEngine_ as RndmEngine
rndmEngine = RndmEngine('RndmGenSvc.Engine',
  SetSingleton = True,
  Seeds = [ 1234567 ] # default seed is 1234567
)

# DRC topoclustering
# use const noise tool for the moment
from Configurables import ConstNoiseTool
constNoiseTool = ConstNoiseTool("ConstNoiseTool",
    detectors = ["FiberDRCalo"],
    systemEncoding = "system:5",
    detectorsNoiseRMS = [0.001], # ad-hoc small value
    detectorsNoiseOffset = [0.],
    OutputLevel = INFO
)

from Configurables import CaloTopoClusterFCCee
topoClusterAll = CaloTopoClusterFCCee("topoClusterAll",
    cells = ["DRcaloSiPMreadoutDigiHit","DRcaloSiPMreadoutDigiHit_scint"],
    clusters = "TopoClusterAll",
    clusterCells = "TopoClusterAllCells",
    useNeighborMap = False,
    readoutName = "DRcaloSiPMreadout",
    neigboursTool = None,
    noiseTool = constNoiseTool,
    systemEncoding = "system:5",
    seedSigma = 4,
    neighbourSigma = 2,
    lastNeighbourSigma = 0,
    calorimeterIDs=[25],
    createClusterCellCollection=True,
    OutputLevel = INFO
)

from Configurables import CreateTruthLinks
createTruthLinks = CreateTruthLinks("CreateTruthLinks",
    cell_hit_links=["DRcaloSiPMreadoutDigiHit_scint_link"],
    clusters=["TopoClusterAll"],
    mcparticles="MCParticles",
    cell_mcparticle_links="CaloHitMCParticleLinks_scint",
    cluster_mcparticle_links="ClusterMCParticleLinks",
    OutputLevel=INFO
)

from Configurables import RndmGenSvc
rndmGenSvc = RndmGenSvc("RndmGenSvc",
  Engine = rndmEngine.name()
)

################ Output
io_svc.outputCommands = [
  "keep *",
  "drop *scintContrib*",
  "drop *Waveform*",
  "drop *DRcaloSiPMreadoutTimeStruct*",
  "drop *DRcaloSiPMreadoutWaveLen*"
]

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
        muon_digitizer,
        tracksFromGenParticles,
        plotTrackDCHHitDistances,
        dNdxFromTracks,
        trackFinder,
        trackFitter,
        sipmEdep,
        sipmOptical,
        topoClusterAll,
        createTruthLinks
    ],
    EvtSel = 'NONE',
    EvtMax = -1,
    ExtSvc = [
        root_hist_svc,
        EventDataSvc("EventDataSvc"),
        geoservice,
        audsvc,
        UniqueIDGenSvc("uidSvc"),
        rndmEngine,
        rndmGenSvc
    ],
    StopOnSignal = True,
)

for algo in application_mgr.TopAlg:
    algo.AuditExecute = True
