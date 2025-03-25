# run_digi_reco.py
# steering file for the ALLEGRO digitisation/reconstruction

#
# COMMON IMPORTS
#

# Logger
from Gaudi.Configuration import INFO, DEBUG  # , VERBOSE
# units and physical constants
from GaudiKernel.PhysicalConstants import pi

#
# SETTINGS
#

# - default settings, that can be overridden via CLI
inputfile = "ALLEGRO_sim.root"             # input file produced with ddsim - can be overridden with IOSvc.Input
outputfile = "ALLEGRO_sim_digi_reco.root"  # output file produced by this steering file - can be overridden with IOSvc.Output
Nevts = -1                                 # -1 means all events in input file (can be overridden with -n or --num-events option of k4run

# - general settings not set via CLI
filterNoiseThreshold = -1                  # if addNoise is true, and filterNoiseThreshold is >0, will filter away cells with abs(energy) below filterNoiseThreshold * expected sigma(noise)
# dataFolder = "data/"                     # directory containing the calibration files
dataFolder = "./"                          # directory containing the calibration files

# - general settings set via CLI
from k4FWCore.parseArgs import parser
parser.add_argument("--pandora", action="store_true", help="Run pandora PFA", default=False)
parser.add_argument("--includeHCal", action="store_true", help="Also digitise HCal hits and create ECAL+HCAL clusters", default=False)
parser.add_argument("--includeMuon", action="store_true", help="Also digitise muon hits", default=False)
parser.add_argument("--saveHits", action="store_true", help="Save G4 hits", default=False)
parser.add_argument("--saveCells", action="store_true", help="Save cell collection", default=False)
parser.add_argument("--addNoise", action="store_true", help="Add noise to cells (ECAL barrel only)", default=False)
parser.add_argument("--addCrosstalk", action="store_true", help="Add cross-talk to cells (ECAL barrel only)", default=False)
parser.add_argument("--addTracks", action="store_true", help="Add reco-level tracks (smeared truth tracks)", default=False)
parser.add_argument("--calibrateClusters", action="store_true", help="Apply MVA calibration to clusters", default=False)
parser.add_argument("--runPhotonID", action="store_true", help="Apply photon ID tool to clusters", default=False)
parser.add_argument("--pfaOutputFile", help="Output file name", default="")
parser.add_argument("--trkdigi", action="store_true", help="Digitise tracker hits", default=False)

opts = parser.parse_known_args()[0]
runPandora = opts.pandora                 # if true, add tracks, include HCal and Muon, and run pandora PFA instead of basic clustering algorithm
runHCal = opts.includeHCal                # if false, it will produce only ECAL clusters. if true, it will also produce ECAL+HCAL clusters
runMuon = opts.includeMuon                # if false, it will not digitise muon hits
addNoise = opts.addNoise                  # add noise or not to the cell energy
addCrosstalk = opts.addCrosstalk          # switch on/off the crosstalk
addTracks = opts.addTracks                # add tracks or not
digitiseTrackerHits = opts.trkdigi        # digitise tracker hits (smear truth)

# - what to save in output file
#
# always drop uncalibrated cells, except for tests and debugging
dropUncalibratedCells = True
# dropUncalibratedCells = False

# for big productions, save significant space removing hits and cells
# however, hits and cluster cells might be wanted for small productions for detailed event displays
# cluster cells are not needed for the training of the MVA energy regression nor the photon ID since needed quantities are stored in cluster shapeParameters
saveHits = opts.saveHits
saveCells = opts.saveCells
# saveHits = False
# saveCells = False
saveClusterCells = True

dropLumiCalHits = True
# dropVertexHits = True
# dropDCHHits = True
# dropSiWrHits = True
# dropMuonHits = True
dropVertexHits = False
dropDCHHits = False
dropSiWrHits = False
dropMuonHits = False


# ECAL barrel parameters for digitisation
ecalBarrelLayers = 11
ecalBarrelSamplingFraction = [0.3800493723322256] * 1 + [0.13494147915064658] * 1 + [0.142866851721152] * 1 + [0.14839315921940666] * 1 + [0.15298362570665006] * 1 + [0.15709704561942747] * 1 + [0.16063717490147533] * 1 + [0.1641723795419055] * 1 + [0.16845490287689746] * 1 + [0.17111520115997653] * 1 + [0.1730605163148862] * 1
ecalBarrelUpstreamParameters = [[0.028158491043365624, -1.564259408365951, -76.52312805346982, 0.7442903558010191, -34.894692961350195, -74.19340877431723]]
ecalBarrelDownstreamParameters = [[0.00010587711361028165, 0.0052371999097777355, 0.69906696456064, -0.9348243433360095, -0.0364714212117143, 8.360401126995626]]
if ecalBarrelSamplingFraction and len(ecalBarrelSamplingFraction) > 0:
    assert (ecalBarrelLayers == len(ecalBarrelSamplingFraction))
# ECAL endcap parameters for digitisation
ecalEndcapLayers = 98
ecalEndcapSamplingFraction = [0.0390585] * 1+ [0.463715] * 1+ [0.0853304] * 1+ [1] * 1+ [0.0442381] * 1+ [0.0552701] * 1+ [0.245704] * 1+ [0.137059] * 1+ [0.238013] * 1+ [0.147364] * 1+ [0.0788765] * 1+ [0.219239] * 1+ [0.151537] * 1+ [0.26711] * 1+ [0.0853741] * 1+ [0.0995584] * 1+ [0.206757] * 1+ [0.16663] * 1+ [0.238659] * 1+ [0.0978915] * 1+ [0.121322] * 1+ [0.204324] * 1+ [0.175887] * 1+ [0.244135] * 1+ [0.0994313] * 1+ [0.141767] * 1+ [0.205447] * 1+ [0.186003] * 1+ [0.237895] * 1+ [0.108545] * 1+ [0.16853] * 1+ [0.205409] * 1+ [0.195066] * 1+ [0.234766] * 1+ [0.109689] * 1+ [0.152743] * 1+ [0.202067] * 1+ [0.199587] * 1+ [0.22892] * 1+ [0.117163] * 1+ [0.247339] * 1+ [0.219485] * 1+ [0.217142] * 1+ [0.248389] * 1+ [0.125487] * 1+ [0.10275] * 1+ [0.185187] * 1+ [0.18939] * 1+ [0.171225] * 1+ [0.109632] * 1+ [0.159225] * 1+ [0.172072] * 1+ [0.174928] * 1+ [0.180492] * 1+ [0.184174] * 1+ [0.18843] * 1+ [0.191688] * 1+ [0.194472] * 1+ [0.198021] * 1+ [0.200064] * 1+ [0.20313] * 1+ [0.203984] * 1+ [0.208658] * 1+ [0.198391] * 1+ [0.153334] * 1+ [0.175712] * 1+ [0.169342] * 1+ [0.176852] * 1+ [0.175731] * 1+ [0.181481] * 1+ [0.17978] * 1+ [0.18426] * 1+ [0.185028] * 1+ [0.186753] * 1+ [0.190321] * 1+ [0.189175] * 1+ [0.193018] * 1+ [0.193594] * 1+ [0.195598] * 1+ [0.1969] * 1+ [0.197713] * 1+ [0.201379] * 1+ [0.193965] * 1+ [0.223362] * 1+ [0.166243] * 1+ [0.373141] * 1+ [0.112825] * 1+ [0.469126] * 1+ [1] * 1+ [0.0954407] * 1+ [0.0706573] * 1+ [1] * 1+ [1] * 1+ [0.112354] * 1+ [1] * 1+ [1] * 1+ [1] * 1+ [1] * 1
if ecalEndcapSamplingFraction and len(ecalEndcapSamplingFraction) > 0:
    assert (ecalEndcapLayers == len(ecalEndcapSamplingFraction))

resegmentECalBarrel = False

# - parameters for clustering (could also be made configurable via CLI)
doSWClustering = True
doTopoClustering = True

