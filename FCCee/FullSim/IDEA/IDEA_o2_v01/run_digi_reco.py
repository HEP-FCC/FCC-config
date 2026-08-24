import os
import math

from Gaudi.Configuration import *

# Reduced barrel wedge (fast, low memory) vs the full detector.
# Set to False to run the full IDEA_o2_v01 geometry -- note it needs considerably more memory,
# and the ddsim step must then be given the full compact file too.
CI = True

detector_xml = (
    "FCCee/IDEA/compact/IDEA_o2_v01_CI/IDEA_o2_v01_CI.xml"
    if CI
    else "FCCee/IDEA/compact/IDEA_o2_v01/IDEA_o2_v01.xml"
)

# Loading the input SIM file, defining output file
from k4FWCore import IOSvc
from Configurables import EventDataSvc
io_svc = IOSvc("IOSvc")
io_svc.Input = "IDEA_o2_v01_sim.root"
io_svc.Output = "IDEA_o2_v01_digi_reco.root"
io_svc.outputCommands = ["keep *"]

################## Simulation setup
# Detector geometry
from Configurables import GeoSvc
geoservice = GeoSvc("GeoSvc")
path_to_detector = os.environ.get("K4GEO", "")
geoservice.detectors = [os.path.join(path_to_detector, detector_xml)]
geoservice.OutputLevel = INFO

############### Vertex Digitizer
from Configurables import DDPlanarDigi
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
siWrapperResolution_t   = 0.040 # [ns], 40 ps per layer -> <30 ps when >1 hit

siwrb_digitizer = DDPlanarDigi("SiWrBdigitizer")
siwrb_digitizer.SubDetectorName = "SiWrB"
siwrb_digitizer.IsStrip = False
siwrb_digitizer.ResolutionU = [siWrapperResolution_x]*4
siwrb_digitizer.ResolutionV = [siWrapperResolution_y]*4
siwrb_digitizer.ResolutionT = [siWrapperResolution_t]*4
siwrb_digitizer.SimTrackHitCollectionName = ["SiWrBCollection"]
siwrb_digitizer.SimTrkHitRelCollection = ["SiWrBSimDigiLinks"]
siwrb_digitizer.TrackerHitCollectionName = ["SiWrBDigis"]
siwrb_digitizer.ForceHitsOntoSurface = True

siwrd_digitizer = DDPlanarDigi("SiWrDdigitizer")
siwrd_digitizer.SubDetectorName = "SiWrD"
siwrd_digitizer.IsStrip = False
siwrd_digitizer.ResolutionU = [siWrapperResolution_x]*4
siwrd_digitizer.ResolutionV = [siWrapperResolution_y]*4
siwrd_digitizer.ResolutionT = [siWrapperResolution_t]*4
siwrd_digitizer.SimTrackHitCollectionName = ["SiWrDCollection"]
siwrd_digitizer.SimTrkHitRelCollection = ["SiWrDSimDigiLinks"]
siwrd_digitizer.TrackerHitCollectionName = ["SiWrDDigis"]
siwrd_digitizer.ForceHitsOntoSurface = True

############### DCH Digitizer
from Configurables import DCHdigi_v02
dch_digitizer = DCHdigi_v02(
    "DCHdigi2",
    InputSimHitCollection=["DCHCollection"],
    OutputDigihitCollection=["DCHDigis"],
    OutputLinkCollection=["DCHDigisSimAssociationCollection"],
    DCH_name="DCH_v2",
    zResolution_mm=30.,                 # in mm
    xyResolution_mm=0.1,                # in mm
    Deadtime_ns=400.0,                  # in ns
    GasType=0,                          # 0: He(90%)-Isobutane(10%)
    ReadoutWindowStartTime_ns=1.0,
    ReadoutWindowDuration_ns=450.0,
    DriftVelocity_um_per_ns=-1.0,       # negative -> chosen from GasType
    SignalVelocity_mm_per_ns=200.0,
    OutputLevel=INFO,
)

