"""Sanity checks on the IDEA o2 digi/reco output produced by ctest_sim_digi_reco.sh.

Checks the final products of the chain -- truth tracks, topo clusters and Pandora
particle-flow objects -- beyond simply counting them.
"""

import sys

import edm4hep
import podio.reading

AT_CALORIMETER = edm4hep.TrackState.AtCalorimeter


def check(path):
    n_track = n_cluster = n_pfo = 0
    no_calo_state = no_mc = no_hits = 0
    pfo_charged_no_input = pfo_bad_energy = 0

    for frame in podio.reading.get_reader(path).get("events"):
        tracks = frame.get("TracksFromGenParticles")
        n_track += len(tracks)

        # the track-driven seeding consumes the state extrapolated to the calorimeter
        for track in tracks:
            if not any(ts.location == AT_CALORIMETER for ts in track.getTrackStates()):
                no_calo_state += 1

        associated = {lk.getFrom().id() for lk in frame.get("TracksFromGenParticlesAssociation")}
        no_mc += sum(1 for track in tracks if track.id() not in associated)

        clusters = frame.get("TopoGrownClusters")
        n_cluster += len(clusters)
        no_hits += sum(1 for cluster in clusters if len(cluster.getHits()) == 0)

        pfos = frame.get("PandoraPfaIdea")
        n_pfo += len(pfos)
        # PFOs without track and cluster are legitimate only as neutral excess emitted along a charged
        # cluster (IdeaPfoCreationAlgorithm), so they must be neutral; every PFO has a positive energy
        pfo_charged_no_input += sum(1 for pfo in pfos
                                    if len(pfo.getTracks()) == 0 and len(pfo.getClusters()) == 0
                                    and pfo.getCharge() != 0)
        pfo_bad_energy += sum(1 for pfo in pfos if not pfo.getEnergy() > 0)

    print(f"truth tracks {n_track}, topo clusters {n_cluster}, pandora PFOs {n_pfo}")

    checks = [
        (n_track > 0, "no truth tracks were produced"),
        (no_calo_state == 0, f"{no_calo_state} tracks have no AtCalorimeter state"),
        (no_mc == 0, f"{no_mc} tracks are not associated to an MC particle"),
        (n_cluster > 0, "no topo clusters were grown"),
        (no_hits == 0, f"{no_hits} clusters have no hits"),
        (n_pfo > 0, "no pandora PFOs were produced"),
        (pfo_charged_no_input == 0, f"{pfo_charged_no_input} charged PFOs have neither a track nor a cluster"),
        (pfo_bad_energy == 0, f"{pfo_bad_energy} PFOs have a non-positive energy"),
    ]
    for ok, msg in checks:
        if not ok:
            print("FAIL:", msg)

    return all(ok for ok, _ in checks)


if __name__ == "__main__":
    sys.exit(0 if check(sys.argv[1]) else 1)