# cluster energy corrections
# simple parametrisations of up/downstream losses for ECAL-only clusters
# not to be applied for ECAL+HCAL clustering
# superseded by MVA calibration, but can be turned on here for the purpose of testing that the code is not broken - will end up in separate cluster collection
applyUpDownstreamCorrections = False

# BDT regression from total cluster energy and fraction of energy in each layer (after correction for sampling fraction)
# not to be applied (yet) for ECAL+HCAL clustering (MVA trained only on ECAL so far)
# applyMVAClusterEnergyCalibration = True
applyMVAClusterEnergyCalibration = opts.calibrateClusters

# calculate cluster energy and barycenter per layer and save it as extra parameters
addShapeParameters = True
ecalBarrelThetaWeights = [-1, 3.0, 3.0, 3.0, 4.25, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0]  # to be recalculated for V03, separately for topo and calo clusters...

# run photon ID algorithm
# not run by default in production, but to be turned on here for the purpose of testing that the code is not broken
# currently off till we provide the onnx files
# runPhotonIDTool = False
runPhotonIDTool = opts.runPhotonID
logEWeightInPhotonID = False

if runPandora:
    print("PandoraPFA is requested, will set addTracks, runHCal and runMuon to True, doSWClustering and doTopoClustering to False")
    runHCal = True
    runMuon = True
    addTracks = True
    doSWClustering = False
    doTopoClustering = False


#
# ALGORITHMS AND SERVICES SETUP
#
TopAlg = []  # alg sequence
ExtSvc = []  # list of external services


# Event counter
from Configurables import EventCounter
eventCounter = EventCounter("EventCounter",
                            OutputLevel=INFO,
                            Frequency=10)
TopAlg += [eventCounter]
# add a message sink service if you want a summary table at the end (not needed..)
# ExtSvc += ["Gaudi::Monitoring::MessageSvcSink"]

# CPU information
from Configurables import AuditorSvc, ChronoAuditor
chra = ChronoAuditor()
audsvc = AuditorSvc()
audsvc.Auditors = [chra]
ExtSvc += [audsvc]


# Detector geometry
# prefix all xmls with path_to_detector
# if K4GEO is empty, this should use relative path to working directory
from Configurables import GeoSvc
import os
geoservice = GeoSvc("GeoSvc")
path_to_detector = os.environ.get("K4GEO", "")
detectors_to_use = [
    'FCCee/ALLEGRO/compact/ALLEGRO_o1_v03/ALLEGRO_o1_v03.xml'
]
geoservice.detectors = [
    os.path.join(path_to_detector, _det) for _det in detectors_to_use
]
geoservice.OutputLevel = INFO
ExtSvc += [geoservice]


# Input/Output handling
from k4FWCore import IOSvc
from Configurables import EventDataSvc
io_svc = IOSvc("IOSvc")
io_svc.Input = inputfile
io_svc.Output = outputfile
evtsvc = EventDataSvc("EventDataSvc")
ExtSvc += [evtsvc]

if addTracks or digitiseTrackerHits:
    ExtSvc += ["RndmGenSvc"]


# Tracking
# Create tracks from gen particles
if addTracks:
    from Configurables import TracksFromGenParticles
    tracksFromGenParticles = TracksFromGenParticles("CreateTracksFromGenParticles",
                                                    InputGenParticles=["MCParticles"],
                                                    InputSimTrackerHits=["VertexBarrelCollection",
                                                                         "VertexEndcapCollection",
                                                                         "DCHCollection",
                                                                         "SiWrBCollection",
                                                                         "SiWrDCollection"],
                                                    OutputTracks=["TracksFromGenParticles"],
                                                    OutputMCRecoTrackParticleAssociation=["TracksFromGenParticlesAssociation"],
                                                    ExtrapolateToECal=True,
                                                    KeepOnlyBestExtrapolation=False,
                                                    TrackerIDs=[1,2,3,23,24],  # from DectDimensions.xml
                                                    OutputLevel=INFO)
    TopAlg += [tracksFromGenParticles]


# Tracker digitisation
if digitiseTrackerHits:
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
                                  xResolution = [innerVertexResolution_x, innerVertexResolution_x, innerVertexResolution_x,
                                                 outerVertexResolution_x, outerVertexResolution_x], # mm, r-phi direction
                                  yResolution = [innerVertexResolution_y, innerVertexResolution_y, innerVertexResolution_y,
                                                 outerVertexResolution_y, outerVertexResolution_y], # mm, z direction
                                  tResolution = [innerVertexResolution_t, innerVertexResolution_t, innerVertexResolution_t,
                                                 outerVertexResolution_t, outerVertexResolution_t],
                                  forceHitsOntoSurface = False,
                                  OutputLevel = INFO
                                  )
    TopAlg += [vtxb_digitizer]

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
    TopAlg += [vtxd_digitizer]

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
    TopAlg += [siwrb_digitizer]

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
    TopAlg += [siwrd_digitizer]

    from Configurables import UniqueIDGenSvc
    ExtSvc += [UniqueIDGenSvc("uidSvc")]
    from Configurables import DCHdigi_v01
    # "https://fccsw.web.cern.ch/fccsw/filesFoSimDigiReco/IDEA/DataAlgFORGEANT.root"
    dch_digitizer = DCHdigi_v01("DCHdigi",
                                DCH_simhits = ["DCHCollection"],
                                DCH_name = "DCH_v2",
                                fileDataAlg = dataFolder + "DataAlgFORGEANT.root",
                                calculate_dndx = False, # cluster counting disabled (to be validated, see FCC-config#239)
                                create_debug_histograms = False,
                                # zResolution_mm = 30., # in mm - Note: At this point, the z resolution comes without the stereo measurement
                                # xyResolution_mm = 0.1 # in mm
                                # no smearing
                                zResolution_mm = 0., # in mm - Note: At this point, the z resolution comes without the stereo measurement
                                xyResolution_mm = 0. # in mm
                                )
    TopAlg += [dch_digitizer]


# Calorimeter digitisation (merging hits into cells, EM scale calibration via sampling fractions)

# - ECAL readouts
ecalBarrelReadoutName = "ECalBarrelModuleThetaMerged"      # barrel, original segmentation (baseline)
ecalBarrelReadoutName2 = "ECalBarrelModuleThetaMerged2"    # barrel, after re-segmentation (for optimisation studies)
ecalEndcapReadoutName = "ECalEndcapTurbine"                # endcap, turbine-like (baseline)
# - HCAL readouts
if runHCal:
    hcalBarrelReadoutName = "HCalBarrelReadout"            # barrel, original segmentation (phi-theta)
    # hcalBarrelReadoutName = "HCalBarrelReadoutPhiRow"    # barrel, alternative segmentation (phi-row)
    hcalEndcapReadoutName = "HCalEndcapReadout"            # endcap, original segmentation
else:
    hcalBarrelReadoutName = ""
    hcalEndcapReadoutName = ""

# - EM scale calibration (sampling fraction)
from Configurables import CalibrateInLayersTool
#   * ECAL barrel
calibEcalBarrel = CalibrateInLayersTool("CalibrateECalBarrel",
                                        samplingFraction=ecalBarrelSamplingFraction,
                                        readoutName=ecalBarrelReadoutName,
                                        layerFieldName="layer")
#   * ECAL endcap
calibEcalEndcap = CalibrateInLayersTool("CalibrateECalEndcap",
                                        samplingFraction=ecalEndcapSamplingFraction,
                                        readoutName=ecalEndcapReadoutName,
                                        layerFieldName="layer")

if runHCal:
    from Configurables import CalibrateCaloHitsTool
    # HCAL barrel
    calibHCalBarrel = CalibrateCaloHitsTool(
        "CalibrateHCalBarrel", invSamplingFraction="29.4202")
    # HCAL endcap
    calibHCalEndcap = CalibrateCaloHitsTool(
        "CalibrateHCalEndcap", invSamplingFraction="29.4202")  # FIXME: to be updated for ddsim

