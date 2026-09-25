#
# File: python/FCC_config/ALLEGRO/CreateCaloCellsConfig.py
# Author: scott snyder <snyder@bnl.gov>
# Date: Jun, 2026
# Purpose: ALLEGRO job configuration functions for creating calorimeter cells.
#
# ComponentAccumulator style configuration functions for ALLEGRO calorimeter
# cell making.
#
# Here is an example of using these to configure cell reconstruction for
# both ECal and HCAL with default parameters:
#
#    class Flags:
#        pass
#    flags = Flags()
#    flags.compactFile = os.environ.get("K4GEO", "") + "/FCCee/ALLEGRO/compact/ALLEGRO_o1_v03/ALLEGRO_o1_v03.xml"
#    from FCC_config.ALLEGRO.CreateCaloCellsConfig import defineCaloCellFlags
#    defineCaloCellFlags(flags)
#
#    from FCC_config.ComponentAccumulator import ComponentAccumulator
#    caldigi_cfg = ComponentAccumulator()
#    from FCC_config.ALLEGRO.CreateCaloCellsConfig import \
#      CreateECalBarrelCellsCfg, CreateECalBarrelCellsCfg, \
#      CreateHCalBarrelCellsCfg, CreateHCalEndcapCellsCfg
#    caldigi_cfg.merge(CreateECalBarrelCellsCfg(flags))
#    caldigi_cfg.merge(CreateECalEndcapCellsCfg(flags))
#    caldigi_cfg.merge(CreateHCalBarrelCellsCfg(flags))
#    caldigi_cfg.merge(CreateHCalEndcapCellsCfg(flags))
#
#    caldigi_cfg.toVars (TopAlg, ExtSvc)
#
# The behavior can be changed via arguments to the above functions.
# For example, to enable noise and crosstalk:
#
#    caldigi_cfg.merge(CreateECalBarrelCellsCfg(flags,
#                                               name = 'ECalCellsWithNoise',
#                                               addNoise = True,
#                                               addCrosstalk = True,
#                                               cellsNameSuffix = 'WithNoise'))
#
# Some defaults can also be overridden via the flags object.
# See the code for details.
#


from FCC_config.ComponentAccumulator import ComponentAccumulator
import Configurables as C
from FCC_config.DetIDs import detIDs


# ECAL barrel parameters for digitization
ecalBarrelLayers = 11

# e-, 10 GeV, flat theta, B field off
# ecalBarrelSamplingFraction = [0.3800493723322256,  #  0
#                               0.13494147915064658, #  1
#                               0.142866851721152,   #  2
#                               0.14839315921940666, #  3
#                               0.15298362570665006, #  4
#                               0.15709704561942747, #  5
#                               0.16063717490147533, #  6
#                               0.1641723795419055,  #  7
#                               0.16845490287689746, #  8
#                               0.17111520115997653, #  9
#                               0.1730605163148862,  # 10
#                               ]

#  e-, 20 GeV, flat theta, B field on; LAr+Pb
ecalBarrelSamplingFraction = [0.3790943904011486,  #  0
                              0.1355600584387894,  #  1
                              0.14628210607758893, #  2
                              0.15274136994224854, #  3
                              0.15817255837886351, #  4
                              0.16290355087527258, #  5
                              0.1674201708055751,  #  6
                              0.1715846423182708,  #  7
                              0.17558662106635545, #  8
                              0.18002243792463576, #  9
                              0.18288329976007917, # 10
                              ]

# LKr+W
# ecalBarrelSamplingFraction = [0.4806159038189229,  #  0
#                               0.2822724529941907,  #  1
#                               0.29324811578621524, #  2
#                               0.2996356722403102,  #  3
#                               0.3047116566166906,  #  4
#                               0.3090324459212472,  #  5
#                               0.3133282052725273,  #  6
#                               0.3173868504112048,  #  7
#                               0.3215311396527887,  #  8
#                               0.32516920330802673, #  9
#                               0.3318488881234955,  # 10
#                               ]

ecalBarrelUpstreamParameters = [[0.028158491043365624,
                                 -1.564259408365951,
                                 -76.52312805346982,
                                 0.7442903558010191,
                                 -34.894692961350195,
                                 -74.19340877431723]]
