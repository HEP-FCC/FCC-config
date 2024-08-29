from Configurables import ApplicationMgr
from Configurables import AuditorSvc, ChronoAuditor
from Configurables import k4DataSvc, PodioInput
from Configurables import PodioOutput
from Configurables import GeoSvc
from Configurables import CorrectCaloClusters
from Configurables import CreateCaloClustersSlidingWindowFCCee
from Configurables import CaloTowerToolFCCee
from Configurables import CreateEmptyCaloCellsCollection
from Configurables import CreateCaloCellPositionsFCCee
from Configurables import CellPositionsECalBarrelModuleThetaSegTool
from Configurables import RedoSegmentation
from Configurables import CreateCaloCells
from Configurables import CalibrateCaloHitsTool
from Configurables import CalibrateInLayersTool
from Configurables import HepMCToEDMConverter
from Configurables import CaloTopoClusterInputTool
from Configurables import TopoCaloNeighbours
from Configurables import TopoCaloNoisyCells
from Configurables import CaloTopoClusterFCCee

from Gaudi.Configuration import *
import os

from GaudiKernel.SystemOfUnits import GeV, tesla
_pi = 3.14159

dumpGDML = False
runHCal = False

# Loading the output of the SIM step
evtsvc = k4DataSvc('EventDataSvc')
evtsvc.input = "./ALLEGRO_sim.root"
Nevts = 100

input_reader = PodioInput('InputReader')

podioevent = k4DataSvc("EventDataSvc")

# Detector geometry
geoservice = GeoSvc("GeoSvc")
# if K4GEO is empty, this should use relative path to working directory
path_to_detector = os.environ.get("K4GEO", "")
print(path_to_detector)
detectors_to_use = [
    'FCCee/ALLEGRO/compact/ALLEGRO_o1_v02/ALLEGRO_o1_v02.xml'
]
# prefix all xmls with path_to_detector
geoservice.detectors = [
    os.path.join(path_to_detector, _det) for _det in detectors_to_use
]
geoservice.OutputLevel = INFO

# from Configurables import GeoToGdmlDumpSvc
if dumpGDML:
    from Configurables import GeoToGdmlDumpSvc
    gdmldumpservice = GeoToGdmlDumpSvc("GeoToGdmlDumpSvc")

# Detector readouts
# ECAL
ecalBarrelReadoutName = "ECalBarrelModuleThetaMerged"
ecalBarrelReadoutName2 = "ECalBarrelModuleThetaMerged2"
ecalEndcapReadoutName = "ECalEndcapPhiEta"
ecalBarrelHitsName = ecalBarrelReadoutName # ddsim stores simHit collection with name as the readout name defined for the detector
# HCAL
if runHCal:
    hcalBarrelReadoutName = "HCalBarrelReadout"
    hcalEndcapReadoutName = "HCalEndcapReadout"
else:
    hcalBarrelReadoutName = ""
    hcalEndcapReadoutName = ""

# Digitization (Merging hits into cells, EM scale calibration)
# EM scale calibration (sampling fraction)
calibEcalBarrel = CalibrateInLayersTool("CalibrateECalBarrel",
                                        samplingFraction=[0.36599110182660616] * 1 + [0.1366222373338866] * 1 + [0.1452035173747207] * 1 + [0.1504319190969367] * 1 + [0.15512713637727382] * 1 + [0.1592916726494782] * 1 + [
                                            0.16363478857307595] * 1 + [0.1674697333180323] * 1 + [0.16998205747422343] * 1 + [0.1739146363733975] * 1 + [0.17624609543603845] * 1 + [0.1768613530850488] * 1,
                                        readoutName=ecalBarrelReadoutName,
                                        layerFieldName="layer")

calibEcalEndcap = CalibrateCaloHitsTool(
    "CalibrateECalEndcap", invSamplingFraction="4.27")
if runHCal:
    calibHcells = CalibrateCaloHitsTool(
        "CalibrateHCal", invSamplingFraction="31.4")
    calibHcalEndcap = CalibrateCaloHitsTool(
        "CalibrateHCalEndcap", invSamplingFraction="31.7")

# Create cells in ECal barrel
# 1. step - merge hits into cells with theta and module segmentation
# (module is a 'physical' cell i.e. lead + LAr + PCB + LAr +lead)
# 2. step - rewrite the cellId using the merged theta-module segmentation
# (merging several modules and severla theta readout cells).
# Add noise at this step if you derived the noise already assuming merged cells