# - cell positioning tools
from Configurables import CellPositionsECalBarrelModuleThetaSegTool
cellPositionEcalBarrelTool = CellPositionsECalBarrelModuleThetaSegTool(
    "CellPositionsECalBarrel",
    readoutName=ecalBarrelReadoutName,
    OutputLevel=INFO
)
# the noise tool needs the positioning tool, but if I reuse the previous one the code crashes..
cellPositionEcalBarrelToolForNoise = CellPositionsECalBarrelModuleThetaSegTool(
    "CellPositionsECalBarrelForNoise",
    readoutName=ecalBarrelReadoutName,
    OutputLevel=INFO
)
if resegmentECalBarrel:
    cellPositionEcalBarrelTool2 = CellPositionsECalBarrelModuleThetaSegTool(
        "CellPositionsECalBarrel2",
        readoutName=ecalBarrelReadoutName2,
        OutputLevel=INFO
    )

from Configurables import CellPositionsECalEndcapTurbineSegTool
cellPositionEcalEndcapTool = CellPositionsECalEndcapTurbineSegTool(
    "CellPositionsECalEndcap",
    readoutName=ecalEndcapReadoutName,
    OutputLevel=INFO
)

if runHCal:
    from Configurables import CellPositionsHCalPhiThetaSegTool
    cellPositionHCalBarrelTool = CellPositionsHCalPhiThetaSegTool(
        "CellPositionsHCalBarrel",
        readoutName=hcalBarrelReadoutName,
        detectorName="HCalBarrel",
        OutputLevel=INFO
    )
    cellPositionHCalEndcapTool = CellPositionsHCalPhiThetaSegTool(
        "CellPositionsHCalEndcap",
        readoutName=hcalEndcapReadoutName,
        detectorName="HCalThreePartsEndcap",
        numLayersHCalThreeParts=[6, 9, 22],
        OutputLevel=INFO
    )

# - crosstalk tool
if addCrosstalk:
    from Configurables import ReadCaloCrosstalkMap
    # read the crosstalk map
    readCrosstalkMap = ReadCaloCrosstalkMap("ReadCrosstalkMap",
                                            fileName="https://fccsw.web.cern.ch/fccsw/filesForSimDigiReco/ALLEGRO/ALLEGRO_o1_v03/xtalk_neighbours_map_ecalB_thetamodulemerged.root",
                                            OutputLevel=INFO)
else:
    readCrosstalkMap = None

# - noise tool
if addNoise:
    ecalBarrelNoisePath = "elecNoise_ecalBarrelFCCee_theta.root"
    ecalBarrelNoiseRMSHistName = "h_elecNoise_fcc_"
    from Configurables import NoiseCaloCellsVsThetaFromFileTool
    ecalBarrelNoiseTool = NoiseCaloCellsVsThetaFromFileTool("ecalBarrelNoiseTool",
                                                            cellPositionsTool=cellPositionEcalBarrelToolForNoise,
                                                            readoutName=ecalBarrelReadoutName,
                                                            noiseFileName=ecalBarrelNoisePath,
                                                            elecNoiseRMSHistoName=ecalBarrelNoiseRMSHistName,
                                                            setNoiseOffset=False,
                                                            activeFieldName="layer",
                                                            addPileup=False,
                                                            filterNoiseThreshold=filterNoiseThreshold,
                                                            useAbsInFilter=True,
                                                            numRadialLayers=ecalBarrelLayers,
                                                            scaleFactor=1 / 1000.,  # MeV to GeV
                                                            OutputLevel=INFO)

    from Configurables import TubeLayerModuleThetaCaloTool
    ecalBarrelGeometryTool = TubeLayerModuleThetaCaloTool("ecalBarrelGeometryTool",
                                                          readoutName=ecalBarrelReadoutName,
                                                          activeVolumeName="LAr_sensitive",
                                                          activeFieldName="layer",
                                                          activeVolumesNumber=ecalBarrelLayers,
                                                          fieldNames=["system"],
                                                          fieldValues=[4],
                                                          OutputLevel=INFO)
else:
    ecalBarrelNoiseTool = None
    ecalBarrelGeometryTool = None

# Create cells in ECal barrel (calibrated and positioned - optionally with xtalk and noise added)
# from uncalibrated cells (+cellID info) from ddsim
ecalBarrelPositionedCellsName = ecalBarrelReadoutName + "Positioned"
ecalBarrelLinks = ecalBarrelPositionedCellsName + "SimCaloHitLinks"
from Configurables import CreatePositionedCaloCells
createEcalBarrelCells = CreatePositionedCaloCells("CreatePositionedECalBarrelCells",
                                                  doCellCalibration=True,
                                                  calibTool=calibEcalBarrel,
                                                  positionsTool=cellPositionEcalBarrelTool,
                                                  addCrosstalk=addCrosstalk,
                                                  crosstalkTool=readCrosstalkMap,
                                                  addCellNoise=False,
                                                  filterCellNoise=False,
                                                  noiseTool=None,
                                                  geometryTool=ecalBarrelGeometryTool,
                                                  OutputLevel=INFO,
                                                  hits=ecalBarrelReadoutName,
                                                  cells=ecalBarrelPositionedCellsName,
                                                  links=ecalBarrelLinks
                                                  )
TopAlg += [createEcalBarrelCells]

# -  now, if we want to also save cells with coarser granularity:
if resegmentECalBarrel:
    # rewrite the cellId using the merged theta-module segmentation
    # (merging several modules and severla theta readout cells).
    # Add noise at this step if you derived the noise already assuming merged cells
    # Step a: compute new cellID of cells based on new readout
    # (merged module-theta segmentation with variable merging vs layer)
    from Configurables import RedoSegmentation
    resegmentEcalBarrelTool = RedoSegmentation("ReSegmentationEcal",
                                               # old bitfield (readout)
                                               oldReadoutName=ecalBarrelReadoutName,
                                               # specify which fields are going to be altered (deleted/rewritten)
                                               oldSegmentationIds=["module", "theta"],
                                               # new bitfield (readout), with new segmentation (merged modules and theta cells)
                                               newReadoutName=ecalBarrelReadoutName2,
                                               OutputLevel=INFO,
                                               debugPrint=200,
                                               inhits=ecalBarrelPositionedCellsName,
                                               outhits="ECalBarrelCellsMerged")

    # Step b: merge new cells with same cellID together
    # do not apply cell calibration again since cells were already
    # calibrated in Step 1
    # noise and xtalk off assuming they were applied earlier
    ecalBarrelPositionedCellsName2 = ecalBarrelReadoutName2 + "Positioned"
    ecalBarrelLinks2 = ecalBarrelPositionedCellsName2 + "SimCaloHitLinks"
    createEcalBarrelCells2 = CreatePositionedCaloCells("CreatePositionedECalBarrelCells2",
                                                       doCellCalibration=False,
                                                       positionsTool=cellPositionEcalBarrelTool2,
                                                       calibTool=None,
                                                       crosstalkTool=None,
                                                       addCrosstalk=False,
                                                       addCellNoise=False,
                                                       filterCellNoise=False,
                                                       OutputLevel=INFO,
                                                       hits="ECalBarrelCellsMerged",
                                                       cells=ecalBarrelPositionedCellsName2,
                                                       links=ecalBarrelLinks2)
    TopAlg += [
        resegmentEcalBarrelTool,
        createEcalBarrelCells2,
    ]

# Create cells in ECal endcap (needed if one wants to apply cell calibration,
# which is not performed by ddsim)
ecalEndcapPositionedCellsName = ecalEndcapReadoutName + "Positioned"
ecalEndcapLinks = ecalEndcapPositionedCellsName + "SimCaloHitLinks"
createEcalEndcapCells = CreatePositionedCaloCells("CreatePositionedECalEndcapCells",
                                                  doCellCalibration=True,
                                                  positionsTool=cellPositionEcalEndcapTool,
                                                  calibTool=calibEcalEndcap,
                                                  crosstalkTool=None,
                                                  addCrosstalk=False,
                                                  addCellNoise=False,
                                                  filterCellNoise=False,
                                                  OutputLevel=INFO,
                                                  hits=ecalEndcapReadoutName,
                                                  cells=ecalEndcapPositionedCellsName,
                                                  links=ecalEndcapLinks)