ecalBarrelDownstreamParameters = [[0.00010587711361028165,
                                   0.0052371999097777355,
                                   0.69906696456064,
                                   -0.9348243433360095,
                                   -0.0364714212117143,
                                   8.360401126995626]]


if ecalBarrelSamplingFraction and len(ecalBarrelSamplingFraction) > 0:
    assert (ecalBarrelLayers == len(ecalBarrelSamplingFraction))


# ECAL endcap parameters for digitization
ecalEndcapWheels = 3

# the turbine endcap has calibration "layers" in the both the z and radial
# directions, for each of the three wheels.  So the total number of layers
# is given by:
#
#   ECalEndcapNumCalibZLayersWheel1*ECalEndcapNumCalibRhoLayersWheel1
#  +ECalEndcapNumCalibZLayersWheel2*ECalEndcapNumCalibRhoLayersWheel2
#  +ECalEndcapNumCalibZLayersWheel3*ECalEndcapNumCalibRhoLayersWheel3
#
# which in the current design is 5*10+1*14+1*34 = 98
# NB some cells near the inner and outer edges of the calorimeter are difficult
# to calibrate as they are not part of the core of well-contained showers.
# The calibrated values can be <0 or >1 for such cells, so these nonsensical
# numbers are replaced by 1
ecalEndcapLayers = 98
ecalEndcapSamplingFraction = [
    0.0897818,  0.221318,   0.0820002, 0.994281, 0.0414437, # 0  wheel 1 zlay 0
    0.1148,     0.178831,   0.142449,  0.181206, 0.342843,  # 5
    0.137479,   0.176479,   0.153273,  0.195836, 0.0780405, # 10 wheel 1 zlay 1
    0.150202,   0.17846,    0.164886,  0.175758, 0.10836,   # 15
    0.160243,   0.183373,   0.171818,  0.194848, 0.111899,  # 20 wheel 1 zlay 2
    0.170704,   0.188455,   0.178164,  0.209113, 0.105241,  # 25
    0.180637,   0.192206,   0.186096,  0.211962, 0.112019,  # 30 wheel 1 zlay 3
    0.180344,   0.195684,   0.190778,  0.218259, 0.118516,  # 35
    0.207786,   0.204474,   0.207048,  0.225913, 0.111325,  # 40 wheel 1 zlay 4
    0.147875,   0.195625,   0.173326,  0.175449, 0.104087,  # 45
    0.153645,   0.161263,   0.165499,  0.171758, 0.175789,  # 50 wheel 2
    0.180657,   0.184563,   0.187876,  0.191762, 0.19426,   # 55
    0.197959,   0.199021,   0.204428,  0.195709,            # 60
    0.151751,   0.171477,   0.165509,  0.172565, 0.172961,  # 64 wheel 3
    0.175534,   0.177989,   0.18026,   0.181898, 0.183912,  # 69
    0.185654,   0.187515,   0.190408,  0.188794, 0.193699,  # 74
    0.192287,   0.19755,    0.190943,  0.218553, 0.161085,  # 79
    0.373086,   0.122495,   0.21103,   1,        0.138686,  # 84
    0.0545171,  1,          1,         0.227945, 0.0122872, # 89
    0.00437334, 0.00363533, 1,         1,                   # 94
    ]
if ecalEndcapSamplingFraction and len(ecalEndcapSamplingFraction) > 0:
    assert (ecalEndcapLayers == len(ecalEndcapSamplingFraction))


hcalBarrelLayers = 13
hcalEndcapLayers = 22

    
def ECalBarrelGeometryTool (flags, name = 'ECalBarrelGeometryTool',
                            readoutName = None):
    """Return calorimeter tool for ECal barrel.

Use the default readout if readoutName is not supplied."""

    if readoutName is None: readoutName = flags.ECal.Barrel.readoutName
    return C.TubeLayerModuleThetaCaloTool(name,
                                          readoutName=readoutName,
                                          activeVolumeName="LAr_sensitive",
                                          activeFieldName="layer",
                                          activeVolumesNumber=ecalBarrelLayers,
                                          fieldNames=["system"],
                                          fieldValues=[detIDs(flags, 'ECAL_Barrel')],
                                          )