# Step 1: merge hits into cells according to initial segmentation
ecalBarrelCellsName = "ECalBarrelCells"
createEcalBarrelCells = CreateCaloCells("CreateECalBarrelCells",
                                        doCellCalibration=True,
                                        calibTool=calibEcalBarrel,
                                        addCellNoise=False,
                                        filterCellNoise=False,
                                        addPosition=True,
                                        OutputLevel=INFO,
                                        hits=ecalBarrelHitsName,
                                        cells=ecalBarrelCellsName)

# Step 2a: compute new cellID of cells based on new readout
# (merged module-theta segmentation with variable merging vs layer)
resegmentEcalBarrel = RedoSegmentation("ReSegmentationEcal",
                                       # old bitfield (readout)
                                       oldReadoutName=ecalBarrelReadoutName,
                                       # specify which fields are going to be altered (deleted/rewritten)
                                       oldSegmentationIds=["module", "theta"],
                                       # new bitfield (readout), with new segmentation (merged modules and theta cells)
                                       newReadoutName=ecalBarrelReadoutName2,
                                       OutputLevel=INFO,
                                       debugPrint=200,
                                       inhits=ecalBarrelCellsName,
                                       outhits="ECalBarrelCellsMerged")

# Step 2b: merge new cells with same cellID together
# do not apply cell calibration again since cells were already
# calibrated in Step 1
ecalBarrelCellsName2 = "ECalBarrelCells2"
createEcalBarrelCells2 = CreateCaloCells("CreateECalBarrelCells2",
                                         doCellCalibration=False,
                                         addCellNoise=False,
                                         filterCellNoise=False,
                                         OutputLevel=INFO,
                                         hits="ECalBarrelCellsMerged",
                                         cells=ecalBarrelCellsName2)

# Add to Ecal barrel cells the position information
# (good for physics, all coordinates set properly)

cellPositionEcalBarrelTool = CellPositionsECalBarrelModuleThetaSegTool(
    "CellPositionsECalBarrel",
    readoutName=ecalBarrelReadoutName,
    OutputLevel=INFO
)
ecalBarrelPositionedCellsName = "ECalBarrelPositionedCells"
createEcalBarrelPositionedCells = CreateCaloCellPositionsFCCee(
    "CreateECalBarrelPositionedCells",
    OutputLevel=INFO
)
createEcalBarrelPositionedCells.positionsTool = cellPositionEcalBarrelTool
createEcalBarrelPositionedCells.hits.Path = ecalBarrelCellsName
createEcalBarrelPositionedCells.positionedHits.Path = ecalBarrelPositionedCellsName

cellPositionEcalBarrelTool2 = CellPositionsECalBarrelModuleThetaSegTool(
    "CellPositionsECalBarrel2",
    readoutName=ecalBarrelReadoutName2,
    OutputLevel=INFO
)
createEcalBarrelPositionedCells2 = CreateCaloCellPositionsFCCee(
    "CreateECalBarrelPositionedCells2",
    OutputLevel=INFO
)
createEcalBarrelPositionedCells2.positionsTool = cellPositionEcalBarrelTool2
createEcalBarrelPositionedCells2.hits.Path = ecalBarrelCellsName2
createEcalBarrelPositionedCells2.positionedHits.Path = "ECalBarrelPositionedCells2"


# Create cells in ECal endcap
createEcalEndcapCells = CreateCaloCells("CreateEcalEndcapCaloCells",
                                        doCellCalibration=True,
                                        calibTool=calibEcalEndcap,
                                        addCellNoise=False,
                                        filterCellNoise=False,
                                        OutputLevel=INFO)
createEcalEndcapCells.hits.Path = "ECalEndcapPhiEta"
createEcalEndcapCells.cells.Path = "ECalEndcapCells"