TopAlg += [createEcalEndcapCells]

if addNoise:
    # cells with noise not filtered
    ecalBarrelCellsNoiseLinks = ecalBarrelPositionedCellsName + "WithNoise" + "SimCaloHitLinks"
    createEcalBarrelCellsNoise = CreatePositionedCaloCells("CreatePositionedECalBarrelCellsWithNoise",
                                                           doCellCalibration=True,
                                                           calibTool=calibEcalBarrel,
                                                           positionsTool=cellPositionEcalBarrelTool,
                                                           addCrosstalk=addCrosstalk,
                                                           crosstalkTool=readCrosstalkMap,
                                                           addCellNoise=True,
                                                           filterCellNoise=False,
                                                           noiseTool=ecalBarrelNoiseTool,
                                                           geometryTool=ecalBarrelGeometryTool,
                                                           OutputLevel=INFO,
                                                           hits=ecalBarrelReadoutName,
                                                           cells=ecalBarrelPositionedCellsName + "WithNoise",
                                                           links=ecalBarrelCellsNoiseLinks)
    TopAlg += [createEcalBarrelCellsNoise]

    # cells with noise filtered
    ecalBarrelCellsNoiseFilteredLinks = ecalBarrelPositionedCellsName + "WithNoiseFiltered" + "SimCaloHitLinks"
    createEcalBarrelCellsNoiseFiltered = CreatePositionedCaloCells("CreatePositionedECalBarrelCellsWithNoiseFiltered",
                                                                   doCellCalibration=True,
                                                                   calibTool=calibEcalBarrel,
                                                                   positionsTool=cellPositionEcalBarrelTool,
                                                                   addCrosstalk=addCrosstalk,
                                                                   crosstalkTool=readCrosstalkMap,
                                                                   addCellNoise=True,
                                                                   filterCellNoise=True,
                                                                   noiseTool=ecalBarrelNoiseTool,
                                                                   geometryTool=ecalBarrelGeometryTool,
                                                                   OutputLevel=INFO,
                                                                   hits=ecalBarrelReadoutName,  # uncalibrated & unpositioned cells without noise
                                                                   cells=ecalBarrelPositionedCellsName + "WithNoiseFiltered",
                                                                   links=ecalBarrelCellsNoiseFilteredLinks
                                                                   )
    TopAlg += [createEcalBarrelCellsNoiseFiltered]

if runHCal:
    # Apply calibration and positioning to cells in HCal barrel
    hcalBarrelPositionedCellsName = hcalBarrelReadoutName + "Positioned"
    hcalBarrelLinks = hcalBarrelPositionedCellsName + "SimCaloHitLinks"
    createHCalBarrelCells = CreatePositionedCaloCells("CreatePositionedHCalBarrelCells",
                                                      doCellCalibration=True,
                                                      calibTool=calibHCalBarrel,
                                                      positionsTool=cellPositionHCalBarrelTool,
                                                      addCellNoise=False,
                                                      filterCellNoise=False,
                                                      hits=hcalBarrelReadoutName,
                                                      cells=hcalBarrelPositionedCellsName,
                                                      links=hcalBarrelLinks,
                                                      OutputLevel=INFO)
    TopAlg += [createHCalBarrelCells]

    # Apply calibration and positioning to cells in HCal endcap
    hcalEndcapPositionedCellsName = hcalEndcapReadoutName + "Positioned"
    hcalEndcapLinks = hcalEndcapPositionedCellsName + "SimCaloHitLinks"
    createHCalEndcapCells = CreatePositionedCaloCells("CreatePositionedHCalEndcapCells",
                                                      doCellCalibration=True,
                                                      calibTool=calibHCalEndcap,
                                                      addCellNoise=False,
                                                      filterCellNoise=False,
                                                      positionsTool=cellPositionHCalEndcapTool,
                                                      OutputLevel=INFO,
                                                      hits=hcalEndcapReadoutName,
                                                      cells=hcalEndcapPositionedCellsName,
                                                      links=hcalEndcapLinks)
    TopAlg += [createHCalEndcapCells]

else:
    hcalBarrelPositionedCellsName = "emptyCaloCells"
    hcalEndcapPositionedCellsName = "emptyCaloCells"
    hcalBarrelLinks = ""
    hcalEndcapLinks = ""
    cellPositionHCalBarrelTool = None
    cellPositionHCalEndcapTool = None

# Empty cells for parts of calorimeter not implemented yet
if doSWClustering or doTopoClustering:
    from Configurables import CreateEmptyCaloCellsCollection
    createemptycells = CreateEmptyCaloCellsCollection("CreateEmptyCaloCells")
    createemptycells.cells.Path = "emptyCaloCells"
    TopAlg += [createemptycells]


# Muon cells [add longitudinal segmentation to detector?]
if runMuon:
    from Configurables import CellPositionsSimpleCylinderPhiThetaSegTool
    muonBarrelReadoutName = "MuonTaggerBarrelPhiTheta"
    muonBarrelPositionedCellsName = muonBarrelReadoutName + "Positioned"
    muonBarrelLinks = muonBarrelPositionedCellsName + "SimCaloHitLinks"
    cellPositionMuonBarrelTool = CellPositionsSimpleCylinderPhiThetaSegTool(
        "CellPositionsMuonBarrel",
        detectorName="MuonTaggerBarrel",
        readoutName=muonBarrelReadoutName,
        OutputLevel=INFO
    )

    from Configurables import NoiseCaloCellsFlatTool
    MuonBarrelNoiseTool = NoiseCaloCellsFlatTool("MuonBarrelNoiseTool",
                                                 cellNoiseRMS=0.0005,  # in GeV
                                                 filterNoiseThreshold=3,
                                                 OutputLevel=INFO)
    createMuonBarrelCells = CreatePositionedCaloCells("CreatePositionedMuonBarrelCells",
                                                      positionsTool=cellPositionMuonBarrelTool,
                                                      doCellCalibration=False,
                                                      # calibTool=None,
                                                      addCrosstalk=False,
                                                      # crosstalkTool=None
                                                      addCellNoise=False,
                                                      # filterCellNoise=False,
                                                      # noiseTool=None,
                                                      filterCellNoise=True,
                                                      noiseTool=MuonBarrelNoiseTool,
                                                      geometryTool=None,
                                                      OutputLevel=INFO,
                                                      hits=muonBarrelReadoutName,
                                                      cells=muonBarrelPositionedCellsName,
                                                      links=muonBarrelLinks
                                                      )
    TopAlg += [createMuonBarrelCells]

    muonEndcapReadoutName = "MuonTaggerEndcapPhiTheta"
    muonEndcapPositionedCellsName = muonEndcapReadoutName + "Positioned"
    muonEndcapLinks = muonEndcapPositionedCellsName + "SimCaloHitLinks"
    cellPositionMuonEndcapTool = CellPositionsSimpleCylinderPhiThetaSegTool(
        "CellPositionsMuonEndcap",
        detectorName="MuonTaggerEndcap",
        readoutName=muonEndcapReadoutName,
        OutputLevel=INFO
    )
    createMuonEndcapCells = CreatePositionedCaloCells("CreatePositionedMuonEndcapCells",
                                                      positionsTool=cellPositionMuonEndcapTool,
                                                      doCellCalibration=False,
                                                      # calibTool=None,
                                                      addCrosstalk=False,
                                                      # crosstalkTool=None
                                                      addCellNoise=False,
                                                      filterCellNoise=False,
                                                      noiseTool=None,
                                                      geometryTool=None,
                                                      OutputLevel=INFO,
                                                      hits=muonEndcapReadoutName,
                                                      cells=muonEndcapPositionedCellsName,
                                                      links=muonEndcapLinks
                                                      )
    TopAlg += [createMuonEndcapCells]