def ECalEndcapGeometryTool (flags, name = 'ECalEndcapGeometryTool',
                            readoutName = None):
    """Return calorimeter tool for ECal endcap.

Use the default readout if readoutName is not supplied."""
    
    if readoutName is None: readoutName = flags.ECal.Endcap.readoutName
    return C.TurbineEndcapCaloTool (name,
                                    readoutName=readoutName)


def HCalBarrelGeometryTool (flags, name = 'HCalBarrelGeometryTool',
                            readoutName = None):
    """Return calorimeter tool for HCal barrel.

Use the default readout if readoutName is not supplied."""
    
    if readoutName is None: readoutName = flags.HCal.Barrel.readoutName
    return C.HCalPhiThetaCaloTool(name,
                                  readoutName=readoutName)


def HCalEndcapGeometryTool (flags, name = 'HCalEndcapGeometryTool',
                            readoutName = None):
    """Return calorimeter tool for HCal endcap.

Use the default readout if readoutName is not supplied."""
    
    if readoutName is None: readoutName = flags.HCal.Endcap.readoutName
    return C.HCalPhiThetaCaloTool(name,
                                  readoutName=readoutName)


class CaloCellIndexerSvc:
    """Helper to handle merging of CaloCellIndexerSvc."""
    def __init__ (self, name, GeoTools = []):
        self._name = name
        self.GeoTools = GeoTools
        return
    def name (self):
        return self._name

    def mergeTo (self, old):
        if not isinstance (old, CaloCellIndexerSvc): return False
        oldnames = [x.name() for x in old.GeoTools]
        for tool in self.GeoTools:
            if tool.name() not in oldnames:
                old.GeoTools.append (tool)
        return True

    def convertTo (self):
        return C.k4__recCalo__CaloCellIndexerSvc (self.name(),
                                                  GeoTools = self.GeoTools)


def CaloCellIndexerSvcCfg (flags,
                           name = 'k4::recCalo::CaloCellIndexerSvc',
                           detectors = [],
                           tools = []):
    """Return CA for an indexer service for a given set of geometry tools.

The detectors argument is a list of subdirectory names for which to create
geometry tools.  Any explicitly given by the tools argument will also be
added.
"""
    _geometry_tools = {
        'ECAL_Barrel' : ECalBarrelGeometryTool,
        'ECAL_Endcap' : ECalEndcapGeometryTool,
        'HCAL_Barrel' : HCalBarrelGeometryTool,
        'HCAL_Endcap' : HCalEndcapGeometryTool,
    }
    cfg = ComponentAccumulator()
    tools = tools[:]
    for d in detectors:
        tools.append (_geometry_tools[d](flags))
    svc = CaloCellIndexerSvc (name, GeoTools = tools)
    cfg.addSvc (svc)
    return cfg


def CalibrateECalBarrel (flags, name = 'CalibrateECalBarrel'):
    """Return tool to calibrate ECal barrel cells."""
    return C.CalibrateInLayersTool(name,
                                   samplingFraction=ecalBarrelSamplingFraction,
                                   readoutName=flags.ECal.Barrel.readoutName,
                                   layerFieldName="layer")


def CalibrateECalEndcap (flags, name = 'CalibrateECalEndcap'):
    """Return tool to calibrate ECal endcap cells."""
    return C.CalibrateInLayersTool(name,
                                   samplingFraction=ecalEndcapSamplingFraction,
                                   readoutName=flags.ECal.Endcap.readoutName,
                                   layerFieldName="layer")


def CalibrateHCalBarrel (flags, name = 'CalibrateHCalBarrel'):
    """Return tool to calibrate HCal barrel cells."""
    return C.CalibrateCaloHitsTool(name,
                                   invSamplingFraction=29.4202)


def CalibrateHCalEndcap (flags, name = 'CalibrateHCalEndcap'):
    """Return tool to calibrate HCal endcap cells."""
    return C.CalibrateCaloHitsTool(name,
                                   invSamplingFraction=29.4202)  # FIXME: to be updated for ddsim