if runHCal:
    # Create cells in HCal
    # 1. step - merge hits into cells with the default readout
    hcalBarrelCellsName = "HCalBarrelCells"
    createHcalBarrelCells = CreateCaloCells("CreateHCalBarrelCells",
                                            doCellCalibration=True,
                                            calibTool=calibHcells,
                                            addCellNoise=False,
                                            filterCellNoise=False,
                                            addPosition=True,
                                            hits=hcalBarrelHitsName,
                                            cells=hcalBarrelCellsName,
                                            OutputLevel=INFO)

    # createHcalEndcapCells = CreateCaloCells("CreateHcalEndcapCaloCells",
    #                                    doCellCalibration=True,
    #                                    calibTool=calibHcalEndcap,
    #                                    addCellNoise=False,
    #                                    filterCellNoise=False,
    #                                    OutputLevel=INFO)
    # createHcalEndcapCells.hits.Path="HCalEndcapHits"
    # createHcalEndcapCells.cells.Path="HCalEndcapCells"

    from Configurables import CellPositionsHCalBarrelPhiThetaSegTool
    cellPositionHcalBarrelTool = CellPositionsHCalBarrelPhiThetaSegTool(
        "CellPositionsHCalBarrel",
        readoutName=hcalBarrelReadoutName,
        OutputLevel=INFO
    )
    hcalBarrelPositionedCellsName = "HCalBarrelPositionedCells"    
    createHcalBarrelPositionedCells = CreateCaloCellPositionsFCCee(
        "CreateHcalBarrelPositionedCells",
        OutputLevel=INFO
    )
    createHcalBarrelPositionedCells.positionsTool = cellPositionHcalBarrelTool
    createHcalBarrelPositionedCells.hits.Path = hcalBarrelCellsName
    createHcalBarrelPositionedCells.positionedHits.Path = hcalBarrelPositionedCellsName
else:
    hcalBarrelCellsName = "emptyCaloCells"
    hcalBarrelPositionedCellsName = "emptyCaloCells"
    cellPositionHcalBarrelTool = None
    
# Empty cells for parts of calorimeter not implemented yet
createemptycells = CreateEmptyCaloCellsCollection("CreateEmptyCaloCells")
createemptycells.cells.Path = "emptyCaloCells"

# Produce sliding window clusters
towers = CaloTowerToolFCCee("towers",
                       deltaThetaTower = 0.009817477, deltaPhiTower = 2*2*_pi/1536.,
                       ecalBarrelReadoutName=ecalBarrelReadoutName,
                       ecalEndcapReadoutName=ecalEndcapReadoutName,
                       ecalFwdReadoutName="",
                       hcalBarrelReadoutName=hcalBarrelReadoutName,
                       hcalExtBarrelReadoutName="",
                       hcalEndcapReadoutName="",
                       hcalFwdReadoutName="",
                       OutputLevel=INFO)
towers.ecalBarrelCells.Path = ecalBarrelPositionedCellsName
towers.ecalEndcapCells.Path = "ECalEndcapCells"
towers.ecalFwdCells.Path = "emptyCaloCells"

towers.hcalBarrelCells.Path = hcalBarrelCellsName
towers.hcalExtBarrelCells.Path = "emptyCaloCells"
towers.hcalEndcapCells.Path = "emptyCaloCells"
towers.hcalFwdCells.Path = "emptyCaloCells"

# Cluster variables
windT = 9
windP = 17
posT = 5
posP = 11
dupT = 7
dupP = 13
finT = 9
finP = 17
# Minimal energy to create a cluster in GeV (FCC-ee detectors have to reconstruct low energy particles)
threshold = 0.040

createClusters = CreateCaloClustersSlidingWindowFCCee("CreateClusters",
                                                 towerTool=towers,
                                                 nThetaWindow=windT, nPhiWindow=windP,
                                                 nThetaPosition=posT, nPhiPosition=posP,
                                                 nThetaDuplicates=dupT, nPhiDuplicates=dupP,
                                                 nThetaFinal=finT, nPhiFinal=finP,
                                                 energyThreshold=threshold,
                                                 energySharingCorrection=False,
                                                 attachCells=True,
                                                 OutputLevel=INFO
                                                 )
createClusters.clusters.Path = "CaloClusters"
createClusters.clusterCells.Path = "CaloClusterCells"

createEcalBarrelPositionedCaloClusterCells = CreateCaloCellPositionsFCCee(
    "ECalBarrelPositionedCaloClusterCells",
    OutputLevel=INFO
)
createEcalBarrelPositionedCaloClusterCells.positionsTool = cellPositionEcalBarrelTool
createEcalBarrelPositionedCaloClusterCells.hits.Path = "CaloClusterCells"
createEcalBarrelPositionedCaloClusterCells.positionedHits.Path = "PositionedCaloClusterCells"