############### Muon Digitizer
muon_digitizer = DDPlanarDigi()
muon_digitizer.SubDetectorName = "Muon-System"
muon_digitizer.EncodingStringParameterName = "MuonSystemReadoutID"
muon_digitizer.CellIDBits = "23"
muon_digitizer.IsStrip = False
muon_digitizer.ResolutionU = [0.4] # in mm
muon_digitizer.ResolutionV = [0.4] # in mm
muon_digitizer.ForceHitsOntoSurface = True
muon_digitizer.SimTrackHitCollectionName = ["MuonSystemCollection"]
muon_digitizer.SimTrkHitRelCollection = ["MSTrackerHitRelations"]
muon_digitizer.TrackerHitCollectionName = ["MSTrackerHits"]

############### Tracks from gen particles
# ExtrapolateToECal=True is required downstream: pandora needs the AtCalorimeter track state,
# and a track without one carries no calorimeter position.
from Configurables import TracksFromGenParticles
tracksFromGenParticles = TracksFromGenParticles("CreateTracksFromGenParticles",
                                                InputGenParticles=["MCParticles"],
                                                InputSimTrackerHits=[
                                                    "VertexBarrelCollection",
                                                    "VertexEndcapCollection",
                                                    "DCHCollection",
                                                    "SiWrBCollection",
                                                    "SiWrDCollection"
                                                ],
                                                OutputTracks=["TracksFromGenParticles"],
                                                OutputMCRecoTrackParticleAssociation=["TracksFromGenParticlesAssociation"],
                                                ExtrapolateToECal=True,
                                                OnlyCaloReachingParticles=True,
                                                OutputLevel=INFO)

############### dNdx from tracks
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

############### Optical calo digitization
from Configurables import CreateOpticalCaloCells


def optical_digi(name, optical, truth, out, link, calib, mask=False):
    return CreateOpticalCaloCells(
        name,
        OpticalHits=optical,
        TruthHits=truth,
        OutputCollection=out,
        OutputLinks=link,
        calibrationConstant=calib,
        maskCherenkovForTruthLink=mask,
        OutputLevel=INFO,
    )


# ECAL crystals: scint & Cherenkov share one deposit -> mask cherenkov in the link
ecalDigis = [
    optical_digi("createEcalScintCells", "SCEPCal_MainScounts", "SCEPCal_MainEdep",
                 "SCEPCal_digi_scint", "SCEPCal_scint_link", 1.0 / 1965.0, mask=True),
    optical_digi("createEcalCherenCells", "SCEPCal_MainCcounts", "SCEPCal_MainEdep",
                 "SCEPCal_digi_cheren", "SCEPCal_cheren_link", 1.0 / 97.75, mask=True),
]

# HCAL tubes: scint & Cherenkov are distinct cells -> full-cellID link (default)
hcalDigis = [
    optical_digi("createHcalBarrelScintCells", "DRBTScin", "DRTubeEdep",
                 "DRBTScin_digi", "DRBTScin_link", 1.0 / 206.25),
    optical_digi("createHcalBarrelCherenCells", "DRBTCher", "DRTubeEdep",
                 "DRBTCher_digi", "DRBTCher_link", 1.0 / 68.25),
]
if not CI:  # DR endcap exists only in the full geometry
    hcalDigis += [
        optical_digi("createHcalEndcapRScintCells", "DRETScinRight", "DRTubeEdep",
                     "DRETScinRight_digi", "DRETScinRight_link", 1.0 / 206.25),
        optical_digi("createHcalEndcapRCherenCells", "DRETCherRight", "DRTubeEdep",
                     "DRETCherRight_digi", "DRETCherRight_link", 1.0 / 68.25),
        optical_digi("createHcalEndcapLScintCells", "DRETScinLeft", "DRTubeEdep",
                     "DRETScinLeft_digi", "DRETScinLeft_link", 1.0 / 206.25),
        optical_digi("createHcalEndcapLCherenCells", "DRETCherLeft", "DRTubeEdep",
                     "DRETCherLeft_digi", "DRETCherLeft_link", 1.0 / 68.25),
    ]

############### Seed -> merge -> grow clustering (SCEPCal)
from Configurables import (
    CaloDrivenClusterSeeding,
    TrackDrivenClusterSeeding,
    ClusterSeedMerging,
    ClusterSeedGrower,
)