def CellPositionsECalBarrel (flags,
                             name = 'CellPositionsECalBarrel',
                             readoutName = None):
    """Return tool to calculate cell positions for ECal barrel."""
    if readoutName is None: readoutName = flags.ECal.Barrel.readoutName
    return C.CellPositionsECalBarrelModuleThetaSegTool(name,
                                                       readoutName=readoutName)


def CellPositionsECalEndcap (flags,
                             name = 'CellPositionsECalEndcap',
                             readoutName = None):
    """Return tool to calculate cell positions for ECal endcap."""
    if readoutName is None: readoutName = flags.ECal.Endcap.readoutName
    return C.CellPositionsECalEndcapTurbineSegTool(name,
                                                   readoutName=readoutName)


def CellPositionsHCalBarrel (flags,
                             name = 'CellPositionsHCalBarrel',
                             readoutName = None):
    """Return tool to calculate cell positions for HCal barrel."""
    if readoutName is None: readoutName = flags.HCal.Barrel.readoutName
    return C.CellPositionsHCalPhiThetaSegTool(name,
                                              readoutName=readoutName,
                                              detectorName='HCalBarrel')


def CellPositionsHCalEndcap (flags,
                             name = 'CellPositionsHCalEndcap',
                             readoutName = None):
    """Return tool to calculate cell positions for HCal endcap."""
    if readoutName is None: readoutName = flags.HCal.Endcap.readoutName
    return C.CellPositionsHCalPhiThetaSegTool(name,
                                              readoutName=readoutName,
                                              detectorName='HCalThreePartsEndcap',
                                              numLayersHCalThreeParts=[6, 9, 22])


def ReadCrosstalkMapECalBarrel (flags, name = 'ReadCrosstalkMapECalBarrel'):
    """Return crosstalk tool for ECal barrel"""
    return C.ReadCaloCrosstalkMap(name,
                                  #detID = detIDs(flags, 'ECAL_Barrel'),
                                  fileName = flags.ECal.Barrel.xtalkPath)


def ECalBarrelNoiseTool (flags, name = 'ECalBarrelNoiseTool'):
    """Return noise tool for ECal barrel."""
    return C.NoiseCaloCellsFromFileBarrelTool (name,
                                               cellPositionsTool=CellPositionsECalBarrel(flags),
                                               readoutName=flags.ECal.Barrel.readoutName,
                                               noiseFileName=flags.ECal.Barrel.noisePath,
                                               elecNoiseRMSHistoName=flags.ECal.Barrel.noiseRMSHistName,
                                               setNoiseOffset=False,
                                               activeFieldName="layer",
                                               addPileup=False,
                                               filterNoiseThreshold=flags.ECal.Barrel.filterNoiseThreshold,
                                               useAbsInFilter=True,
                                               numHistograms=ecalBarrelLayers,
                                               scaleFactor=1 / 1000.,  # MeV to GeV
                                               )


def ECalEndcapNoiseTool (flags, name = 'ECalEndcapNoiseTool'):
    """Return noise tool for ECal endcap."""
    return C.NoiseCaloCellsFromFileTurbineEndcapTool (name,
                                                      cellPositionsTool=CellPositionsECalEndcap(flags),
                                                      readoutName=flags.ECal.Endcap.readoutName,
                                                      noiseFileName=flags.ECal.Endcap.noisePath,
                                                      elecNoiseRMSHistoName=flags.ECal.Endcap.noiseRMSHistName,
                                                      setNoiseOffset=False,
                                                      activeFieldName="wheel",
                                                      addPileup=False,
                                                      filterNoiseThreshold=flags.ECal.Endcap.filterNoiseThreshold,
                                                      useAbsInFilter=True,
                                                      numHistograms=ecalEndcapWheels, # 3 wheels
                                                      scaleFactor=1 / 1000.,  # MeV to GeV
                                               )