correctCaloClusters = CorrectCaloClusters("correctCaloClusters",
                                          inClusters=createClusters.clusters.Path,
                                          outClusters="Corrected"+createClusters.clusters.Path,
                                          numLayers=[12],
                                          firstLayerIDs=[0],
                                          lastLayerIDs=[11],
                                          # readoutNames = [ecalBarrelReadoutNamePhiEta],
                                          readoutNames=[ecalBarrelReadoutName],
                                          # upstreamParameters = [[0.02729094887360858, -1.378665489864182, -68.40424543618059, 3.6930827214130053, -5528.714729126099, -1630.7911298009794]],
                                          upstreamParameters=[
                                              [0.02729094887360858, -1.378665489864182, -68.40424543618059, 3.6930827214130053, -5528.714729126099, -1630.7911298009794]],
                                          upstreamFormulas=[
                                              ['[0]+[1]/(x-[2])', '[0]+[1]/(x-[2])']],
                                          # downstreamParameters = [[-0.0032351643028483354, 0.006597484738888312, 0.8972024981692965, -1.0207168610322181, 0.017878133854084398, 9.108099243443101]],
                                          downstreamParameters=[
                                              [-0.0032351643028483354, 0.006597484738888312, 0.8972024981692965, -1.0207168610322181, 0.017878133854084398, 9.108099243443101]],
                                          downstreamFormulas=[
                                              ['[0]+[1]*x', '[0]+[1]/sqrt(x)', '[0]+[1]/x']],
                                          OutputLevel=INFO
                                          )

# TOPO CLUSTERS PRODUCTION
createTopoInput = CaloTopoClusterInputTool("CreateTopoInput",
                                           ecalBarrelReadoutName=ecalBarrelReadoutName,
                                           ecalEndcapReadoutName="",
                                           ecalFwdReadoutName="",
                                           hcalBarrelReadoutName=hcalBarrelReadoutName,
                                           hcalExtBarrelReadoutName="",
                                           hcalEndcapReadoutName="",
                                           hcalFwdReadoutName="",
                                           OutputLevel=INFO)

createTopoInput.ecalBarrelCells.Path = ecalBarrelPositionedCellsName
# createTopoInput.ecalBarrelCells.Path = "ECalBarrelPositionedCells2"
createTopoInput.ecalEndcapCells.Path = "emptyCaloCells"
createTopoInput.ecalFwdCells.Path = "emptyCaloCells"
createTopoInput.hcalBarrelCells.Path = hcalBarrelPositionedCellsName
createTopoInput.hcalExtBarrelCells.Path = "emptyCaloCells"
createTopoInput.hcalEndcapCells.Path = "emptyCaloCells"
createTopoInput.hcalFwdCells.Path = "emptyCaloCells"
cellPositionHcalBarrelNoSegTool = None
cellPositionHcalExtBarrelTool = None

readNeighboursMap = TopoCaloNeighbours("ReadNeighboursMap",
                                       fileName = "./data/neighbours_map_barrel_thetamodulemerged.root",
                                       OutputLevel=INFO)

# Noise levels per cell
readNoisyCellsMap = TopoCaloNoisyCells("ReadNoisyCellsMap",
                                       fileName="./data/cellNoise_map_electronicsNoiseLevel_thetamodulemerged.root",
                                       OutputLevel=INFO)

createTopoClusters = CaloTopoClusterFCCee("CreateTopoClusters",
                                          TopoClusterInput=createTopoInput,
                                          # expects neighbours map from cellid->vec < neighbourIds >
                                          neigboursTool=readNeighboursMap,
                                          # tool to get noise level per cellid
                                          noiseTool=readNoisyCellsMap,
                                          # cell positions tools for all sub - systems
                                          positionsECalBarrelTool=cellPositionEcalBarrelTool,
                                          positionsHCalBarrelTool=cellPositionHcalBarrelTool,
                                          positionsHCalBarrelNoSegTool=cellPositionHcalBarrelNoSegTool,
                                          positionsHCalExtBarrelTool=cellPositionHcalExtBarrelTool,
                                          # positionsHCalExtBarrelTool = HCalExtBcells,
                                          # positionsEMECTool = EMECcells,
                                          # positionsHECTool = HECcells,
                                          # positionsEMFwdTool = ECalFwdcells,
                                          # positionsHFwdTool = HCalFwdcells,
                                          noSegmentationHCal=False,
                                          seedSigma=4,
                                          neighbourSigma=2,
                                          lastNeighbourSigma=0,
                                          OutputLevel=INFO)
