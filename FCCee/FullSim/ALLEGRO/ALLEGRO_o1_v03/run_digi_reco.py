#
# IMPORTS
#
from Configurables import ApplicationMgr
from Configurables import EventCounter
from Configurables import AuditorSvc, ChronoAuditor
# Input/output
from Configurables import k4DataSvc, PodioInput
from Configurables import PodioOutput
# Geometry
from Configurables import GeoSvc
# Create cells
from Configurables import CreateCaloCells
from Configurables import CreateEmptyCaloCellsCollection
# Cell positioning tools
from Configurables import CreateCaloCellPositionsFCCee
from Configurables import CellPositionsECalBarrelModuleThetaSegTool
# Redo segmentation for ECAL
from Configurables import RedoSegmentation
# Change HCAL segmentation
from Configurables import RewriteBitfield
# Apply sampling fraction corrections
from Configurables import CalibrateCaloHitsTool
from Configurables import CalibrateInLayersTool
# Up/down stream correction
from Configurables import CorrectCaloClusters
# SW clustering
from Configurables import CaloTowerToolFCCee
from Configurables import CreateCaloClustersSlidingWindowFCCee
# Topo clustering
from Configurables import CaloTopoClusterInputTool
from Configurables import TopoCaloNeighbours
from Configurables import TopoCaloNoisyCells
from Configurables import CaloTopoClusterFCCee
# Decorate clusters with shower shape parameters
from Configurables import AugmentClustersFCCee
# MVA calibration
from Configurables import CalibrateCaloClusters
# photon/pi0 identification
from Configurables import PhotonIDTool
# Logger
from Gaudi.Configuration import INFO, VERBOSE, DEBUG
# units and physical constants
from GaudiKernel.SystemOfUnits import GeV, tesla, mm
from GaudiKernel.PhysicalConstants import pi, halfpi, twopi
# python libraries
import os
from math import cos, sin, tan

#
# SETTINGS
#

# - general settings
#
inputfile = "ALLEGRO_sim.root"
Nevts = -1  # -1 means all events
dumpGDML = False
runHCal = True

# - what to save in output file
#
# for big productions, save significant space removing hits and cells
# however, hits and cluster cells might be wanted for small productions for detailed event displays
# cluster cells are not needed for the training of the MVA energy regression nor the photon ID since needed quantities are stored in cluster shapeParameters
# saveHits = False
# saveCells = False
# saveClusterCells = False
saveHits = True
saveCells = True
saveClusterCells = True

# ECAL barrel parameters for digitisation
samplingFraction=[0.3800493723322256] * 1 + [0.13494147915064658] * 1 + [0.142866851721152] * 1 + [0.14839315921940666] * 1 + [0.15298362570665006] * 1 + [0.15709704561942747] * 1 + [0.16063717490147533] * 1 + [0.1641723795419055] * 1 + [0.16845490287689746] * 1 + [0.17111520115997653] * 1 + [0.1730605163148862] * 1
upstreamParameters = [[0.025582045561310333, -0.9524128168665387, -53.10089405478649, 1.283851527438571, -295.30650178662637, -284.8945817377308]]  # FIXME: to be updated for ddsim
downstreamParameters = [[0.0018280333929494054, 0.004932212590963076, 0.8409676097173655, -1.2676690014715288, 0.005347798049886769, 4.161741293789687]]  # FIXME: to be updated for ddsim
    
ecalBarrelLayers = len(samplingFraction)
resegmentECalBarrel = False

# - parameters for clustering
#
doSWClustering = True
doTopoClustering = True

# cluster energy corrections
# simple parametrisations of up/downstream losses
# not to be applied for ECAL+HCAL clustering
applyUpDownstreamCorrections = False and not runHCal

# BDT regression from total cluster energy and fraction of energy in each layer (after correction for sampling fraction)
# not to be applied (yet) for ECAL+HCAL clustering (MVA trained only on ECAL so far)
applyMVAClusterEnergyCalibration = True and not runHCal

# calculate cluster energy and barycenter per layer and save it as extra parameters
addShapeParameters = True and not runHCal
ecalBarrelThetaWeights = [-1, 3.0, 3.0, 3.0, 4.25, 4.0, 4.0, 4.0, 4.0, 4.0, 4.0]  # to be recalculated for V03, separately for topo and calo clusters...