caloDrivenClusterSeed = CaloDrivenClusterSeeding(
    "CaloDrivenClusterSeed",
    InputCaloHitCollections=["SCEPCal_digi_scint"],
    OutputSeedsA="CaloDrivenSeedsA",
    OutputSeedsB="CaloDrivenSeedsB",
    ReadoutName="SCEPCal_Main",
    FieldStringsToFilter=["depth"],
    FieldValuesToFilter=[0],
    SeedEnergyThresholdA=0.04,
    SeedEnergyThresholdB=0.02,
    MinAboveThresholdNeighbours=2,
    VonNeumannDistance=2,
    OutputLevel=INFO,
)

trackDrivenClusterSeed = TrackDrivenClusterSeeding(
    "TrackDrivenClusterSeed",
    InputTrackCollection="TracksFromGenParticles",
    InputCaloHitCollections=["SCEPCal_digi_scint"],
    OutputSeedsC="TrackDrivenSeedsC",
    ReadoutName="SCEPCal_Main",
    FieldStringsToFilter=["depth"],
    FieldValuesToFilter=[0],
    SeedEnergyThreshold=0.02,
    TrackWindow=0.05,
    OutputLevel=INFO,
)

clusterSeedMerge = ClusterSeedMerging(
    "ClusterSeedMerge",
    CaloDrivenSeeds=["CaloDrivenSeedsA", "CaloDrivenSeedsB"],
    TrackDrivenSeeds=["TrackDrivenSeedsC"],
    OutputMergedSeeds="MergedSeeds",
    MergeDistance=45.0,
    W0=4.6,
    OutputLevel=INFO,
)

topoClusterGrower = ClusterSeedGrower(
    "TopoClusterGrower",
    InputSeeds=["MergedSeeds"],
    InputHits=["SCEPCal_digi_cheren", "SCEPCal_digi_scint"],
    OutputClusters="TopoGrownClusters",
    ReadoutName="SCEPCal_Main",
    FieldStringsToFilter=[],
    FieldValuesToFilter=[],
    FieldStringsToInclude=[],
    FieldValuesToInclude=[],
    GrowThreshold=0.0,
    HardThreshold=0.0,
    UnseededThreshold=0.02,
    W0=4.6,
    VNDistSeeded=2,
    VNDistUnseeded=2,
    MinUnseededHits=2,
    MaxOpeningAngle=0.3,
    AttachIsolatedHits=False,
    OutputLevel=INFO,
)

############### Truth links
from Configurables import CreateTruthLinks

createTruthLinksECAL = CreateTruthLinks(
    "CreateTruthLinksECAL",
    cell_hit_links=["SCEPCal_scint_link"],
    clusters=["TopoGrownClusters"],
    mcparticles="MCParticles",
    cell_mcparticle_links="SCEPCal_CaloHitMCParticleLinks",
    cluster_mcparticle_links="EcalClusterMCParticleLinks",
    OutputLevel=INFO,
)

hcal_links = ["DRBTScin_link", "DRBTCher_link"]
if not CI:
    hcal_links += ["DRETScinRight_link", "DRETCherRight_link",
                   "DRETScinLeft_link", "DRETCherLeft_link"]

createTruthLinksHCAL = CreateTruthLinks(
    "CreateTruthLinksHCAL",
    cell_hit_links=hcal_links,
    clusters=[],
    mcparticles="MCParticles",
    cell_mcparticle_links="DRTube_CaloHitMCParticleLinks",
    cluster_mcparticle_links="empty_ClusterMCParticleLinks",
    OutputLevel=INFO,
)

############### Services + application
from Configurables import UniqueIDGenSvc
from k4FWCore import ApplicationMgr

ApplicationMgr(
    TopAlg=[
        vtxb_digitizer,
        vtxd_digitizer,
        siwrb_digitizer,
        siwrd_digitizer,
        dch_digitizer,
        muon_digitizer,
        tracksFromGenParticles,
        dNdxFromTracks,
    ]
    + ecalDigis
    + hcalDigis
    + [
        caloDrivenClusterSeed,
        trackDrivenClusterSeed,
        clusterSeedMerge,
        topoClusterGrower,
        createTruthLinksECAL,
        createTruthLinksHCAL,
    ],
    EvtSel="NONE",
    EvtMax=-1,
    ExtSvc=[EventDataSvc("EventDataSvc"), geoservice, UniqueIDGenSvc("uidSvc")],
    StopOnSignal=True,
)