def CreateECalBarrelCellsCfg (flags,
                              name = 'CreatePositionedECalBarrelCells',
                              doCellCalibration = True,
                              addNoise = False,
                              addCrosstalk = None,
                              filterCellNoise = False,
                              cellsNameSuffix = '',
                              hits = None,
                              readoutName = None,
                              alg = C.CreatePositionedCaloCells,
                              **kw):
    """Return a CA for creating ECal barrel cells.

doCellCalibration controls whether sampling-faction calibration is applied.
addNoise and addCrosstalk control the addition of noise and crosstalk,
while filterCellNoise enables filtering cells with small energy.
Hits are taken from the container given by the hits argumnent, defaulting
to the ECal barrel readout name if not supplied.
If cellsNameSuffix is specified, this will be added to the end of the
output cell container.
The readout name may be overridden using the readoutName argument.
Passing alg allows overriding the algorithm type used for the reconstruction.
"""

    cfg = ComponentAccumulator()
    cfg.merge (CaloCellIndexerSvcCfg (flags, detectors = ['ECAL_Barrel']))
    if hits is None: hits = flags.ECal.Barrel.readoutName
    if readoutName is None: readoutName = flags.ECal.Barrel.readoutName
    if addCrosstalk is None: addCrosstalk = flags.ECal.Barrel.addCrosstalk

    kw.setdefault('cells', readoutName + flags.cellsNamePart + cellsNameSuffix)
    kw.setdefault('links', kw['cells'] + flags.linksNamePart)

    kw.setdefault('calibTool', CalibrateECalBarrel(flags) if doCellCalibration else None)
    if addCrosstalk:
        kw['crosstalkTool'] = ReadCrosstalkMapECalBarrel(flags)
    else:
        kw['crosstalkTool'] = None
       
    kw.setdefault('crosstalkTool', ReadCrosstalkMapECalBarrel(flags) if addCrosstalk else None)
    kw.setdefault('noiseTool', ECalBarrelNoiseTool(flags) if addNoise else None)
    kw.setdefault('geometryTool', ECalBarrelGeometryTool(flags) if addNoise else None)

    if hits == flags.ECal.Barrel.readoutName:
        kw['positionsTool'] = CellPositionsECalBarrel(flags)
    else:
        kw['positionsTool'] = CellPositionsECalBarrel(flags,
                                                      name='CellPositions' + readoutName,
                                                      readoutName=readoutName)

    cfg.addAlg(alg(name,
                   hits=hits,
                   doCellCalibration=doCellCalibration,
                   addCrosstalk=addCrosstalk,
                   addCellNoise=addNoise,
                   filterCellNoise=filterCellNoise,
                   **kw
                   ))
    return cfg
                           

def CreateECalEndcapCellsCfg (flags,
                              name = 'CreatePositionedECalEndcapCells',
                              doCellCalibration = True,
                              addNoise = False,
                              filterCellNoise = False,
                              cellsNameSuffix = '',
                              hits = None,
                              readoutName = None,
                              alg = C.CreatePositionedCaloCells,
                              **kw):
    """Return a CA for creating ECal endcap cells.

doCellCalibration controls whether sampling-faction calibration is applied.
Hits are taken from the container given by the hits argumnent, defaulting
to the ECal endcap readout name if not supplied.
If cellsNameSuffix is specified, this will be added to the end of the
output cell container.
Passing alg allows overriding the algorithm type used for the reconstruction.
"""
    cfg = ComponentAccumulator()
    cfg.merge (CaloCellIndexerSvcCfg (flags, detectors = ['ECAL_Endcap']))
    if readoutName is None: readoutName = flags.ECal.Endcap.readoutName
    if hits is None: hits = flags.ECal.Endcap.readoutName

    kw.setdefault('cells', readoutName + flags.cellsNamePart + cellsNameSuffix)
    kw.setdefault('links', kw['cells'] + flags.linksNamePart)

    kw.setdefault('noiseTool', ECalEndcapNoiseTool(flags) if addNoise else None)
    kw.setdefault('geometryTool', ECalEndcapGeometryTool(flags) if addNoise else None)

    kw.setdefault('calibTool', CalibrateECalEndcap(flags) if doCellCalibration else None)

    if hits == flags.ECal.Endcap.readoutName:
        kw['positionsTool'] = CellPositionsECalEndcap(flags)
    else:
        kw['positionsTool'] = CellPositionsECalEndcap(flags,
                                                      name='CellPositions' + readoutName,
                                                      readoutName=readoutName)

    cfg.addAlg(alg(name,
                   hits=hits,
                   doCellCalibration=doCellCalibration,
                   addCellNoise=addNoise,
                   addCrosstalk=False,
                   filterCellNoise=filterCellNoise,
                   crosstalkTool=None,
                   **kw
                   ))

    return cfg