else:
    muonBarrelReadoutName = ""
    muonEndcapReadoutName = ""
    muonBarrelPositionedCellsName = ""
    muonEndcapPositionedCellsName = ""
    muonBarrelLinks = ""
    muonEndcapLinks = ""

# Function that sets up the sequence for producing SW clusters given an input cell collection
def setupSWClusters(inputCells,
                    inputReadouts,
                    outputClusters,
                    clusteringThreshold,
                    applyUpDownstreamCorrections,
                    applyMVAClusterEnergyCalibration,
                    addShapeParameters,
                    runPhotonIDTool):

    global TopAlg

    from Configurables import CaloTowerToolFCCee
    from Configurables import CreateCaloClustersSlidingWindowFCCee

    # Clustering parameters
    # - phi-theta window sizes
    windT = 9
    windP = 17
    posT = 5
    posP = 11
    dupT = 7
    dupP = 13
    finT = 9
    finP = 17
    # to be tested: about -2% of energy but smaller cluster, less noise
    # windT = 7
    # windP = 9
    # posT = 5
    # posP = 7
    # dupT = 7
    # dupP = 9
    # finT = 7
    # finP = 9
    # - minimal energy to create a cluster in GeV (FCC-ee detectors have to reconstruct low energy particles)
    threshold = clusteringThreshold

    towerTool = CaloTowerToolFCCee(outputClusters + "TowerTool",
                                   deltaThetaTower=4 * 0.009817477 / 4, deltaPhiTower=2 * 2 * pi / 1536.,
                                   ecalBarrelReadoutName=inputReadouts.get("ecalBarrel", ""),
                                   ecalEndcapReadoutName=inputReadouts.get("ecalEndcap", ""),
                                   ecalFwdReadoutName=inputReadouts.get("ecalFwd", ""),
                                   hcalBarrelReadoutName=inputReadouts.get("hcalBarrel", ""),
                                   hcalExtBarrelReadoutName=inputReadouts.get("hcalExtBarrel", ""),
                                   hcalEndcapReadoutName=inputReadouts.get("hcalEndcap", ""),
                                   hcalFwdReadoutName=inputReadouts.get("hcalFwd", ""),
                                   OutputLevel=INFO)
    towerTool.ecalBarrelCells.Path = inputCells.get("ecalBarrel", "emptyCaloCells")
    towerTool.ecalEndcapCells.Path = inputCells.get("ecalEndcap", "emptyCaloCells")
    towerTool.ecalFwdCells.Path = inputCells.get("ecalFwd", "emptyCaloCells")
    towerTool.hcalBarrelCells.Path = inputCells.get("hcalBarrel", "emptyCaloCells")
    towerTool.hcalExtBarrelCells.Path = inputCells.get("hcalExtBarrel", "emptyCaloCells")
    towerTool.hcalEndcapCells.Path = inputCells.get("hcalEndcap", "emptyCaloCells")
    towerTool.hcalFwdCells.Path = inputCells.get("hcalFwd", "emptyCaloCells")

    clusterAlg = CreateCaloClustersSlidingWindowFCCee("Create" + outputClusters,
                                                      towerTool=towerTool,
                                                      nThetaWindow=windT, nPhiWindow=windP,
                                                      nThetaPosition=posT, nPhiPosition=posP,
                                                      nThetaDuplicates=dupT, nPhiDuplicates=dupP,
                                                      nThetaFinal=finT, nPhiFinal=finP,
                                                      energyThreshold=threshold,
                                                      energySharingCorrection=False,
                                                      attachCells=True,
                                                      OutputLevel=INFO
                                                      )
    clusterAlg.clusters.Path = outputClusters
    clusterAlg.clusterCells.Path = outputClusters.replace("Clusters", "Cluster") + "Cells"
    TopAlg += [clusterAlg]

    if applyUpDownstreamCorrections:
        # note that this only works for ecal barrel given various hardcoded quantities
        # to be generalized, pass more input parameters to function
        from Configurables import CorrectCaloClusters
        correctClusterAlg = CorrectCaloClusters("Correct" + outputClusters,
                                                inClusters=clusterAlg.clusters.Path,
                                                outClusters="Corrected" + clusterAlg.clusters.Path,
                                                systemIDs=[4],
                                                numLayers=[ecalBarrelLayers],
                                                firstLayerIDs=[0],
                                                lastLayerIDs=[ecalBarrelLayers - 1],
                                                readoutNames=[inputReadouts["ecalBarrel"]],
                                                upstreamParameters=ecalBarrelUpstreamParameters,
                                                upstreamFormulas=[['[0]+[1]/(x-[2])', '[0]+[1]/(x-[2])']],
                                                downstreamParameters=ecalBarrelDownstreamParameters,
                                                downstreamFormulas=[['[0]+[1]*x', '[0]+[1]/sqrt(x)', '[0]+[1]/x']],
                                                OutputLevel=INFO
                                                )
        TopAlg += [correctClusterAlg]

    if addShapeParameters:
        # note that this only works for ecal barrel given various hardcoded quantities
        from Configurables import AugmentClustersFCCee
        augmentClusterAlg = AugmentClustersFCCee("Augment" + outputClusters,
                                                 inClusters=clusterAlg.clusters.Path,
                                                 outClusters="Augmented" + clusterAlg.clusters.Path,
                                                 systemIDs=[4],
                                                 systemNames=["EMB"],
                                                 numLayers=[ecalBarrelLayers],
                                                 readoutNames=[inputReadouts["ecalBarrel"]],
                                                 layerFieldNames=["layer"],
                                                 thetaRecalcWeights=[ecalBarrelThetaWeights],
                                                 # do_photon_shapeVar=runPhotonIDTool,
                                                 do_photon_shapeVar=True,  # we want these variables to train the photon ID BDT
                                                 do_widthTheta_logE_weights=logEWeightInPhotonID,
                                                 OutputLevel=INFO
                                                 )
        TopAlg += [augmentClusterAlg]

    if applyMVAClusterEnergyCalibration:
        # note that this only works for ecal barrel given various hardcoded quantities
        inClusters = ""
        if addShapeParameters:
            inClusters = augmentClusterAlg.outClusters.Path
        else:
            inClusters = clusterAlg.clusters.Path

        from Configurables import CalibrateCaloClusters
        calibrateClustersAlg = CalibrateCaloClusters("Calibrate" + outputClusters,
                                                     inClusters=inClusters,
                                                     outClusters="Calibrated" + clusterAlg.clusters.Path,
                                                     systemIDs=[4],
                                                     systemNames=["EMB"],
                                                     numLayers=[ecalBarrelLayers],
                                                     firstLayerIDs=[0],
                                                     readoutNames=[inputReadouts["ecalBarrel"]],
                                                     layerFieldNames=["layer"],
                                                     calibrationFile=dataFolder + "lgbm_calibration-CaloClusters.onnx",
                                                     OutputLevel=INFO
                                                     )
        TopAlg += [calibrateClustersAlg]

    if runPhotonIDTool:
        if not addShapeParameters:
            print("Photon ID tool cannot be run if shower shape parameters are not calculated")
            runPhotonIDTool = False
        else:
            inClusters = ""
            if applyMVAClusterEnergyCalibration:
                inClusters = calibrateClustersAlg.outClusters.Path
            else:
                inClusters = augmentClusterAlg.outClusters.Path

            from Configurables import PhotonIDTool
            photonIDAlg = PhotonIDTool("PhotonID" + outputClusters,
                                       inClusters=inClusters,
                                       outClusters="PhotonID" + inClusters,
                                       mvaModelFile=dataFolder + "bdt-photonid-weights-EMBCaloClusters.onnx",
                                       mvaInputsFile=dataFolder + "bdt-photonid-settings-EMBCaloClusters.json",
                                       OutputLevel=INFO
                                       )
            TopAlg += [photonIDAlg]


