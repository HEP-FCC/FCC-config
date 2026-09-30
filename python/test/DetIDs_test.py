#!/usr/bin/env python
#
# File: python/test/DetIDs_test.py
# Author: scott snyder <snyder@bnl.gov>
# Date: Jun, 2026
# Purpose: Unit tests for DetIDs
#

import unittest
import os
from FCC_config.DetIDs import detIDs


class Flags:
    pass

class TestCreateCaloCellsConfig (unittest.TestCase):
    def test_detIDs (self):
        flags = Flags()
        flags.compactFile = os.environ.get("K4GEO", "") + "/FCCee/ALLEGRO/compact/ALLEGRO_o1_v03/ALLEGRO_o1_v03.xml"

        self.assertEqual (detIDs (flags, 'DCH'), 3)
        self.assertEqual (detIDs (flags, ['ECAL_Barrel', 'ECAL_Endcap']), [4, 5])
        self.assertEqual (detIDs (flags, 'Muon_Endcap'), 13)
        self.assertEqual (detIDs (flags, 'Muon_Endcap_1'), 13)
        self.assertEqual (detIDs (flags, 'Muon_Endcap_2'), 14)
        return
        


if __name__ == '__main__':
    unittest.main()
