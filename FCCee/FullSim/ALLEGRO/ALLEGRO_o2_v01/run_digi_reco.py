# run_digi_reco.py
# steering file for the ALLEGRO_o2_v01 digitization/reconstruction

import os
import sys
# add ALLEGRO/ parent directory so run_digi_reco_common can be imported
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ALLEGRO_common"))
from run_digi_reco_common import run_digi_reco
from types import SimpleNamespace

path_to_detector = os.environ.get("K4GEO", "") + "/FCCee/ALLEGRO/compact/ALLEGRO_o2_v01/"
detectors_to_use = [
    'ALLEGRO_o2_v01.xml'
]

wire_tracker = SimpleNamespace(
    det_id_key="DetID_STT",
    id_name="STT",
    hit_collection="STTCollection",
    digi_collection="STTDigis",
    sim_digi_links="STTDigisSimAssociationCollection",
    dNdx_output_collection="STTdNdxCollection",
    dNdx_Zmax_param="STT_half_length_total",
    dNdx_Zmin_param="STT_half_length_total",
    dNdx_Rmin_param="STT_inner_cyl_R_total",
    dNdx_Rmax_param="STT_outer_cyl_R_total",
    dNdx_fill_factor=1.0,   #FIXME: get number for STT
    digi_algo_name="WireTrackerV1",
    dchi_name="STT_o1_v01",
    is_stt=True,
    drop_hits=False,
    drop_hits_command="STTCollection*",
)

run_digi_reco(path_to_detector, detectors_to_use, wire_tracker)