# Function that sets up the sequence for producing Topo clusters given an input cell collection
def setupTopoClusters(inputCells,
                      inputReadouts,
                      outputClusters,
                      clusteringThreshold,
                      neighboursMap,
                      noiseMap,
                      applyUpDownstreamCorrections,
                      applyMVAClusterEnergyCalibration,
                      addShapeParameters,
                      runPhotonIDTool):

    global TopAlg

    from Configurables import TopoCaloNeighbours
    from Configurables import TopoCaloNoisyCells
    from Configurables import CaloTopoClusterFCCee

    # Clustering parameters
    seedSigma = 6
    neighbourSigma = 2
    lastNeighbourSigma = 0

    # tool providing the map of cell neighbours
    neighboursTool = TopoCaloNeighbours(outputClusters + "NeighboursMap",
                                        fileName=neighboursMap,
                                        OutputLevel=INFO)

    # tool providing expected noise levels per cell
    noiseTool = TopoCaloNoisyCells(outputClusters + "NoiseMap",
                                   fileName=noiseMap,
                                   OutputLevel=INFO)

    # list of input cells
    cells = list(inputCells.values())
    # EM barrel readout name (if present)
    readoutName = ""
    if ecalBarrelReadoutName in inputReadouts:
        readoutName = ecalBarrelReadoutName

    # algorithm creating the topoclusters
    clusterAlg = CaloTopoClusterFCCee("Create" + outputClusters,
                                      cells=cells,
                                      clusters=outputClusters,
                                      clusterCells=outputClusters.replace("Clusters", "Cluster") + "Cells",
                                      neigboursTool=neighboursTool,
                                      noiseTool=noiseTool,
                                      seedSigma=seedSigma,
                                      neighbourSigma=neighbourSigma,
                                      lastNeighbourSigma=lastNeighbourSigma,
                                      minClusterEnergy=clusteringThreshold,
                                      OutputLevel=INFO)
    TopAlg += [clusterAlg]

    if applyUpDownstreamCorrections:
        # note that this only works for ecal barrel given various hardcoded quantities
        # to be generalized, pass more input parameters to function
        from Configurables import CorrectCaloClusters
        correctClusterAlg = CorrectCaloClusters("Correct" + outputClusters,
                                                inClusters=clusterAlg.clusters.Path,
                                                outClusters="Corrected" + clusterAlg.clusters.Path,
                                                systemIDs=[4],
                                                numLayers=[ecalBarrelLayers],
                                                firstLayerIDs=[0],
                                                lastLayerIDs=[ecalBarrelLayers - 1],
                                                readoutNames=[inputReadouts["ecalBarrel"]],
                                                upstreamParameters=ecalBarrelUpstreamParameters,
                                                upstreamFormulas=[['[0]+[1]/(x-[2])', '[0]+[1]/(x-[2])']],
                                                downstreamParameters=ecalBarrelDownstreamParameters,
                                                downstreamFormulas=[['[0]+[1]*x', '[0]+[1]/sqrt(x)', '[0]+[1]/x']],
                                                OutputLevel=INFO
                                                )
        TopAlg += [correctClusterAlg]

    if addShapeParameters:
        # note that this only works for ecal barrel given various hardcoded quantities
        from Configurables import AugmentClustersFCCee
        augmentClusterAlg = AugmentClustersFCCee("Augment" + outputClusters,
                                                 inClusters=clusterAlg.clusters.Path,
                                                 outClusters="Augmented" + clusterAlg.clusters.Path,
                                                 systemIDs=[4],
                                                 systemNames=["EMB"],
                                                 numLayers=[ecalBarrelLayers],
                                                 readoutNames=[inputReadouts["ecalBarrel"]],
                                                 layerFieldNames=["layer"],
                                                 thetaRecalcWeights=[ecalBarrelThetaWeights],
                                                 # do_photon_shapeVar=runPhotonIDTool,
                                                 do_photon_shapeVar=True,  # we want these variables to train the photon ID BDT
                                                 do_widthTheta_logE_weights=logEWeightInPhotonID,
                                                 OutputLevel=INFO)
        TopAlg += [augmentClusterAlg]

    if applyMVAClusterEnergyCalibration:
        # note that this only works for ecal barrel given various hardcoded quantities
        inClusters = ""
        if addShapeParameters:
            inClusters = "Augmented" + clusterAlg.clusters.Path
        else:
            inClusters = clusterAlg.clusters.Path

        from Configurables import CalibrateCaloClusters
        calibrateClustersAlg = CalibrateCaloClusters("Calibrate" + outputClusters,
                                                     inClusters=inClusters,
                                                     outClusters="Calibrated" + clusterAlg.clusters.Path,
                                                     systemIDs=[4],
                                                     systemNames=["EMB"],
                                                     numLayers=[ecalBarrelLayers],
                                                     firstLayerIDs=[0],
                                                     readoutNames=[inputReadouts["ecalBarrel"]],
                                                     layerFieldNames=["layer"],
                                                     calibrationFile=dataFolder + "lgbm_calibration-CaloTopoClusters.onnx",
                                                     OutputLevel=INFO
                                                     )
        TopAlg += [calibrateClustersAlg]

    if runPhotonIDTool:
        if not addShapeParameters:
            print("Photon ID tool cannot be run if shower shape parameters are not calculated")
            runPhotonIDTool = False
        else:
            inClusters = ""
            if applyMVAClusterEnergyCalibration:
                inClusters = calibrateClustersAlg.outClusters.Path
            else:
                inClusters = augmentClusterAlg.outClusters.Path

            from Configurables import PhotonIDTool
            photonIDAlg = PhotonIDTool("PhotonID" + outputClusters,
                                       inClusters=inClusters,
                                       outClusters="PhotonID" + inClusters,
                                       mvaModelFile=dataFolder + "bdt-photonid-weights-EMBCaloTopoClusters.onnx",
                                       mvaInputsFile=dataFolder + "bdt-photonid-settings-EMBCaloTopoClusters.json",
                                       OutputLevel=INFO)
            TopAlg += [photonIDAlg]


if doSWClustering:
    # SW ECAL barrel clusters
    EMBCaloClusterInputs = {"ecalBarrel": ecalBarrelPositionedCellsName}
    EMBCaloClusterReadouts = {"ecalBarrel": ecalBarrelReadoutName}
    setupSWClusters(EMBCaloClusterInputs,
                    EMBCaloClusterReadouts,
                    "EMBCaloClusters",
                    0.04,
                    applyUpDownstreamCorrections,
                    applyMVAClusterEnergyCalibration,
                    addShapeParameters,
                    runPhotonIDTool)

    # SW ECAL endcap clusters
    EMECCaloClusterInputs = {"ecalEndcap": ecalEndcapPositionedCellsName}
    EMECCaloClusterReadouts = {"ecalEndcap": ecalEndcapReadoutName}
    setupSWClusters(EMECCaloClusterInputs,
                    EMECCaloClusterReadouts,
                    "EMECCaloClusters",
                    0.04,
                    False,
                    False,
                    False,
                    False)

    # SW ECAL barrel clusters with noise
    if addNoise:
        EMBCaloClusterInputsWithNoise = {"ecalBarrel": ecalBarrelPositionedCellsName + "WithNoise" if filterNoiseThreshold < 0 else ecalBarrelPositionedCellsName + "WithNoiseFiltered"}
        setupSWClusters(EMBCaloClusterInputsWithNoise,
                        EMBCaloClusterReadouts,
                        "EMBCaloClustersWithNoise" if filterNoiseThreshold < 0 else "EMBCaloClustersWithNoiseFiltered",
                        0.1,  # large number of clusters with noise, consider raising to 0.3 if not looking at low-energy cluster reconstruction, or use filtered cells
                        applyUpDownstreamCorrections,
                        applyMVAClusterEnergyCalibration,
                        addShapeParameters,
                        runPhotonIDTool)

    # ECAL + HCAL clusters
    if runHCal:
        CaloClusterInputs = {
            "ecalBarrel": ecalBarrelPositionedCellsName,
            "ecalEndcap": ecalEndcapPositionedCellsName,
            "hcalBarrel": hcalBarrelPositionedCellsName,
            "hcalEndcap": hcalEndcapPositionedCellsName,
        }
        CaloClusterReadouts = {
            "ecalBarrel": ecalBarrelReadoutName,
            "ecalEndcap": ecalEndcapReadoutName,
            "hcalBarrel": hcalBarrelReadoutName,
            "hcalEndcap": hcalEndcapReadoutName,
        }
        setupSWClusters(CaloClusterInputs,
                        CaloClusterReadouts,
                        "CaloClusters",
                        0.04,
                        False,
                        False,
                        False,
                        False)

