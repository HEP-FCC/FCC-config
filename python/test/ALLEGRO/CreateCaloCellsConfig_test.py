#!/usr/bin/env python
#
# File: python/test/ALLEGRO/CreateCaloCellsConfig_test.py
# Author: scott snyder <snyder@bnl.gov>
# Date: Jun, 2026
# Purpose: Unit tests for ALLEGRO CreateCaloCellsConfig 
#

import unittest
import os
from FCC_config.ALLEGRO import CreateCaloCellsConfig


compactFile = os.environ.get("K4GEO", "") + "/FCCee/ALLEGRO/compact/ALLEGRO_o1_v03/ALLEGRO_o1_v03.xml"


class Flags:
    pass

class TestCreateCaloCellsConfig (unittest.TestCase):
    def test_defineCaloCellFlags1 (self):
        flags = Flags()
        flags.dataFiles = 'data/'
        CreateCaloCellsConfig.defineCaloCellFlags (flags)

        self.assertEqual (flags.ECal.Barrel.cellsName, 'ECalBarrelModuleThetaMergedPositioned')
        self.assertEqual (flags.ECal.Barrel.linksName, 'ECalBarrelModuleThetaMergedPositionedSimCaloHitLinks')
        self.assertEqual (flags.ECal.Barrel.noisePath, 'data/elecNoise_ecalBarrelFCCee_theta.root')

        self.assertEqual (flags.ECal.Endcap.cellsName, 'ECalEndcapTurbinePositioned')
        self.assertEqual (flags.ECal.Endcap.linksName, 'ECalEndcapTurbinePositionedSimCaloHitLinks')

        self.assertEqual (flags.HCal.Barrel.cellsName, 'HCalBarrelReadoutPositioned')
        self.assertEqual (flags.HCal.Barrel.linksName, 'HCalBarrelReadoutPositionedSimCaloHitLinks')

        self.assertEqual (flags.HCal.Endcap.cellsName, 'HCalEndcapReadoutPositioned')
        self.assertEqual (flags.HCal.Endcap.linksName, 'HCalEndcapReadoutPositionedSimCaloHitLinks')
        return
        

    def test_defineCaloCellFlags2 (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags (None, 'Cells', 'Links')

        self.assertEqual (flags.ECal.Barrel.cellsName, 'ECalBarrelModuleThetaMergedCells')
        self.assertEqual (flags.ECal.Barrel.linksName, 'ECalBarrelModuleThetaMergedCellsLinks')
        self.assertEqual (flags.ECal.Barrel.noisePath, 'elecNoise_ecalBarrelFCCee_theta.root')

        self.assertEqual (flags.ECal.Endcap.cellsName, 'ECalEndcapTurbineCells')
        self.assertEqual (flags.ECal.Endcap.linksName, 'ECalEndcapTurbineCellsLinks')

        self.assertEqual (flags.HCal.Barrel.cellsName, 'HCalBarrelReadoutCells')
        self.assertEqual (flags.HCal.Barrel.linksName, 'HCalBarrelReadoutCellsLinks')

        self.assertEqual (flags.HCal.Endcap.cellsName, 'HCalEndcapReadoutCells')
        self.assertEqual (flags.HCal.Endcap.linksName, 'HCalEndcapReadoutCellsLinks')
        return


    def test_ECalBarrelGeometryTool (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags()
        flags.compactFile = compactFile
        tool = CreateCaloCellsConfig.ECalBarrelGeometryTool (flags)
        self.assertEqual (tool.getFullName(), 'TubeLayerModuleThetaCaloTool/ECalBarrelGeometryTool')
        return
        

    def test_ECalEndcapGeometryTool (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags()
        tool = CreateCaloCellsConfig.ECalEndcapGeometryTool (flags)
        self.assertEqual (tool.getFullName(), 'TurbineEndcapCaloTool/ECalEndcapGeometryTool')
        return
        

    def test_HCalBarrelGeometryTool (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags()
        tool = CreateCaloCellsConfig.HCalBarrelGeometryTool (flags)
        self.assertEqual (tool.getFullName(), 'HCalPhiThetaCaloTool/HCalBarrelGeometryTool')
        return
        

    def test_HCalEndcapGeometryTool (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags()
        tool = CreateCaloCellsConfig.HCalEndcapGeometryTool (flags)
        self.assertEqual (tool.getFullName(), 'HCalPhiThetaCaloTool/HCalEndcapGeometryTool')
        return
        

    def test_CaloCellIndexerSvcCfg (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags()
        flags.compactFile = compactFile
        ca1 = CreateCaloCellsConfig.CaloCellIndexerSvcCfg (flags,
                                                           detectors = ['ECAL_Barrel',
                                                                        'ECAL_Endcap'])
        self.assertEqual (len(ca1.svcs()), 1)
        self.assertEqual (len(ca1.algs()), 0)
        svc1 = ca1.svcs()[0]
        self.assertEqual (svc1.name(), 'k4::recCalo::CaloCellIndexerSvc')
        self.assertEqual (len(svc1.GeoTools), 2)
        self.assertEqual (svc1.GeoTools[0].getFullName(), 'TubeLayerModuleThetaCaloTool/ECalBarrelGeometryTool')
        self.assertEqual (svc1.GeoTools[1].getFullName(), 'TurbineEndcapCaloTool/ECalEndcapGeometryTool')

        ca2 = CreateCaloCellsConfig.CaloCellIndexerSvcCfg (flags,
                                                           detectors = ['ECAL_Barrel',
                                                                        'HCAL_Barrel'])
        self.assertEqual (len(ca2.svcs()), 1)
        self.assertEqual (len(ca2.algs()), 0)
        svc2 = ca2.svcs()[0]
        self.assertEqual (svc2.name(), 'k4::recCalo::CaloCellIndexerSvc')
        self.assertEqual (len(svc2.GeoTools), 2)
        self.assertEqual (svc2.GeoTools[0].getFullName(), 'TubeLayerModuleThetaCaloTool/ECalBarrelGeometryTool')
        self.assertEqual (svc2.GeoTools[1].getFullName(), 'HCalPhiThetaCaloTool/HCalBarrelGeometryTool')

        ca1.merge (ca2)
        self.assertEqual (len(ca1.svcs()), 1)
        self.assertEqual (len(ca1.algs()), 0)
        svc1 = ca1.svcs()[0]
        self.assertEqual (svc1.name(), 'k4::recCalo::CaloCellIndexerSvc')
        self.assertEqual (len(svc1.GeoTools), 3)
        
        self.assertEqual (svc1.GeoTools[0].getFullName(), 'TubeLayerModuleThetaCaloTool/ECalBarrelGeometryTool')
        self.assertEqual (svc1.GeoTools[1].getFullName(), 'TurbineEndcapCaloTool/ECalEndcapGeometryTool')
        self.assertEqual (svc1.GeoTools[2].getFullName(), 'HCalPhiThetaCaloTool/HCalBarrelGeometryTool')
        
        return
        

    def test_CalibrateECalBarrel (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags()
        tool = CreateCaloCellsConfig.CalibrateECalBarrel (flags)
        self.assertEqual (tool.getFullName(), 'CalibrateInLayersTool/CalibrateECalBarrel')
        self.assertEqual (len(tool.samplingFraction), 11)
        return


    def test_CalibrateECalEndcap (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags()
        tool = CreateCaloCellsConfig.CalibrateECalEndcap (flags)
        self.assertEqual (tool.getFullName(), 'CalibrateInLayersTool/CalibrateECalEndcap')
        self.assertEqual (len(tool.samplingFraction), 98)
        return


    def test_CalibrateHCalBarrel (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags()
        tool = CreateCaloCellsConfig.CalibrateHCalBarrel (flags)
        self.assertEqual (tool.getFullName(), 'CalibrateCaloHitsTool/CalibrateHCalBarrel')
        self.assertEqual (tool.invSamplingFraction, 29.4202)
        return


    def test_CalibrateHCalEndcap (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags()
        tool = CreateCaloCellsConfig.CalibrateHCalEndcap (flags)
        self.assertEqual (tool.getFullName(), 'CalibrateCaloHitsTool/CalibrateHCalEndcap')
        self.assertEqual (tool.invSamplingFraction, 29.4202)
        return


    def test_CellPositionsECalBarrel (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags()
        tool = CreateCaloCellsConfig.CellPositionsECalBarrel (flags)
        self.assertEqual (tool.getFullName(), 'CellPositionsECalBarrelModuleThetaSegTool/CellPositionsECalBarrel')
        self.assertEqual (tool.readoutName, flags.ECal.Barrel.readoutName)
        tool2 = CreateCaloCellsConfig.CellPositionsECalBarrel (flags, name='pos_emb', readoutName='ro')
        self.assertEqual (tool2.getFullName(), 'CellPositionsECalBarrelModuleThetaSegTool/pos_emb')
        self.assertEqual (tool2.readoutName, 'ro')
        return


    def test_CellPositionsECalEndcap (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags()
        tool = CreateCaloCellsConfig.CellPositionsECalEndcap (flags)
        self.assertEqual (tool.getFullName(), 'CellPositionsECalEndcapTurbineSegTool/CellPositionsECalEndcap')
        self.assertEqual (tool.readoutName, flags.ECal.Endcap.readoutName)
        tool2 = CreateCaloCellsConfig.CellPositionsECalEndcap (flags, name='pos_emec', readoutName='ro')
        self.assertEqual (tool2.getFullName(), 'CellPositionsECalEndcapTurbineSegTool/pos_emec')
        self.assertEqual (tool2.readoutName, 'ro')
        return


    def test_CellPositionsHCalBarrel (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags()
        tool = CreateCaloCellsConfig.CellPositionsHCalBarrel (flags)
        self.assertEqual (tool.getFullName(), 'CellPositionsHCalPhiThetaSegTool/CellPositionsHCalBarrel')
        self.assertEqual (tool.readoutName, flags.HCal.Barrel.readoutName)
        self.assertEqual (tool.detectorName, 'HCalBarrel')
        tool2 = CreateCaloCellsConfig.CellPositionsHCalBarrel (flags, name='pos_hcalb', readoutName='ro')
        self.assertEqual (tool2.getFullName(), 'CellPositionsHCalPhiThetaSegTool/pos_hcalb')
        self.assertEqual (tool2.readoutName, 'ro')
        return


    def test_CellPositionsHCalEndcap (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags()
        tool = CreateCaloCellsConfig.CellPositionsHCalEndcap (flags)
        self.assertEqual (tool.getFullName(), 'CellPositionsHCalPhiThetaSegTool/CellPositionsHCalEndcap')
        self.assertEqual (tool.readoutName, flags.HCal.Endcap.readoutName)
        self.assertEqual (tool.detectorName, 'HCalThreePartsEndcap')
        tool2 = CreateCaloCellsConfig.CellPositionsHCalEndcap (flags, name='pos_hcale', readoutName='ro')
        self.assertEqual (tool2.getFullName(), 'CellPositionsHCalPhiThetaSegTool/pos_hcale')
        self.assertEqual (tool2.readoutName, 'ro')
        return


    def test_ReadCrosstalkMapECalBarrel (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags()
        flags.compactFile = compactFile
        tool = CreateCaloCellsConfig.ReadCrosstalkMapECalBarrel (flags)
        self.assertEqual (tool.getFullName(), 'ReadCaloCrosstalkMap/ReadCrosstalkMapECalBarrel')
        return


    def test_ECalBarrelNoiseTool (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags()
        tool = CreateCaloCellsConfig.ECalBarrelNoiseTool (flags)
        self.assertEqual (tool.getFullName(), 'NoiseCaloCellsFromFileBarrelTool/ECalBarrelNoiseTool')
        return
        

    def test_ECalEndcapNoiseTool (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags()
        tool = CreateCaloCellsConfig.ECalEndcapNoiseTool (flags)
        self.assertEqual (tool.getFullName(), 'NoiseCaloCellsFromFileTurbineEndcapTool/ECalEndcapNoiseTool')
        return
        

    def test_CreateECalBarrelCellsCfg (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags()
        flags.compactFile = compactFile

        ca = CreateCaloCellsConfig.CreateECalBarrelCellsCfg (flags)
        self.assertEqual (len(ca.svcs()), 1)
        self.assertEqual (len(ca.algs()), 1)
        alg = ca.algs()[0]
        self.assertEqual (alg.getFullName(), 'CreatePositionedCaloCells/CreatePositionedECalBarrelCells')
        self.assertEqual (alg.hits, 'ECalBarrelModuleThetaMerged')
        self.assertEqual (alg.cells, 'ECalBarrelModuleThetaMergedPositioned')
        self.assertEqual (alg.links, 'ECalBarrelModuleThetaMergedPositionedSimCaloHitLinks')
        self.assertEqual (alg.doCellCalibration, True)
        self.assertEqual (alg.addCrosstalk, False)
        self.assertEqual (alg.addCellNoise, False)
        self.assertEqual (alg.filterCellNoise, False)
        self.assertEqual (alg.noiseTool.getFullName(), '')
        self.assertEqual (alg.calibTool.getFullName(), 'CalibrateInLayersTool/CalibrateECalBarrel')
        self.assertEqual (alg.calibTool.readoutName, 'ECalBarrelModuleThetaMerged')
        self.assertEqual (alg.positionsTool.getFullName(), 'CellPositionsECalBarrelModuleThetaSegTool/CellPositionsECalBarrel')
        self.assertEqual (alg.positionsTool.readoutName, 'ECalBarrelModuleThetaMerged')
        svc = ca.svcs()[0]
        self.assertEqual (svc.name(), 'k4::recCalo::CaloCellIndexerSvc')
        self.assertEqual (len(svc.GeoTools), 1)
        self.assertEqual (svc.GeoTools[0].getFullName(), 'TubeLayerModuleThetaCaloTool/ECalBarrelGeometryTool')

        ca = CreateCaloCellsConfig.CreateECalBarrelCellsCfg (flags, name='ecalb_cells2', doCellCalibration=False, hits='ecalb', cellsNameSuffix='2',
                                                             addNoise=True, addCrosstalk=True, filterCellNoise=True)
        self.assertEqual (len(ca.svcs()), 1)
        self.assertEqual (len(ca.algs()), 1)
        alg = ca.algs()[0]
        self.assertEqual (alg.getFullName(), 'CreatePositionedCaloCells/ecalb_cells2')
        self.assertEqual (alg.hits, 'ecalb')
        self.assertEqual (alg.cells, 'ECalBarrelModuleThetaMergedPositioned2')
        self.assertEqual (alg.links, 'ECalBarrelModuleThetaMergedPositioned2SimCaloHitLinks')
        self.assertEqual (alg.doCellCalibration, False)
        self.assertEqual (alg.addCrosstalk, True)
        self.assertEqual (alg.addCellNoise, True)
        self.assertEqual (alg.filterCellNoise, True)
        self.assertEqual (alg.noiseTool.getFullName(), 'NoiseCaloCellsFromFileBarrelTool/ECalBarrelNoiseTool')
        self.assertEqual (alg.calibTool.getFullName(), '')
        self.assertEqual (alg.positionsTool.getFullName(), 'CellPositionsECalBarrelModuleThetaSegTool/CellPositionsECalBarrelModuleThetaMerged')
        self.assertEqual (alg.positionsTool.readoutName, 'ECalBarrelModuleThetaMerged')
        self.assertEqual (alg.crosstalkTool.getFullName(), 'ReadCaloCrosstalkMap/ReadCrosstalkMapECalBarrel')
        self.assertEqual (alg.geometryTool.getFullName(), 'TubeLayerModuleThetaCaloTool/ECalBarrelGeometryTool')
        return


    def test_CreateECalEndcapCellsCfg (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags()

        ca = CreateCaloCellsConfig.CreateECalEndcapCellsCfg (flags)
        self.assertEqual (len(ca.svcs()), 1)
        self.assertEqual (len(ca.algs()), 1)
        alg = ca.algs()[0]
        self.assertEqual (alg.getFullName(), 'CreatePositionedCaloCells/CreatePositionedECalEndcapCells')
        self.assertEqual (alg.hits, 'ECalEndcapTurbine')
        self.assertEqual (alg.cells, 'ECalEndcapTurbinePositioned')
        self.assertEqual (alg.links, 'ECalEndcapTurbinePositionedSimCaloHitLinks')
        self.assertEqual (alg.doCellCalibration, True)
        self.assertEqual (alg.addCrosstalk, False)
        self.assertEqual (alg.addCellNoise, False)
        self.assertEqual (alg.filterCellNoise, False)
        self.assertEqual (alg.noiseTool.getFullName(), '')
        self.assertEqual (alg.calibTool.getFullName(), 'CalibrateInLayersTool/CalibrateECalEndcap')
        self.assertEqual (alg.calibTool.readoutName, 'ECalEndcapTurbine')
        self.assertEqual (alg.positionsTool.getFullName(), 'CellPositionsECalEndcapTurbineSegTool/CellPositionsECalEndcap')
        self.assertEqual (alg.positionsTool.readoutName, 'ECalEndcapTurbine')
        svc = ca.svcs()[0]
        self.assertEqual (svc.name(), 'k4::recCalo::CaloCellIndexerSvc')
        self.assertEqual (len(svc.GeoTools), 1)
        self.assertEqual (svc.GeoTools[0].getFullName(), 'TurbineEndcapCaloTool/ECalEndcapGeometryTool')

        ca = CreateCaloCellsConfig.CreateECalEndcapCellsCfg (flags, name='ecale_cells2', doCellCalibration=False, hits='ecale', cellsNameSuffix='2',
                                                             addNoise=True, filterCellNoise=True)
        self.assertEqual (len(ca.svcs()), 1)
        self.assertEqual (len(ca.algs()), 1)
        alg = ca.algs()[0]
        self.assertEqual (alg.getFullName(), 'CreatePositionedCaloCells/ecale_cells2')
        self.assertEqual (alg.hits, 'ecale')
        self.assertEqual (alg.cells, 'ECalEndcapTurbinePositioned2')
        self.assertEqual (alg.links, 'ECalEndcapTurbinePositioned2SimCaloHitLinks')
        self.assertEqual (alg.doCellCalibration, False)
        self.assertEqual (alg.addCrosstalk, False)
        self.assertEqual (alg.addCellNoise, True)
        self.assertEqual (alg.filterCellNoise, True)
        self.assertEqual (alg.noiseTool.getFullName(), 'NoiseCaloCellsFromFileTurbineEndcapTool/ECalEndcapNoiseTool')
        self.assertEqual (alg.calibTool.getFullName(), '')
        self.assertEqual (alg.positionsTool.getFullName(), 'CellPositionsECalEndcapTurbineSegTool/CellPositionsECalEndcapTurbine')
        self.assertEqual (alg.positionsTool.readoutName, 'ECalEndcapTurbine')
        return


    def test_CreateHCalBarrelCellsCfg (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags()

        ca = CreateCaloCellsConfig.CreateHCalBarrelCellsCfg (flags)
        self.assertEqual (len(ca.svcs()), 1)
        self.assertEqual (len(ca.algs()), 1)
        alg = ca.algs()[0]
        self.assertEqual (alg.getFullName(), 'CreatePositionedCaloCells/CreatePositionedHCalBarrelCells')
        self.assertEqual (alg.hits, 'HCalBarrelReadout')
        self.assertEqual (alg.cells, 'HCalBarrelReadoutPositioned')
        self.assertEqual (alg.links, 'HCalBarrelReadoutPositionedSimCaloHitLinks')
        self.assertEqual (alg.doCellCalibration, True)
        self.assertEqual (alg.addCrosstalk, False)
        self.assertEqual (alg.addCellNoise, False)
        self.assertEqual (alg.filterCellNoise, False)
        self.assertEqual (alg.noiseTool.getFullName(), '')
        self.assertEqual (alg.calibTool.getFullName(), 'CalibrateCaloHitsTool/CalibrateHCalBarrel')
        self.assertEqual (alg.positionsTool.getFullName(), 'CellPositionsHCalPhiThetaSegTool/CellPositionsHCalBarrel')
        self.assertEqual (alg.positionsTool.readoutName, 'HCalBarrelReadout')
        svc = ca.svcs()[0]
        self.assertEqual (svc.name(), 'k4::recCalo::CaloCellIndexerSvc')
        self.assertEqual (len(svc.GeoTools), 1)
        self.assertEqual (svc.GeoTools[0].getFullName(), 'HCalPhiThetaCaloTool/HCalBarrelGeometryTool')

        ca = CreateCaloCellsConfig.CreateHCalBarrelCellsCfg (flags, name='hcalb_cells2', doCellCalibration=False, hits='hcalb', cellsNameSuffix='2')
        self.assertEqual (len(ca.svcs()), 1)
        self.assertEqual (len(ca.algs()), 1)
        alg = ca.algs()[0]
        self.assertEqual (alg.getFullName(), 'CreatePositionedCaloCells/hcalb_cells2')
        self.assertEqual (alg.hits, 'hcalb')
        self.assertEqual (alg.cells, 'hcalbPositioned2')
        self.assertEqual (alg.links, 'hcalbPositioned2SimCaloHitLinks')
        self.assertEqual (alg.doCellCalibration, False)
        self.assertEqual (alg.addCrosstalk, False)
        self.assertEqual (alg.addCellNoise, False)
        self.assertEqual (alg.filterCellNoise, False)
        self.assertEqual (alg.noiseTool.getFullName(), '')
        self.assertEqual (alg.calibTool.getFullName(), '')
        self.assertEqual (alg.positionsTool.getFullName(), 'CellPositionsHCalPhiThetaSegTool/CellPositionsHCalBarrel')
        self.assertEqual (alg.positionsTool.readoutName, 'HCalBarrelReadout')
        return


    def test_CreateHCalEndcapCellsCfg (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags()

        ca = CreateCaloCellsConfig.CreateHCalEndcapCellsCfg (flags)
        self.assertEqual (len(ca.svcs()), 1)
        self.assertEqual (len(ca.algs()), 1)
        alg = ca.algs()[0]
        self.assertEqual (alg.getFullName(), 'CreatePositionedCaloCells/CreatePositionedHCalEndcapCells')
        self.assertEqual (alg.hits, 'HCalEndcapReadout')
        self.assertEqual (alg.cells, 'HCalEndcapReadoutPositioned')
        self.assertEqual (alg.links, 'HCalEndcapReadoutPositionedSimCaloHitLinks')
        self.assertEqual (alg.doCellCalibration, True)
        self.assertEqual (alg.addCrosstalk, False)
        self.assertEqual (alg.addCellNoise, False)
        self.assertEqual (alg.filterCellNoise, False)
        self.assertEqual (alg.noiseTool.getFullName(), '')
        self.assertEqual (alg.calibTool.getFullName(), 'CalibrateCaloHitsTool/CalibrateHCalEndcap')
        self.assertEqual (alg.positionsTool.getFullName(), 'CellPositionsHCalPhiThetaSegTool/CellPositionsHCalEndcap')
        self.assertEqual (alg.positionsTool.readoutName, 'HCalEndcapReadout')
        svc = ca.svcs()[0]
        self.assertEqual (svc.name(), 'k4::recCalo::CaloCellIndexerSvc')
        self.assertEqual (len(svc.GeoTools), 1)
        self.assertEqual (svc.GeoTools[0].getFullName(), 'HCalPhiThetaCaloTool/HCalEndcapGeometryTool')

        ca = CreateCaloCellsConfig.CreateHCalEndcapCellsCfg (flags, name='hcale_cells2', doCellCalibration=False, hits='hcale', cellsNameSuffix='2')
        self.assertEqual (len(ca.svcs()), 1)
        self.assertEqual (len(ca.algs()), 1)
        alg = ca.algs()[0]
        self.assertEqual (alg.getFullName(), 'CreatePositionedCaloCells/hcale_cells2')
        self.assertEqual (alg.hits, 'hcale')
        self.assertEqual (alg.cells, 'hcalePositioned2')
        self.assertEqual (alg.links, 'hcalePositioned2SimCaloHitLinks')
        self.assertEqual (alg.doCellCalibration, False)
        self.assertEqual (alg.addCrosstalk, False)
        self.assertEqual (alg.addCellNoise, False)
        self.assertEqual (alg.filterCellNoise, False)
        self.assertEqual (alg.noiseTool.getFullName(), '')
        self.assertEqual (alg.calibTool.getFullName(), '')
        self.assertEqual (alg.positionsTool.getFullName(), 'CellPositionsHCalPhiThetaSegTool/CellPositionsHCalEndcap')
        self.assertEqual (alg.positionsTool.readoutName, 'HCalEndcapReadout')
        return
        

    def test_ReSegmentationECalBarrelCfg (self):
        flags = CreateCaloCellsConfig.defineCaloCellFlags()

        ca = CreateCaloCellsConfig.ReSegmentationECalBarrelCfg (flags)
        self.assertEqual (len(ca.svcs()), 0)
        self.assertEqual (len(ca.algs()), 1)
        alg = ca.algs()[0]
        self.assertEqual (alg.getFullName(), 'RedoSegmentation/ReSegmentationEcal')
        self.assertEqual (alg.oldReadoutName, 'ECalBarrelModuleThetaMerged')
        self.assertEqual (alg.newReadoutName, 'ECalBarrelModuleThetaMerged2')
        self.assertEqual (alg.inhits.Path, 'ECalBarrelModuleThetaMergedPositioned')
        self.assertEqual (alg.outhits.Path, 'ECalBarrelCellsMerged')
        self.assertEqual (alg.oldSegmentationIds, ['module', 'theta'])
        return


if __name__ == '__main__':
    unittest.main()