# run photon ID algorithm
runPhotonIDTool = False

#
# ALGORITHMS AND SERVICES SETUP
#

# Input: load the output of the SIM step
podioevent = k4DataSvc('EventDataSvc')
podioevent.input = inputfile
input_reader = PodioInput('InputReader')


# Detector geometry
# prefix all xmls with path_to_detector
# if K4GEO is empty, this should use relative path to working directory
geoservice = GeoSvc("GeoSvc")
path_to_detector = os.environ.get("K4GEO", "")
detectors_to_use = [
    'FCCee/ALLEGRO/compact/ALLEGRO_o1_v03/ALLEGRO_o1_v03.xml'
]
geoservice.detectors = [
    os.path.join(path_to_detector, _det) for _det in detectors_to_use
]
geoservice.OutputLevel = INFO

# GDML dump of detector model
if dumpGDML:
    from Configurables import GeoToGdmlDumpSvc
    gdmldumpservice = GeoToGdmlDumpSvc("GeoToGdmlDumpSvc")

# Digitisation (merging hits into cells, EM scale calibration via sampling fractions)

# - ECAL readouts
ecalBarrelReadoutName = "ECalBarrelModuleThetaMerged"
ecalBarrelReadoutName2 = "ECalBarrelModuleThetaMerged2"
ecalEndcapReadoutName = "ECalEndcapPhiEta"
# - HCAL readouts
if runHCal:
    hcalBarrelReadoutName = "HCalBarrelReadout"
    hcalBarrelReadoutName2 = "BarHCal_Readout_phitheta"
    hcalEndcapReadoutName = "HCalEndcapReadout"
else:
    hcalBarrelReadoutName = ""
    hcalBarrelReadoutName2 = ""
    hcalEndcapReadoutName = ""

# - EM scale calibration (sampling fraction)
#   * ECAL barrel
calibEcalBarrel = CalibrateInLayersTool("CalibrateECalBarrel",
                                        samplingFraction=samplingFraction,
                                        readoutName=ecalBarrelReadoutName,
                                        layerFieldName="layer")
#   * ECAL endcap
calibEcalEndcap = CalibrateCaloHitsTool(
    "CalibrateECalEndcap", invSamplingFraction="4.27")  # FIXME: to be updated for ddsim

if runHCal:
    # HCAL barrel
    calibHcells = CalibrateCaloHitsTool(
        "CalibrateHCal", invSamplingFraction="29.4202")
    # HCAL endcap
    calibHcalEndcap = CalibrateCaloHitsTool(
        "CalibrateHCalEndcap", invSamplingFraction="29.4202")  # FIXME: to be updated for ddsim

# Create cells in ECal barrel (needed if one wants to apply cell calibration,
# which is not performed by ddsim)
# - merge hits into cells according to initial segmentation
ecalBarrelCellsName = "ECalBarrelCells"
createEcalBarrelCells = CreateCaloCells("CreateECalBarrelCells",
                                        doCellCalibration=True,
                                        calibTool=calibEcalBarrel,
                                        addCellNoise=False,
                                        filterCellNoise=False,
                                        addPosition=True,
                                        OutputLevel=INFO,
                                        hits=ecalBarrelReadoutName,
                                        cells=ecalBarrelCellsName)

# - add to Ecal barrel cells the position information
#   (good for physics, all coordinates set properly)
cellPositionEcalBarrelTool = CellPositionsECalBarrelModuleThetaSegTool(
    "CellPositionsECalBarrel",
    readoutName=ecalBarrelReadoutName,
    OutputLevel=INFO
)
ecalBarrelPositionedCellsName = ecalBarrelReadoutName + "Positioned"
createEcalBarrelPositionedCells = CreateCaloCellPositionsFCCee(
    "CreateECalBarrelPositionedCells",
    OutputLevel=INFO
)
createEcalBarrelPositionedCells.positionsTool = cellPositionEcalBarrelTool
createEcalBarrelPositionedCells.hits.Path = ecalBarrelCellsName
createEcalBarrelPositionedCells.positionedHits.Path = ecalBarrelPositionedCellsName