if doTopoClustering:
    # ECAL barrel topoclusters
    EMBCaloTopoClusterInputs = {"ecalBarrel": ecalBarrelPositionedCellsName}
    EMBCaloTopoClusterReadouts = {"ecalBarrel": ecalBarrelReadoutName}
    setupTopoClusters(EMBCaloTopoClusterInputs,
                      EMBCaloTopoClusterReadouts,
                      "EMBCaloTopoClusters",
                      0.0,
                      dataFolder + "neighbours_map_ecalB_thetamodulemerged.root",
                      dataFolder + "cellNoise_map_electronicsNoiseLevel_ecalB_thetamodulemerged.root",
                      applyUpDownstreamCorrections,
                      applyMVAClusterEnergyCalibration,
                      addShapeParameters,
                      runPhotonIDTool)

    # ECAL endcap topoclusters
    EMECCaloTopoClusterInputs = {"ecalEndcap": ecalEndcapPositionedCellsName}
    EMECCaloTopoClusterReadouts = {"ecalEndcap": ecalEndcapReadoutName}
    setupTopoClusters(EMECCaloTopoClusterInputs,
                      EMECCaloTopoClusterReadouts,
                      "EMECCaloTopoClusters",
                      0.0,
                      dataFolder + "neighbours_map_ecalE_turbine.root",
                      dataFolder + "cellNoise_map_endcapTurbine_electronicsNoiseLevel.root",
                      False,
                      False,
                      False,
                      False)

    # ECAL topoclusters with noise
    if addNoise:
        EMBCaloTopoClusterInputsWithNoise = {"ecalBarrel": ecalBarrelPositionedCellsName + "WithNoise" if filterNoiseThreshold < 0 else ecalBarrelPositionedCellsName + "WithNoiseFiltered"}
        setupTopoClusters(EMBCaloTopoClusterInputsWithNoise,
                          EMBCaloTopoClusterReadouts,
                          "EMBCaloTopoClustersWithNoise" if filterNoiseThreshold < 0 else "EMBCaloTopoClustersWithNoiseFiltered",
                          0.1,
                          dataFolder + "neighbours_map_ecalB_thetamodulemerged.root",
                          dataFolder + "cellNoise_map_electronicsNoiseLevel_ecalB_thetamodulemerged.root",
                          applyUpDownstreamCorrections,
                          applyMVAClusterEnergyCalibration,
                          addShapeParameters,
                          runPhotonIDTool)

    # ECAL + HCAL
    if runHCal:
        CaloTopoClusterInputs = {
            "ecalBarrel": ecalBarrelPositionedCellsName,
            "ecalEndcap": ecalEndcapPositionedCellsName,
            "hcalBarrel": hcalBarrelPositionedCellsName,
            "hcalEndcap": hcalEndcapPositionedCellsName,
        }
        CaloTopoClusterReadouts = {
            "ecalBarrel": ecalBarrelReadoutName,
            "ecalEndcap": ecalEndcapReadoutName,
            "hcalBarrel": hcalBarrelReadoutName,
            "hcalEndcap": hcalEndcapReadoutName,
        }
        # note: the neighbour map links ecal and hcal barrels, and hcal barrel-endcap, but does not link (yet) the others
        setupTopoClusters(CaloTopoClusterInputs,
                          CaloTopoClusterReadouts,
                          "CaloTopoClusters",
                          0.0,
                          dataFolder + "neighbours_map_ecalB_thetamodulemerged_ecalE_turbine_hcalB_hcalEndcap_phitheta.root",
                          dataFolder + "cellNoise_map_electronicsNoiseLevel_ecalB_ECalBarrelModuleThetaMerged_ecalE_ECalEndcapTurbine_hcalB_HCalBarrelReadout_hcalE_HCalEndcapReadout.root",
                          False,
                          False,
                          False,
                          False)