def CreateHCalBarrelCellsCfg (flags,
                              name = 'CreatePositionedHCalBarrelCells',
                              doCellCalibration = True,
                              cellsNameSuffix = '',
                              hits = None,
                              alg = C.CreatePositionedCaloCells,
                              **kw):
    """Return a CA for creating HCal barrel cells.

doCellCalibration controls whether sampling-faction calibration is applied.
Hits are taken from the container given by the hits argumnent, defaulting
to the HCal barrel readout name if not supplied.
If cellsNameSuffix is specified, this will be added to the end of the
output cell container.
Passing alg allows overriding the algorithm type used for the reconstruction.
"""
    cfg = ComponentAccumulator()
    cfg.merge (CaloCellIndexerSvcCfg (flags, detectors = ['HCAL_Barrel']))
    if hits is None: hits = flags.HCal.Barrel.readoutName

    kw.setdefault('cells', hits + flags.cellsNamePart + cellsNameSuffix)
    kw.setdefault('links', kw['cells'] + flags.linksNamePart)

    kw.setdefault('calibTool', CalibrateHCalBarrel(flags) if doCellCalibration else None)

    cfg.addAlg(alg(name,
                   hits=hits,
                   doCellCalibration=doCellCalibration,
                   positionsTool=CellPositionsHCalBarrel(flags),
                   addCellNoise=False,
                   noiseTool=None,
                   addCrosstalk=False,
                   filterCellNoise=False,
                   crosstalkTool=None,
                   **kw
                   ))
    return cfg


def CreateHCalEndcapCellsCfg (flags,
                              name = 'CreatePositionedHCalEndcapCells',
                              doCellCalibration = True,
                              cellsNameSuffix = '',
                              hits = None,
                              alg = C.CreatePositionedCaloCells,
                              **kw):
    """Return a CA for creating HCal endcap cells.

doCellCalibration controls whether sampling-faction calibration is applied.
Hits are taken from the container given by the hits argumnent, defaulting
to the HCal endcap readout name if not supplied.
If cellsNameSuffix is specified, this will be added to the end of the
output cell container.
Passing alg allows overriding the algorithm type used for the reconstruction.
"""
    cfg = ComponentAccumulator()
    cfg.merge (CaloCellIndexerSvcCfg (flags, detectors = ['HCAL_Endcap']))
    if hits is None: hits = flags.HCal.Endcap.readoutName

    kw.setdefault('cells', hits + flags.cellsNamePart + cellsNameSuffix)
    kw.setdefault('links', kw['cells'] + flags.linksNamePart)

    kw.setdefault('calibTool', CalibrateHCalEndcap(flags) if doCellCalibration else None)

    cfg.addAlg(alg(name,
                   hits=hits,
                   doCellCalibration=doCellCalibration,
                   positionsTool=CellPositionsHCalEndcap(flags),
                   addCellNoise=False,
                   noiseTool=None,
                   addCrosstalk=False,
                   filterCellNoise=False,
                   crosstalkTool=None,
                   **kw
                   ))
    return cfg


                           
def ReSegmentationECalBarrelCfg(flags,
                                name = 'ReSegmentationEcal',
                                newReadoutName = 'ECalBarrelModuleThetaMerged2',
                                newCellsName = 'ECalBarrelCellsMerged'):
    """Rewrite ECal barrel cells with a new segmentation."""

    cfg = ComponentAccumulator()
    cfg.addAlg(C.RedoSegmentation(name,
                                  # old bitfield (readout)
                                  oldReadoutName=flags.ECal.Barrel.readoutName,
                                  # specify which fields are going to be altered (deleted/rewritten)
                                  oldSegmentationIds=['module', 'theta'],
                                  # new bitfield (readout), with new segmentation (merged modules and theta cells)
                                  newReadoutName=newReadoutName,
                                  debugPrint=200,
                                  inhits=flags.ECal.Barrel.readoutName + flags.cellsNamePart,
                                  outhits=newCellsName))
    return cfg