# -  now, if we want to also save cells with coarser granularity:
if resegmentECalBarrel:
    # 2. step - rewrite the cellId using the merged theta-module segmentation
    # (merging several modules and severla theta readout cells).
    # Add noise at this step if you derived the noise already assuming merged cells
    # Step 2a: compute new cellID of cells based on new readout
    # (merged module-theta segmentation with variable merging vs layer)
    resegmentEcalBarrelTool = RedoSegmentation("ReSegmentationEcal",
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
    createEcalBarrelPositionedCells2.positionedHits.Path = ecalBarrelReadoutName2 + "Positioned"


# Create cells in ECal endcap (needed if one wants to apply cell calibration,
# which is not performed by ddsim)
createEcalEndcapCells = CreateCaloCells("CreateEcalEndcapCaloCells",
                                        doCellCalibration=True,
                                        calibTool=calibEcalEndcap,
                                        addCellNoise=False,
                                        filterCellNoise=False,
                                        OutputLevel=INFO)
createEcalEndcapCells.hits.Path = ecalEndcapReadoutName
createEcalEndcapCells.cells.Path = "ECalEndcapCells"

if runHCal:
    # Create cells in HCal barrel
    # 1 - merge hits into cells with the default readout
    hcalBarrelCellsName = "HCalBarrelCells"
    createHcalBarrelCells = CreateCaloCells("CreateHCalBarrelCells",
                                            doCellCalibration=True,
                                            calibTool=calibHcells,
                                            addCellNoise=False,
                                            filterCellNoise=False,
                                            addPosition=True,
                                            hits=hcalBarrelReadoutName,
                                            cells=hcalBarrelCellsName,
                                            OutputLevel=INFO)

    # 2 - attach positions to the cells (cell positions needed for RedoSegmentation!)
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

    # 3 - compute new cellID of cells based on new readout - removing row information
    # We use a RedoSegmentation. Using a RewriteBitField with removeIds=["row"],
    # wont work because there are tiles with same layer/theta/phi but different row
    # as a consequence there will be multiple cells with same cellID in the output collection
    # and this will screw up the SW clustering
    hcalBarrelCellsName2 = "HCalBarrelCells2"

    # first we create new hits with the readout without the row information
    # and then merge them into new cells
    rewriteHCalBarrel = RedoSegmentation("ReSegmentationHcal",
                                         # old bitfield (readout)
                                         oldReadoutName=hcalBarrelReadoutName,
                                         # specify which fields are going to be altered (deleted/rewritten)
                                         oldSegmentationIds=["row", "theta", "phi"],
                                         # new bitfield (readout), with new segmentation (merged modules and theta cells)
                                         newReadoutName=hcalBarrelReadoutName2,
                                         OutputLevel=INFO,
                                         debugPrint=200,
                                         inhits=hcalBarrelPositionedCellsName,
                                         outhits="HCalBarrelCellsWithoutRow")

    createHcalBarrelCells2 = CreateCaloCells("CreateHCalBarrelCells2",
                                             doCellCalibration=False,
                                             addCellNoise=False,
                                             filterCellNoise=False,
                                             OutputLevel=INFO,
                                             hits=rewriteHCalBarrel.outhits.Path,
                                             cells=hcalBarrelCellsName2)

    # 4 - attach positions to the new cells
    from Configurables import CellPositionsHCalBarrelPhiThetaSegTool
    hcalBarrelPositionedCellsName2 =  hcalBarrelReadoutName2 + "Positioned"
    cellPositionHcalBarrelTool2 = CellPositionsHCalBarrelPhiThetaSegTool(
        "CellPositionsHCalBarrel2",
        readoutName=hcalBarrelReadoutName2,
        OutputLevel=INFO
    )
    createHcalBarrelPositionedCells2 = CreateCaloCellPositionsFCCee(
        "CreateHCalBarrelPositionedCells2",
        OutputLevel=INFO
    )
    createHcalBarrelPositionedCells2.positionsTool = cellPositionHcalBarrelTool2
    createHcalBarrelPositionedCells2.hits.Path = hcalBarrelCellsName2
    createHcalBarrelPositionedCells2.positionedHits.Path = hcalBarrelPositionedCellsName2

    # Create cells in HCal endcap
    # createHcalEndcapCells = CreateCaloCells("CreateHcalEndcapCaloCells",
    #                                    doCellCalibration=True,
    #                                    calibTool=calibHcalEndcap,
    #                                    addCellNoise=False,
    #                                    filterCellNoise=False,
    #                                    OutputLevel=INFO)
    # createHcalEndcapCells.hits.Path="HCalEndcapHits"
    # createHcalEndcapCells.cells.Path="HCalEndcapCells"

else:
    hcalBarrelCellsName = "emptyCaloCells"
    hcalBarrelPositionedCellsName = "emptyCaloCells"
    hcalBarrelCellsName2 = "emptyCaloCells"
    hcalBarrelPositionedCellsName2 = "emptyCaloCells"
    cellPositionHcalBarrelTool = None
    cellPositionHcalBarrelTool2 = None

# Empty cells for parts of calorimeter not implemented yet
createemptycells = CreateEmptyCaloCellsCollection("CreateEmptyCaloCells")
createemptycells.cells.Path = "emptyCaloCells"

# Produce sliding window clusters
if doSWClustering:
    towers = CaloTowerToolFCCee("towers",
                                deltaThetaTower=4 * 0.009817477 / 4, deltaPhiTower=2 * 2 * pi / 1536.,
                                ecalBarrelReadoutName=ecalBarrelReadoutName,
                                ecalEndcapReadoutName=ecalEndcapReadoutName,
                                ecalFwdReadoutName="",
                                hcalBarrelReadoutName=hcalBarrelReadoutName2,
                                hcalExtBarrelReadoutName="",
                                hcalEndcapReadoutName="",
                                hcalFwdReadoutName="",
                                OutputLevel=INFO)
    towers.ecalBarrelCells.Path = ecalBarrelPositionedCellsName
    towers.ecalEndcapCells.Path = "ECalEndcapCells"
    towers.ecalFwdCells.Path = "emptyCaloCells"
    towers.hcalBarrelCells.Path = hcalBarrelPositionedCellsName2
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

    if applyUpDownstreamCorrections:
        correctCaloClusters = CorrectCaloClusters("correctCaloClusters",
                                                  inClusters=createClusters.clusters.Path,
                                                  outClusters="Corrected" + createClusters.clusters.Path,
                                                  numLayers=[ecalBarrelLayers],
                                                  firstLayerIDs=[0],
                                                  lastLayerIDs=[ecalBarrelLayers-1],
                                                  readoutNames=[ecalBarrelReadoutName],
                                                  upstreamParameters=upstreamParameters,
                                                  upstreamFormulas=[
                                                      ['[0]+[1]/(x-[2])', '[0]+[1]/(x-[2])']],
                                                  downstreamParameters=downstreamParameters,
                                                  downstreamFormulas=[
                                                      ['[0]+[1]*x', '[0]+[1]/sqrt(x)', '[0]+[1]/x']],
                                                  OutputLevel=INFO
                                                  )

    if addShapeParameters:
        augmentCaloClusters = AugmentClustersFCCee("augmentCaloClusters",
                                                   inClusters=createClusters.clusters.Path,
                                                   outClusters="Augmented" + createClusters.clusters.Path,
                                                   systemIDs=[4],
                                                   systemNames=["EMB"],
                                                   numLayers=[ecalBarrelLayers],
                                                   readoutNames=[ecalBarrelReadoutName],
                                                   layerFieldNames=["layer"],
                                                   thetaRecalcWeights=[ecalBarrelThetaWeights],
                                                   do_photon_shapeVar=runPhotonIDTool,
                                                   OutputLevel=INFO
                                                   )

    if applyMVAClusterEnergyCalibration:
        inClusters = ""
        if addShapeParameters:
            inClusters = "Augmented" + createClusters.clusters.Path
        else:
            inClusters = createClusters.clusters.Path

        calibrateCaloClusters = CalibrateCaloClusters("calibrateCaloClusters",
                                                      inClusters=inClusters,
                                                      outClusters="Calibrated" + createClusters.clusters.Path,
                                                      systemIDs=[4],
                                                      systemNames=["EMB"],
                                                      numLayers=[ecalBarrelLayers],
                                                      firstLayerIDs=[0],
                                                      readoutNames=[
                                                          ecalBarrelReadoutName],
                                                      layerFieldNames=["layer"],
                                                      calibrationFile="data/lgbm_calibration-CaloClusters.onnx",
                                                      OutputLevel=INFO
                                                      )

    if runPhotonIDTool:
        if not addShapeParameters:
            print("Photon ID tool cannot be run if shower shape parameters are not calculated")
            runPhotonIDTool = False
        else:
            inClusters = ""
            if applyMVAClusterEnergyCalibration:
                inClusters = calibrateCaloClusters.outClusters.Path
            else:
                inClusters = augmentCaloClusters.outClusters.Path

            photonIDCaloClusters = PhotonIDTool("photonIDCaloClusters",
                                                inClusters=inClusters,
                                                outClusters="PhotonID" + inClusters,
                                                mvaModelFile="data/bdt-photonid-weights-CaloClusters.onnx",
                                                mvaInputsFile="data/bdt-photonid-inputs-CaloClusters.json",
                                                OutputLevel=INFO
                                                )

if doTopoClustering:
    # Produce topoclusters (ECAL only or ECAL+HCAL)
    createTopoInput = CaloTopoClusterInputTool("CreateTopoInput",
                                               ecalBarrelReadoutName=ecalBarrelReadoutName,
                                               ecalEndcapReadoutName="",
                                               ecalFwdReadoutName="",
                                               hcalBarrelReadoutName=hcalBarrelReadoutName2,
                                               hcalExtBarrelReadoutName="",
                                               hcalEndcapReadoutName="",
                                               hcalFwdReadoutName="",
                                               OutputLevel=INFO)

    createTopoInput.ecalBarrelCells.Path = ecalBarrelPositionedCellsName
    createTopoInput.ecalEndcapCells.Path = "emptyCaloCells"
    createTopoInput.ecalFwdCells.Path = "emptyCaloCells"
    createTopoInput.hcalBarrelCells.Path = hcalBarrelPositionedCellsName2
    createTopoInput.hcalExtBarrelCells.Path = "emptyCaloCells"
    createTopoInput.hcalEndcapCells.Path = "emptyCaloCells"
    createTopoInput.hcalFwdCells.Path = "emptyCaloCells"
    cellPositionHcalBarrelNoSegTool = None
    cellPositionHcalExtBarrelTool = None

    neighboursMap = "neighbours_map_ecalB_thetamodulemerged.root"
    noiseMap = "cellNoise_map_electronicsNoiseLevel_ecalB_thetamodulemerged.root"
    if runHCal:
        neighboursMap = "neighbours_map_ecalB_thetamodulemerged_hcalB_thetaphi.root"
        noiseMap = "cellNoise_map_electronicsNoiseLevel_ecalB_thetamodulemerged_hcalB_thetaphi.root"

    readNeighboursMap = TopoCaloNeighbours("ReadNeighboursMap",
                                           fileName=neighboursMap,
                                           OutputLevel=INFO)

    # Noise levels per cell
    readNoisyCellsMap = TopoCaloNoisyCells("ReadNoisyCellsMap",
                                           fileName=noiseMap,
                                           OutputLevel=INFO)

    createTopoClusters = CaloTopoClusterFCCee("CreateTopoClusters",
                                              TopoClusterInput=createTopoInput,
                                              # expects neighbours map from cellid->vec < neighbourIds >
                                              neigboursTool=readNeighboursMap,
                                              # tool to get noise level per cellid
                                              noiseTool=readNoisyCellsMap,
                                              # cell positions tools for all sub - systems
                                              positionsECalBarrelTool=cellPositionEcalBarrelTool,
                                              positionsHCalBarrelTool=cellPositionHcalBarrelTool2,
                                              # positionsHCalBarrelNoSegTool=cellPositionHcalBarrelNoSegTool,
                                              # positionsHCalExtBarrelTool=cellPositionHcalExtBarrelTool,
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


    # Correction below is for EM-only clusters
    # Need something different for EM+HCAL
    if applyUpDownstreamCorrections:
        correctCaloTopoClusters = CorrectCaloClusters(
            "correctCaloTopoClusters",
            inClusters=createTopoClusters.clusters.Path,
            outClusters="Corrected" + createTopoClusters.clusters.Path,
            numLayers=[ecalBarrelLayers],
            firstLayerIDs=[0],
            lastLayerIDs=[ecalBarrelLayers-1],
            readoutNames=[ecalBarrelReadoutName],
            # do not split the following line or it will break scripts that update the values of the corrections
            upstreamParameters=upstreamParameters,
            upstreamFormulas=[['[0]+[1]/(x-[2])', '[0]+[1]/(x-[2])']],
            # do not split the following line or it will break scripts that update the values of the corrections
            downstreamParameters=downstreamParameters,
            downstreamFormulas=[['[0]+[1]*x', '[0]+[1]/sqrt(x)', '[0]+[1]/x']],
            OutputLevel=INFO
        )

    if addShapeParameters:
        augmentCaloTopoClusters = AugmentClustersFCCee("augmentCaloTopoClusters",
                                                       inClusters=createTopoClusters.clusters.Path,
                                                       outClusters="Augmented" + createTopoClusters.clusters.Path,
                                                       systemIDs=[4],
                                                       systemNames=["EMB"],
                                                       numLayers=[ecalBarrelLayers],
                                                       readoutNames=[ecalBarrelReadoutName],
                                                       layerFieldNames=["layer"],
                                                       thetaRecalcWeights=[ecalBarrelThetaWeights],
                                                       do_photon_shapeVar=runPhotonIDTool,
                                                       OutputLevel=INFO)

    if applyMVAClusterEnergyCalibration:
        inClusters = ""
        if addShapeParameters:
            inClusters = "Augmented" + createTopoClusters.clusters.Path
        else:
            inClusters = createTopoClusters.clusters.Path

        calibrateCaloTopoClusters = CalibrateCaloClusters("calibrateCaloTopoClusters",
                                                          inClusters=inClusters,
                                                          outClusters="Calibrated" + createTopoClusters.clusters.Path,
                                                          systemIDs=[4],
                                                          systemNames=["EMB"],
                                                          numLayers=[ecalBarrelLayers],
                                                          firstLayerIDs=[0],
                                                          readoutNames=[
                                                              ecalBarrelReadoutName],
                                                          layerFieldNames=["layer"],
                                                          calibrationFile="data/lgbm_calibration-CaloTopoClusters.onnx",
                                                          OutputLevel=INFO
                                                          )

    if runPhotonIDTool:
        if not addShapeParameters:
            print("Photon ID tool cannot be run if shower shape parameters are not calculated")
            runPhotonIDTool = False
        else:
            inClusters = ""
            if applyMVAClusterEnergyCalibration:
                inClusters = calibrateCaloTopoClusters.outClusters.Path
            else:
                inClusters = augmentCaloTopoClusters.outClusters.Path

            photonIDCaloClusters = PhotonIDTool("photonIDCaloTopoClusters",
                                                inClusters=inClusters,
                                                outClusters="PhotonID" + inClusters,
                                                mvaModelFile="data/bdt-photonid-weights-CaloTopoClusters.onnx",
                                                mvaInputsFile="data/bdt-photonid-inputs-CaloTopoClusters.json",
                                                OutputLevel=INFO
                                                )

# Output
out = PodioOutput("out",
                  OutputLevel=INFO)
out.filename = "ALLEGRO_sim_digi_reco.root"

# drop the unpositioned ECal and HCal barrel and endcap cells
if runHCal:
    out.outputCommands = ["keep *", "drop emptyCaloCells", "drop ECalBarrelCells*", "drop HCalBarrelCells*", "drop %s" % createEcalEndcapCells.cells.Path]
else:
    out.outputCommands = ["keep *", "drop HCal*", "drop emptyCaloCells", "drop ECalBarrelCells*", "drop %s" % createEcalEndcapCells.cells.Path]
out.outputCommands.append("drop %s" % ecalBarrelReadoutName)
out.outputCommands.append("drop %s" % ecalBarrelReadoutName2)
if runHCal:
    out.outputCommands.append("drop %s" % hcalBarrelReadoutName)
    out.outputCommands.append("drop %s" % hcalBarrelPositionedCellsName)
if resegmentECalBarrel:
    out.outputCommands.append("drop ECalBarrelCellsMerged")
    out.outputCommands.append("drop %s" % ecalBarrelCellsName2)

# drop lumi, vertex, DCH, Muons (unless want to keep for event display)
out.outputCommands.append("drop Lumi*")
# out.outputCommands.append("drop Vertex*")
# out.outputCommands.append("drop DriftChamber_simHits*")
out.outputCommands.append("drop MuonTagger*")

# drop hits/positioned cells/cluster cells if desired
if not saveHits:
    out.outputCommands.append("drop %s_contributions" % ecalBarrelReadoutName)
    out.outputCommands.append("drop %s_contributions" % ecalBarrelReadoutName2)
    out.outputCommands.append("drop %s_contributions" % ecalEndcapReadoutName)
if not saveCells:
    out.outputCommands.append("drop %s" % ecalBarrelPositionedCellsName)
    out.outputCommands.append("drop %s" % ecalEndcapReadoutName)
    if resegmentECalBarrel:
        out.outputCommands.append("drop %s" % ecalBarrelPositionedCellsName2)
    if runHCal:
        out.outputCommands.append("drop %s" % hcalBarrelPositionedCellsName2)
if resegmentECalBarrel:
    out.outputCommands.append("drop ECalBarrelCellsMerged")
    out.outputCommands.append("drop %s" % ecalBarrelCellsName2)
if not saveClusterCells:
    out.outputCommands.append("drop Calo*ClusterCells*")

# if we decorate the clusters, we can drop the non-decorated ones
if addShapeParameters:
    out.outputCommands.append("drop %s" % augmentCaloClusters.inClusters)

# CPU information
chra = ChronoAuditor()
audsvc = AuditorSvc()
audsvc.Auditors = [chra]
out.AuditExecute = True

# Event counter
event_counter = EventCounter('event_counter')
event_counter.Frequency = 10

# Configure list of external services
ExtSvc = [geoservice, podioevent, audsvc]
if dumpGDML:
    ExtSvc += [gdmldumpservice]

# Setup alg sequence
TopAlg = [
    event_counter,
    input_reader,
    createEcalBarrelCells,
    createEcalBarrelPositionedCells,
    createEcalEndcapCells
]
createEcalBarrelCells.AuditExecute = True
createEcalBarrelPositionedCells.AuditExecute = True
createEcalEndcapCells.AuditExecute = True

if resegmentECalBarrel:
    TopAlg += [
        resegmentEcalBarrelTool,
        createEcalBarrelCells2,
        createEcalBarrelPositionedCells2,
    ]
    resegmentEcalBarrelTool.AuditExecute = True
    createEcalBarrelCells2.AuditExecute = True
    createEcalBarrelPositionedCells2.AuditExecute = True

if runHCal:
    TopAlg += [
        createHcalBarrelCells,
        createHcalBarrelPositionedCells,
        rewriteHCalBarrel,
        createHcalBarrelCells2,
        createHcalBarrelPositionedCells2,
        # createHcalEndcapCells
    ]
    createHcalBarrelCells.AuditExecute = True
    createHcalBarrelPositionedCells.AuditExecute = True
    rewriteHCalBarrel.AuditExecute = True
    createHcalBarrelCells2.AuditExecute = True
    createHcalBarrelPositionedCells2.AuditExecute = True

if doSWClustering or doTopoClustering:
    TopAlg += [createemptycells]
    createemptycells.AuditExecute = True
    
    if doSWClustering:
        TopAlg += [createClusters]
        createClusters.AuditExecute = True

        if applyUpDownstreamCorrections:
            TopAlg += [correctCaloClusters]
            correctCaloClusters.AuditExecute = True

        if addShapeParameters:
            TopAlg += [augmentCaloClusters]
            augmentCaloClusters.AuditExecute = True

        if applyMVAClusterEnergyCalibration:
            TopAlg += [calibrateCaloClusters]
            calibrateCaloClusters.AuditExecute = True

        if runPhotonIDTool:
            TopAlg += [photonIDCaloClusters]
            photonIDCaloClusters.AuditExecute = True

    if doTopoClustering:
        TopAlg += [createTopoClusters]
        createTopoClusters.AuditExecute = True
        
        if applyUpDownstreamCorrections:
            TopAlg += [correctCaloTopoClusters]
            correctCaloTopoClusters.AuditExecute = True

        if addShapeParameters:
            TopAlg += [augmentCaloTopoClusters]
            augmentCaloTopoClusters.AuditExecute = True

        if applyMVAClusterEnergyCalibration:
            TopAlg += [calibrateCaloTopoClusters]
            calibrateCaloTopoClusters.AuditExecute = True

        if runPhotonIDTool:
            TopAlg += [photonIDCaloTopoClusters]
            photonIDCaloTopoClusters.AuditExecute = True

TopAlg += [
    out
]

ApplicationMgr(
    TopAlg=TopAlg,
    EvtSel='NONE',
    EvtMax=Nevts,
    ExtSvc=ExtSvc,
    StopOnSignal=True,
)