################################################
#  Pandora
################################################
if runPandora:
    from Configurables import MarlinProcessorWrapper
    pandora = MarlinProcessorWrapper('DDMarlinPandora')
    pandora.OutputLevel = DEBUG
    pandora.ProcessorType = 'DDPandoraPFANewProcessor'
    pandora.Parameters = {
        "PandoraSettingsXmlFile": ["PandoraSettingsDefault.xml"],
        "ECalMipThreshold": ["0."],
        "HCalMipThreshold": ["0."],
        "ECalToHadGeVCalibrationBarrel": ["1."],  # this must be calculated for ALLEGRO
        "ECalToHadGeVCalibrationEndCap": ["1."],  # this must be calculated for ALLEGRO
        "HCalToHadGeVCalibration": ["1."],  # this must be calculated for ALLEGRO
        # "ECalToMipCalibration": ["175.439"],  # value is from CLD -> this must be calculated for ALLEGRO
        # "HCalToMipCalibration": ["49.7512"],  # value is from CLD -> this must be calculated for ALLEGRO
        "ECalToMipCalibration": ["26.0"],  # value is from CLD -> this must be calculated for ALLEGRO
        "HCalToMipCalibration": ["5.77"],  # value is from CLD -> this must be calculated for ALLEGRO
        "DigitalMuonHits": ["0"],
        "MaxHCalHitHadronicEnergy": ["10000000."],
        "MuonToMipCalibration": ["20703.9"],  # value is from CLD -> this must be calculated for ALLEGRO
        "ECalToEMGeVCalibration": ["1.0"],  # this seems to be an EM scale factor for ECAL: set to 1 since input cell energy is already calibrated at EM scale
        "HCalToEMGeVCalibration": ["1.0"],  # this seems to be an EM scale factor for HCAL: set to 1 since input cell energy is already calibrated at EM scale
        "DetectorName": ["ALLEGRO"],
        "UseDD4hepField": ["1"],
        "MCParticleCollections": ["MCParticle"],
        "ECalCaloHitCollections": [ecalBarrelPositionedCellsName],
        # "HCalCaloHitCollections": [hcalBarrelPositionedCellsName, hcalEndcapPositionedCellsName],
        "HCalCaloHitCollections": [hcalBarrelPositionedCellsName],
        "MuonCaloHitCollections": [muonBarrelPositionedCellsName],   #  muonEndcapPositionedCellsName],
        "RelCaloHitCollections": [ecalBarrelLinks, hcalBarrelLinks, muonBarrelLinks],
        "TrackCollections": ["TrackCollection"],
        "RelTrackCollections": ["TracksFromGenParticlesAssociation"],
    }
    TopAlg += [pandora]

    from Configurables import Lcio2EDM4hepTool
    lcioConvTool = Lcio2EDM4hepTool("lcio2EDM4hep")
    lcioConvTool.convertAll = True
    lcioConvTool.collNameMapping = {
        "MCParticle": "MCParticles",
        "TrackCollection": "TracksFromGenParticles",
    }
    pandora.Lcio2EDM4hepTool = lcioConvTool

    from Configurables import EDM4hep2LcioTool
    edm4hepConvTool = EDM4hep2LcioTool("EDM4hep2lcio")
    edm4hepConvTool.convertAll = True
    edm4hepConvTool.collNameMapping = {
        "MCParticles": "MCParticle",
        "TracksFromGenParticles": "TrackCollection",
    }
    pandora.EDM4hep2LcioTool = edm4hepConvTool

    # attempt to run pandora calibration
    pfoAnalysis = MarlinProcessorWrapper("PfoAnalysisWrapper")
    pfoAnalysis.OutputLevel = DEBUG
    pfoAnalysis.ProcessorType = ("PfoAnalysis")
    # how to use io_svc.Output instead of outputfile (overridden via cmd line)?
    # or to set via cmd line PfoAnalysisWrapper.Parameters[RootFile] ?
    outputFile = opts.pfaOutputFile
    if outputFile == "":
        outputFile = outputfile.replace(".root", "_PandoraAnalysis.root")
    pfoAnalysis.Parameters = {
        "RootFile"                          : [outputFile],
        "MCParticleCollection"              : ["MCParticle"],
        "PfoCollection"                     : ["PandoraPFANewPFOs"],
        "CollectCalibrationDetails"         : ["1"],
        # from LC digitisers
        # "ECalCollections"                   : ["ECALBarrel"],
        # "HCalCollections"                   : ["HCALBarrel"],
        # "MuonCollections"                   : ["MUON"],
        # from ALLEGRO digitisers
        "ECalCollections"                   : [ecalBarrelPositionedCellsName],
        "HCalCollections"                   : [hcalBarrelPositionedCellsName],
        "MuonCollections"                   : [muonBarrelPositionedCellsName],
        "ECalCollectionsSimCaloHit"         : [ecalBarrelReadoutName],
        "HCalBarrelCollectionsSimCaloHit"   : [hcalBarrelReadoutName],
        "MuonCollectionsSimCaloHit"         : [muonBarrelReadoutName],
    #     "BCALcollections"             : [""],  # BeamCal
    #     "LHCALcollections"            : [""],  # ? lumi -hcal?
    #     "LCALcollections"             : [""],  # ? lumi -ecal?
    }
    TopAlg += [pfoAnalysis]


    # see https://github.com/Pandora/PFA/LCPandoraAnalysis/blob/master/scripts/PandoraPfaCalibrator.xml
    #     https://github.com/Pandora/PFA/LCPandoraAnalysis/blob/master/include/PandoraPfaCalibrator.h
    #     https://github.com/Pandora/PFA/LCPandoraAnalysis/blob/master/src/PandoraPfaCalibrator.cc
    # and https://github.com/Pandora/PFA/LCPandoraAnalysis/blob/master/include/CalibrationHelper.h
    #     https://github.com/Pandora/PFA/LCPandoraAnalysis/blob/master/include/CalibrationHelper.cc
    # and executables in https://github.com/Pandora/PFA/LCPandoraAnalysis/blob/master/calibration
    
    
    # pandoraCalibrator = MarlinProcessorWrapper( "PandoraPFACalibratorWrapper" )
    # pandoraCalibrator.OutputLevel = DEBUG
    # pandoraCalibrator.ProcessorType = ( "PandoraPFACalibrator" )
    # pandoraCalibrator.Parameters = {
    #     # "RootFile" : "PandoraPFACalibrator.root",
    #     "MCPfoCollections"            : ["MCPFOs"],
    #     "ReconstructedPfoCollections" : ["PandoraPFOs"],
    #     "ECALBarrelcollections"       : ["ECalBarrelModuleThetaMergedPositioned"],
    #     "ECALEndCapcollections"       : [""],
    #     "HCALcollections"             : ["HCalBarrelReadoutPositioned"],
    #     "MUONcollections"             : ["MuonTaggerBarrelPhiThetaPositioned"],
    #     "BCALcollections"             : [""],  # what is this?
    #     "LHCALcollections"            : [""],  # what is this?  
    #     "LCALcollections"             : [""],  # what is this?
    #     "ECALBarrelEncoding"          : ["system:4,cryo:1,type:3,subtype:3,layer:8,module:11,theta:10"],
    #     "ECALEndCapEncoding"          : ["system:4,cryo:1,type:3,subtype:3,side:-2,wheel:3,layer:8,module:17,rho:8,z:8"],
    #     "HCALEncoding"                : ["system:4,layer:5,row:9,theta:9,phi:10"],
    #     "MUONEncoding"                : ["system:4,subsystem:1,layer:5,theta:10,phi:10"]
    #     }
    # TopAlg += [pandoraCalibrator]


# Configure the output

# drop the empty cells
io_svc.outputCommands = ["keep *",
                         "drop emptyCaloCells"]

# drop the uncalibrated cells
if dropUncalibratedCells:
    io_svc.outputCommands.append("drop %s" % ecalBarrelReadoutName)
    io_svc.outputCommands.append("drop %s" % ecalBarrelReadoutName2)
    io_svc.outputCommands.append("drop %s" % ecalEndcapReadoutName)
    if runHCal:
        io_svc.outputCommands.append("drop %s" % hcalBarrelReadoutName)
        io_svc.outputCommands.append("drop %s" % hcalEndcapReadoutName)
    else:
        io_svc.outputCommands += ["drop HCal*"]

    # drop the intermediate ecal barrel cells in case of a resegmentation
    if resegmentECalBarrel:
        io_svc.outputCommands.append("drop ECalBarrelCellsMerged")

# drop lumi, vertex, DCH, Muons (unless want to keep for event display)
if dropLumiCalHits:
    io_svc.outputCommands.append("drop Lumi*")
if dropVertexHits:
    io_svc.outputCommands.append("drop VertexBarrelCollection*")
    io_svc.outputCommands.append("drop VertexEndcapCollection*")
if dropDCHHits:
    io_svc.outputCommands.append("drop DCHCollection*")
if dropSiWrHits:
    io_svc.outputCommands.append("drop SiWrBCollection*")
    io_svc.outputCommands.append("drop SiWrDCollection*")
if dropMuonHits:
    io_svc.outputCommands.append("drop MuonTagger*PhiTheta")   # hits
    io_svc.outputCommands.append("drop MuonTagger*PhiThetaPositioned")   # cells

# drop hits/positioned cells/cluster cells if desired
if not saveHits:
    io_svc.outputCommands.append("drop *%sContributions" % ecalBarrelReadoutName)
    io_svc.outputCommands.append("drop *%sContributions" % ecalBarrelReadoutName2)
    io_svc.outputCommands.append("drop *%sContributions" % ecalEndcapReadoutName)
    if runHCal:
        io_svc.outputCommands.append("drop *%sContributions" % hcalBarrelReadoutName)
        io_svc.outputCommands.append("drop *%sContributions" % hcalEndcapReadoutName)
if not saveCells:
    io_svc.outputCommands.append("drop %s" % ecalBarrelPositionedCellsName)
    io_svc.outputCommands.append("drop %s" % ecalEndcapPositionedCellsName)
    if addNoise:
        io_svc.outputCommands.append("drop %sWithNoise*" % ecalBarrelPositionedCellsName)
        io_svc.outputCommands.append("drop %sWithNoise*" % ecalEndcapPositionedCellsName)
    if resegmentECalBarrel:
        io_svc.outputCommands.append("drop %s" % ecalBarrelPositionedCellsName2)
    if runHCal:
        io_svc.outputCommands.append("drop %s" % hcalBarrelPositionedCellsName)
        io_svc.outputCommands.append("drop %s" % hcalEndcapPositionedCellsName)
if not saveClusterCells:
    io_svc.outputCommands.append("drop *Calo*Cluster*Cells*")
# drop hits<->cells links if either of the two collections are not saved
if not saveHits or not saveCells:
    io_svc.outputCommands.append("drop *SimCaloHitLinks")

# if we decorate the clusters, we can drop the non-decorated ones
if addShapeParameters:
    for algo in TopAlg:
        if algo.__class__.__name__ == "AugmentClustersFCCee":
            io_svc.outputCommands.append("drop %s" % algo.inClusters)


# configure the application
print(TopAlg)
print(ExtSvc)
from k4FWCore import ApplicationMgr
applicationMgr = ApplicationMgr(
    TopAlg=TopAlg,
    EvtSel='NONE',
    EvtMax=Nevts,
    ExtSvc=ExtSvc,
    StopOnSignal=True,
)

for algo in applicationMgr.TopAlg:
    algo.AuditExecute = True
    # for debug
    # algo.OutputLevel = DEBUG