createTopoClusters.clusters.Path = "CaloTopoClusters"
createTopoClusters.clusterCells.Path = "CaloTopoClusterCells"

createEcalBarrelPositionedCaloTopoClusterCells = CreateCaloCellPositionsFCCee(
    "ECalBarrelPositionedCaloTopoClusterCells",
    OutputLevel=INFO
)
# createEcalBarrelPositionedCaloTopoClusterCells.positionsTool = cellPositionEcalBarrelTool2
createEcalBarrelPositionedCaloTopoClusterCells.positionsTool = cellPositionEcalBarrelTool
createEcalBarrelPositionedCaloTopoClusterCells.hits.Path = "CaloTopoClusterCells"
createEcalBarrelPositionedCaloTopoClusterCells.positionedHits.Path = "PositionedCaloTopoClusterCells"

correctCaloTopoClusters = CorrectCaloClusters(
    "correctCaloTopoClusters",
    inClusters=createTopoClusters.clusters.Path,
    outClusters="Corrected"+createTopoClusters.clusters.Path,
    numLayers=[12],
    firstLayerIDs=[0],
    lastLayerIDs=[11],
    # readoutNames = [ecalBarrelReadoutNamePhiEta],
    readoutNames=[ecalBarrelReadoutName],
    # upstreamParameters = [[0.02729094887360858, -1.378665489864182, -68.40424543618059, 3.6930827214130053, -5528.714729126099, -1630.7911298009794]],
    upstreamParameters=[[0.02729094887360858, -1.378665489864182, -68.40424543618059,
                         3.6930827214130053, -5528.714729126099, -1630.7911298009794]],
    upstreamFormulas=[['[0]+[1]/(x-[2])', '[0]+[1]/(x-[2])']],
    # downstreamParameters = [[-0.0032351643028483354, 0.006597484738888312, 0.8972024981692965, -1.0207168610322181, 0.017878133854084398, 9.108099243443101]],
    downstreamParameters=[[-0.0032351643028483354, 0.006597484738888312,
                           0.8972024981692965, -1.0207168610322181, 0.017878133854084398, 9.108099243443101]],
    downstreamFormulas=[['[0]+[1]*x', '[0]+[1]/sqrt(x)', '[0]+[1]/x']],
    OutputLevel=INFO
)

# Output
out = PodioOutput("out",
                  OutputLevel=INFO)

out.outputCommands = ["keep *", "drop emptyCaloCells", "drop ECalBarrelCells", "drop ECalBarrelCells2", "drop ECalBarrelCellsMerged", "drop CaloTopoClusterCells"]

out.filename = "ALLEGRO_sim_digi_reco.root"

# CPU information
chra = ChronoAuditor()
audsvc = AuditorSvc()
audsvc.Auditors = [chra]
createEcalBarrelCells.AuditExecute = True
createEcalBarrelPositionedCells.AuditExecute = True
if runHCal:
    createHcalBarrelCells.AuditExecute = True
createTopoClusters.AuditExecute = True
out.AuditExecute = True

ExtSvc = [evtsvc, geoservice, podioevent, audsvc]
if dumpGDML:
    ExtSvc += [gdmldumpservice]

TopAlg = [
    input_reader,
    createEcalBarrelCells,
    createEcalBarrelPositionedCells,
    resegmentEcalBarrel,
    createEcalBarrelCells2,
    createEcalBarrelPositionedCells2,
    createEcalEndcapCells
]
if runHCal:
    TopAlg += [
        createHcalBarrelCells,
        createHcalBarrelPositionedCells,
        # createHcalEndcapCells
    ]
TopAlg += [
    createemptycells,
    createClusters,
    createEcalBarrelPositionedCaloClusterCells,
    correctCaloClusters,
    createTopoClusters,
    createEcalBarrelPositionedCaloTopoClusterCells,
    correctCaloTopoClusters,
    out
]

ApplicationMgr(
    TopAlg=TopAlg,
    EvtSel='NONE',
    EvtMax=Nevts,
    ExtSvc=ExtSvc,
    StopOnSignal=True,
)