class Flags:
    """Dummy class to hold configuration flags."""
    pass


def defineCaloCellFlags(flags = None,
                        cellsNamePart = 'Positioned',
                        linksNamePart = 'SimCaloHitLinks'):
    """Define configuration flags for calorimeter cell reconstruction.

    If a top-level flags object is given as the first argument,
    flags will be added to it.  Otherwise, a new top-level flags
    object will be created.  In any case, the top-level flags
    are returned.

    cellsNamePart is a suffix to add to the readout name to get the
    cell container names; linksNamePart is a suffix added to the cell
    container names to get the link names.

    If defined, flags.dataFiles is used as the path to data files.

    Creates flags sub-objects ECal.Barrel, ECal.Endcap, HCal.Barrel, HCal.Endcap.
    """

    # Create top-level object if not provided.
    if flags is None:
        flags = Flags()

    # Container name suffixes.
    flags.cellsNamePart = cellsNamePart
    flags.linksNamePart = linksNamePart

    # dataFiles defaults to null.
    dataFiles = getattr (flags, 'dataFiles', '')

    flags.ECal = Flags()
    flags.HCal = Flags()

    # ECal barrel
    flags.ECal.Barrel = Flags()
    flags.ECal.Barrel.readoutName = 'ECalBarrelModuleThetaMerged'      # barrel, original segmentation (baseline)
    flags.ECal.Barrel.cellsName = flags.ECal.Barrel.readoutName + flags.cellsNamePart
    flags.ECal.Barrel.linksName = flags.ECal.Barrel.cellsName + flags.linksNamePart
    flags.ECal.Barrel.addCrosstalk = False
    flags.ECal.Barrel.noisePath = dataFiles + "elecNoise_ecalBarrelFCCee_theta.root"
    flags.ECal.Barrel.xtalkPath = dataFiles + "xtalk_neighbours_map_ecalB_thetamodulemerged.root"
    flags.ECal.Barrel.noiseRMSHistName = 'h_elecNoise_fcc_'
    flags.ECal.Barrel.filterNoiseThreshold = -1

    # ECal endcap
    flags.ECal.Endcap = Flags()
    flags.ECal.Endcap.readoutName = 'ECalEndcapTurbine'                # endcap, turbine-like (baseline)
    flags.ECal.Endcap.cellsName = flags.ECal.Endcap.readoutName + flags.cellsNamePart
    flags.ECal.Endcap.linksName = flags.ECal.Endcap.cellsName + flags.linksNamePart
    flags.ECal.Endcap.noisePath = dataFiles + "elecNoise_ecalendcap.root"
    flags.ECal.Endcap.noiseRMSHistName = 'noise_endcap_wheel'
    flags.ECal.Endcap.filterNoiseThreshold = -1

    # HCal barrel
    flags.HCal.Barrel = Flags()
    flags.HCal.Barrel.readoutName = 'HCalBarrelReadout'            # barrel, original segmentation (phi-theta)
    #flags.HCal.Barrel.readoutName = 'HCalBarrelReadoutPhiRow'    # barrel, alternative segmentation (phi-row)
    flags.HCal.Barrel.cellsName = flags.HCal.Barrel.readoutName + flags.cellsNamePart
    flags.HCal.Barrel.linksName = flags.HCal.Barrel.cellsName + flags.linksNamePart

    # HCal endcap
    flags.HCal.Endcap = Flags()
    flags.HCal.Endcap.readoutName = 'HCalEndcapReadout'            # endcap, original segmentation
    #flags.HCal.Endcap.readoutName = 'HCalEndcapReadoutPhiRow'    # endcap, alternative segmentation (phi-row)
    flags.HCal.Endcap.cellsName = flags.HCal.Endcap.readoutName + flags.cellsNamePart
    flags.HCal.Endcap.linksName = flags.HCal.Endcap.cellsName + flags.linksNamePart

    return flags

    
