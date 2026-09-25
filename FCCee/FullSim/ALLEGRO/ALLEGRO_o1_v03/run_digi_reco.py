# run_digi_reco.py
# steering file for the ALLEGRO_o1_v03 digitization/reconstruction

import os
import sys
# add ALLEGRO/ parent directory so run_digi_reco_common can be imported
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ALLEGRO_common"))
from run_digi_reco_common import run_digi_reco
from types import SimpleNamespace

path_to_detector = os.environ.get("K4GEO", "") + "/FCCee/ALLEGRO/compact/ALLEGRO_o1_v03/"
detectors_to_use = [
    'ALLEGRO_o1_v03.xml'
]

wire_tracker = SimpleNamespace(
    det_id_key="DetID_DCH",
    id_name="DCH",
    hit_collection="DCHCollection",
    digi_collection="DCHDigis",
    sim_digi_links="DCHDigisSimAssociationCollection",
    dNdx_output_collection="DCHdNdxCollection",
    dNdx_Zmax_param="DCH_gas_Lhalf",
    dNdx_Zmin_param="DCH_gas_Lhalf",
    dNdx_Rmin_param="DCH_gas_inner_cyl_R",
    dNdx_Rmax_param="DCH_gas_outer_cyl_R",
    dNdx_fill_factor=1.0,
    digi_algo_name="DCHDigitizer",
    dchi_name="DCH_v2",
    is_stt=False,
    drop_hits=False,
    drop_hits_command="DCHCollection*",
)

run_digi_reco(path_to_detector, detectors_to_use, wire_tracker)
