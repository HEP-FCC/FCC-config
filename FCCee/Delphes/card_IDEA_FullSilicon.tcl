####################################################################                                l
# FCC-ee IDEA detector model
#
# Authors: Elisa Fontanesi, Lorenzo Pezzotti, Massimiliano Antonello, Michele Selvaggi
# email: efontane@bo.infn.it,
#        lorenzo.pezzotti01@universitadipavia.it,
#        m.antonello@uninsubria.it,
#        michele.selvaggi@cern.ch
#####################################################################

set B 2.0

#######################################
# Order of execution of various modules
#######################################

set ExecutionPath {
  ParticlePropagator

  ChargedHadronTrackingEfficiency
  ElectronTrackingEfficiency
  MuonTrackingEfficiency

  TrackMergerPre
  TrackSmearing

  TrackMerger
  Calorimeter
  EFlowMerger

  PhotonEfficiency
  PhotonIsolation

  MuonFilter

  ElectronFilter
  ElectronEfficiency
  ElectronIsolation

  MuonEfficiency
  MuonIsolation

  MissingET

  NeutrinoFilter
  GenJetFinder
  GenMissingET

  FastJetFinder

  JetEnergyScale

  JetFlavorAssociation

  BTagging
  TauTagging

  UniqueObjectFinder

  ScalarHT
  TreeWriter
}

#################################
# Propagate particles in cylinder
#################################

module ParticlePropagator ParticlePropagator {
  set InputArray Delphes/stableParticles

  set OutputArray stableParticles
  set ChargedHadronOutputArray chargedHadrons
  set ElectronOutputArray electrons
  set MuonOutputArray muons

  # inner radius of the solenoid, in m
  set Radius 2.25

  # half-length: z of the solenoid, in m
  set HalfLength 2.5

  # magnetic field, in T
  set Bz $B
}

####################################
# Charged hadron tracking efficiency
####################################

module Efficiency ChargedHadronTrackingEfficiency {
    set InputArray ParticlePropagator/chargedHadrons
    set OutputArray chargedHadrons
    # We use only one efficiency, we set only 0 effincency out of eta bounds:

    set EfficiencyFormula {
        (abs(eta) > 3.0)                                       * (0.000) +
        (energy >= 0.5) * (abs(eta) <= 3.0)                    * (0.997) +
        (energy < 0.5 && energy >= 0.3) * (abs(eta) <= 3.0)    * (0.65) +
        (energy < 0.3) * (abs(eta) <= 3.0)                     * (0.06)
    }
}

#	(pt <= 0.1)                                     * (0.00) +
#	(abs(eta) <= 3.0)               * (pt > 0.1)    * (1.00) +
#	(abs(eta) > 3)                                  * (0.00)



##############################
# Electron tracking efficiency
##############################

module Efficiency ElectronTrackingEfficiency {
    set InputArray ParticlePropagator/electrons
    set OutputArray electrons


    # Current full simulation with CLICdet provides for electrons:
    set EfficiencyFormula {
        (abs(eta) > 3.0)                                       * (0.000) +
        (energy >= 0.5) * (abs(eta) <= 3.0)                    * (0.997) +
        (energy < 0.5 && energy >= 0.3) * (abs(eta) <= 3.0)    * (0.65) +
        (energy < 0.3) * (abs(eta) <= 3.0)                     * (0.06)
    }
}


##########################
# Muon tracking efficiency
##########################

module Efficiency MuonTrackingEfficiency {
    set InputArray ParticlePropagator/muons
    set OutputArray muons

    # Current full simulation with CLICdet provides for muons:
    set EfficiencyFormula {
        (abs(eta) > 3.0)                                       * (0.000) +
        (energy >= 0.5) * (abs(eta) <= 3.0)                    * (0.997) +
        (energy < 0.5 && energy >= 0.3) * (abs(eta) <= 3.0)    * (0.65) +
        (energy < 0.3) * (abs(eta) <= 3.0)                     * (0.06)
    }
}

##############
# Track merger
##############

module Merger TrackMergerPre {
# add InputArray InputArray
  add InputArray ChargedHadronTrackingEfficiency/chargedHadrons
  add InputArray ElectronTrackingEfficiency/electrons
  add InputArray MuonTrackingEfficiency/muons
  set OutputArray tracks
}


########################################
# Smearing for charged tracks
########################################

module TrackCovariance TrackSmearing {
    set InputArray TrackMergerPre/tracks
    set OutputArray tracks


    set InputArray TrackMergerPre/tracks
    set OutputArray tracks


    ## minimum number of hits to accept a track
    set NMinHits 6

    ## uses https://raw.githubusercontent.com/selvaggi/FastTrackCovariance/master/GeoIDEA_BASE.txt
    set DetectorGeometry {


      # Layer type 1 = R (barrel) or 2 = z (forward/backward)
      # Layer label
      # Minimum dimension z for barrel or R for forward
      # Maximum dimension z for barrel or R for forward
      # R/z location of layer
      # Thickness (meters)
      # Radiation length (meters)
      # Number of measurements in layers (1D or 2D)
      # Stereo angle (rad) - 0(pi/2) = axial(z) layer - Upper side
      # Stereo angle (rad) - 0(pi/2) = axial(z) layer - Lower side
      # Resolution Upper side (meters) - 0 = no measurement
      # Resolution Lower side (meters) - 0 = no measurement
      # measurement flag = T, scattering only = F


      # barrel  name       zmin   zmax   r        w (m)      X0        n_meas  th_up (rad) th_down (rad)    reso_up (m)   reso_down (m)  flag

       1        PIPE       -100    100    0.015    0.001655  0.2805     0        0          0                0             0              0
       1 VTX -0.125 0.125 0.0175 4.5e-005 0.0937 2 0 1.5708 3e-006 3e-006 1
       1 VTX -0.125 0.125 0.0185 4.5e-005 0.0937 2 0 1.5708 3e-006 3e-006 1
       1 VTX -0.125 0.125 0.037 4.5e-005 0.0937 2 0 1.5708 3e-006 3e-006 1
       1 VTX -0.125 0.125 0.038 4.5e-005 0.0937 2 0 1.5708 3e-006 3e-006 1
       1 VTX -0.125 0.125 0.057 4.5e-005 0.0937 2 0 1.5708 3e-006 3e-006 1
       1 VTX -0.125 0.125 0.058 4.5e-005 0.0937 2 0 1.5708 3e-006 3e-006 1
       1 VTX -0.125 0.125 0.018 0.000557 0.0937 0 0 0 0 0 0
       1 VTX -0.125 0.125 0.0375 0.000557 0.0937 0 0 0 0 0 0
       1 VTX -0.125 0.125 0.0575 0.000557 0.0937 0 0 0 0 0 0
       1 VTX -0.5 0.5 0.112 0.000337 0.0937 0 0 0 0 0 0
       1 VTX -0.126 0.126 0.111 9e-006 0.0937 0 0 0 0 0 0
       1 VTX -0.5 0.5 0.1115 9e-006 0.0937 0 0 0 0 0 0
       1 ITK -0.4816 0.4816 0.127 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       1 ITK -0.4816 0.4816 0.4 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       1 ITK -0.6923 0.6923 0.67 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       1 ITK -0.4816 0.4816 0.132 0.000159 0.0937 0 0 0 0 0 0
       1 ITK -0.4816 0.4816 0.405 0.000159 0.0937 0 0 0 0 0 0
       1 ITK -0.6923 0.6923 0.675 0.000159 0.0937 0 0 0 0 0 0
       1 ITK -2.3 2.3 0.686 0.001171 0.0937 0 0 0 0 0 0
       1 ITK -2.3 2.3 0.6855 0.000281 0.0937 0 0 0 0 0 0
       1 OTK -1.2642 1.2642 1 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       1 OTK -1.2642 1.2642 1.568 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       1 OTK -1.2642 1.2642 2.136 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       1 OTK -1.2642 1.2642 1.005 0.000244 0.0937 0 0 0 0 0 0
       1 OTK -1.2642 1.2642 1.578 0.000117 0.0937 0 0 0 0 0 0
       1 OTK -1.2642 1.2642 2.126 0.000117 0.0937 0 0 0 0 0 0

      # endcap  name       rmin   rmax   z        w (m)      X0        n_meas   th_up (rad)  th_down (rad)   reso_up (m)   reso_down (m) flag
      
       2 VTXDSK 0.045 0.102 -0.301 4.4e-005 0.0937 2 0 1.5708 3e-006 3e-006 1
       2 VTXDSK 0.045 0.102 -0.299 4.4e-005 0.0937 2 0 1.5708 3e-006 3e-006 1
       2 VTXDSK 0.0345 0.102 -0.231 4.4e-005 0.0937 2 0 1.5708 3e-006 3e-006 1
       2 VTXDSK 0.0345 0.102 -0.229 4.4e-005 0.0937 2 0 1.5708 3e-006 3e-006 1
       2 VTXDSK 0.024 0.102 -0.161 4.4e-005 0.0937 2 0 1.5708 3e-006 3e-006 1
       2 VTXDSK 0.024 0.102 -0.159 4.4e-005 0.0937 2 0 1.5708 3e-006 3e-006 1
       2 VTXDSK 0.024 0.102 0.159 4.4e-005 0.0937 2 0 1.5708 3e-006 3e-006 1
       2 VTXDSK 0.024 0.102 0.161 4.4e-005 0.0937 2 0 1.5708 3e-006 3e-006 1
       2 VTXDSK 0.0345 0.102 0.229 4.4e-005 0.0937 2 0 1.5708 3e-006 3e-006 1
       2 VTXDSK 0.0345 0.102 0.231 4.4e-005 0.0937 2 0 1.5708 3e-006 3e-006 1
       2 VTXDSK 0.045 0.102 0.299 4.4e-005 0.0937 2 0 1.5708 3e-006 3e-006 1
       2 VTXDSK 0.045 0.102 0.301 4.4e-005 0.0937 2 0 1.5708 3e-006 3e-006 1
       2 VTXDSK 0.075 0.102 -0.5 0.000337 0.0937 0 0 0 0 0 0
       2 VTXDSK 0.045 0.102 -0.3 0.000557 0.0937 0 0 0 0 0 0
       2 VTXDSK 0.0345 0.102 -0.23 0.000557 0.0937 0 0 0 0 0 0
       2 VTXDSK 0.024 0.102 -0.16 0.000557 0.0937 0 0 0 0 0 0
       2 VTXDSK 0.0175 0.112 -0.126 9e-006 0.0937 0 0 0 0 0 0
       2 VTXDSK 0.0175 0.112 0.126 9e-006 0.0937 0 0 0 0 0 0
       2 VTXDSK 0.024 0.102 0.16 0.000557 0.0937 0 0 0 0 0 0
       2 VTXDSK 0.0345 0.102 0.23 0.000557 0.0937 0 0 0 0 0 0
       2 VTXDSK 0.045 0.102 0.3 0.000557 0.0937 0 0 0 0 0 0
       2 VTXDSK 0.075 0.102 0.5 0.000337 0.0937 0 0 0 0 0 0
       2 ITKDSK 0.33 0.647 -2.19 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 ITKDSK 0.293 0.64 -1.946 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 ITKDSK 0.2495 0.657 -1.661 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 ITKDSK 0.2075 0.6605 -1.377 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 ITKDSK 0.166 0.663 -1.093 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 ITKDSK 0.1235 0.652 -0.808 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 ITKDSK 0.0795 0.457 -0.524 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 ITKDSK 0.0795 0.457 0.524 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 ITKDSK 0.1235 0.652 0.808 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 ITKDSK 0.166 0.663 1.093 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 ITKDSK 0.2075 0.6605 1.377 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 ITKDSK 0.2495 0.657 1.661 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 ITKDSK 0.293 0.64 1.946 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 ITKDSK 0.33 0.647 2.19 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 ITKDSK 0.33 0.648 -2.18 0.000346 0.0937 0 0 0 0 0 0
       2 ITKDSK 0.293 0.641 -1.956 0.000346 0.0937 0 0 0 0 0 0
       2 ITKDSK 0.2495 0.658 -1.651 0.000321 0.0937 0 0 0 0 0 0
       2 ITKDSK 0.2075 0.6615 -1.387 0.000321 0.0937 0 0 0 0 0 0
       2 ITKDSK 0.166 0.664 -1.083 0.000289 0.0937 0 0 0 0 0 0
       2 ITKDSK 0.1235 0.653 -0.818 0.000289 0.0937 0 0 0 0 0 0
       2 ITKDSK 0.0795 0.456 -0.514 0.000309 0.0937 0 0 0 0 0 0
       2 ITKDSK 0.0795 0.456 0.514 0.000309 0.0937 0 0 0 0 0 0
       2 ITKDSK 0.1235 0.653 0.818 0.000289 0.0937 0 0 0 0 0 0
       2 ITKDSK 0.166 0.664 1.083 0.000289 0.0937 0 0 0 0 0 0
       2 ITKDSK 0.2075 0.6615 1.387 0.000321 0.0937 0 0 0 0 0 0
       2 ITKDSK 0.2495 0.658 1.651 0.000321 0.0937 0 0 0 0 0 0
       2 ITKDSK 0.293 0.641 1.956 0.000346 0.0937 0 0 0 0 0 0
       2 ITKDSK 0.33 0.648 2.18 0.000346 0.0937 0 0 0 0 0 0
       2 OTKDSK 0.718 2.08 -2.19 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 OTKDSK 0.718 2.08 -1.883 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 OTKDSK 0.718 2.08 -1.617 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 OTKDSK 0.718 2.08 -1.31 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 OTKDSK 0.718 2.08 1.31 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 OTKDSK 0.718 2.08 1.617 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 OTKDSK 0.718 2.08 1.883 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 OTKDSK 0.718 2.08 2.19 0.000956 0.0937 2 0 1.5708 7e-006 9e-005 1
       2 OTKDSK 0.99 2.08 -1.2842 0.000562 0.0937 0 0 0 0 0 0
       2 OTKDSK 0.6517 0.686 -0.7123 0.000562 0.0937 0 0 0 0 0 0
       2 OTKDSK 0.127 0.65 -0.5016 0.000562 0.0937 0 0 0 0 0 0
       2 OTKDSK 0.718 2.08 -2.18 0.000342 0.0937 0 0 0 0 0 0
       2 OTKDSK 0.718 2.08 -1.893 0.000342 0.0937 0 0 0 0 0 0
       2 OTKDSK 0.718 2.08 -1.607 0.000342 0.0937 0 0 0 0 0 0
       2 OTKDSK 0.718 2.08 -1.32 0.000342 0.0937 0 0 0 0 0 0
       2 OTKDSK 0.718 2.08 1.32 0.000342 0.0937 0 0 0 0 0 0
       2 OTKDSK 0.718 2.08 1.607 0.000342 0.0937 0 0 0 0 0 0
       2 OTKDSK 0.718 2.08 1.893 0.000342 0.0937 0 0 0 0 0 0
       2 OTKDSK 0.718 2.08 2.18 0.000342 0.0937 0 0 0 0 0 0
       2 OTKDSK 0.127 0.65 0.5016 0.000562 0.0937 0 0 0 0 0 0
       2 OTKDSK 0.6517 0.686 0.7123 0.000562 0.0937 0 0 0 0 0 0
       2 OTKDSK 0.99 2.08 1.2842 0.000562 0.0937 0 0 0 0 0 0
       1 MAG -2.5 2.5 2.25 0.05 0.0658 0 0 0 0 0 0

      # endcap  name       rmin   rmax   z        w (m)      X0        n_meas   th_up (rad)  th_down (rad)   reso_up (m)   reso_down (m) flag

    }

    set Bz $B
}

##############
# Track merger
##############

module Merger TrackMerger {
# add InputArray InputArray
  add InputArray TrackSmearing/tracks
  set OutputArray tracks
}


#############
# Calorimeter
#############
module DualReadoutCalorimeter Calorimeter {
  set ParticleInputArray ParticlePropagator/stableParticles
  set TrackInputArray TrackMerger/tracks

  set TowerOutputArray towers
  set PhotonOutputArray photons

  set EFlowTrackOutputArray eflowTracks
  set EFlowPhotonOutputArray eflowPhotons
  set EFlowNeutralHadronOutputArray eflowNeutralHadrons

  set ECalEnergyMin 0.5
  set HCalEnergyMin 0.5
  set EnergyMin 0.5
  set ECalEnergySignificanceMin 1.0
  set HCalEnergySignificanceMin 1.0
  set EnergySignificanceMin 1.0

  set SmearTowerCenter true
    set pi [expr {acos(-1)}]

    # Lists of the edges of each tower in eta and phi;
    # each list starts with the lower edge of the first tower;
    # the list ends with the higher edged of the last tower.
    # Barrel:  deta=0.02 towers up to |eta| <= 0.88 ( up to 45°)
    # Endcaps: deta=0.02 towers up to |eta| <= 3.0 (8.6° = 100 mrad)
    # Cell size: about 6 cm x 6 cm

    #barrel:
    set PhiBins {}
    for {set i -120} {$i <= 120} {incr i} {
        add PhiBins [expr {$i * $pi/120}]
    }
    #deta=0.02 units for |eta| <= 0.88
    for {set i -44} {$i < 45} {incr i} {
        set eta [expr {$i * 0.02}]
        add EtaPhiBins $eta $PhiBins
    }

    #endcaps:
    set PhiBins {}
    for {set i -120} {$i <= 120} {incr i} {
        add PhiBins [expr {$i* $pi/120}]
    }
    #deta=0.02 units for 0.88 < |eta| <= 3.0
    #first, from -3.0 to -0.88
    for {set i 1} {$i <=106} {incr i} {
        set eta [expr {-3.00 + $i * 0.02}]
        add EtaPhiBins $eta $PhiBins
    }
    #same for 0.88 to 3.0
    for  {set i 1} {$i <=106} {incr i} {
        set eta [expr {0.88 + $i * 0.02}]
        add EtaPhiBins $eta $PhiBins
    }

    # default energy fractions {abs(PDG code)} {Fecal Fhcal}
    add EnergyFraction {0} {0.0 1.0}
    # energy fractions for e, gamma and pi0
    add EnergyFraction {11} {1.0 0.0}
    add EnergyFraction {22} {1.0 0.0}
    add EnergyFraction {111} {1.0 0.0}
    # energy fractions for muon, neutrinos and neutralinos
    add EnergyFraction {12} {0.0 0.0}
    add EnergyFraction {13} {0.0 0.0}
    add EnergyFraction {14} {0.0 0.0}
    add EnergyFraction {16} {0.0 0.0}
    add EnergyFraction {1000022} {0.0 0.0}
    add EnergyFraction {1000023} {0.0 0.0}
    add EnergyFraction {1000025} {0.0 0.0}
    add EnergyFraction {1000035} {0.0 0.0}
    add EnergyFraction {1000045} {0.0 0.0}
    # energy fractions for K0short and Lambda
    add EnergyFraction {310} {0.3 0.7}
    add EnergyFraction {3122} {0.3 0.7}


    # set ECalResolutionFormula {resolution formula as a function of eta and energy}
    set ECalResolutionFormula {
    (abs(eta) <= 0.88 )                     * sqrt(energy^2*0.01^2 + energy*0.11^2)+
    (abs(eta) > 0.88 && abs(eta) <= 3.0)    * sqrt(energy^2*0.01^2 + energy*0.11^2)
    }

    # set HCalResolutionFormula {resolution formula as a function of eta and energy}
    set HCalResolutionFormula {
    (abs(eta) <= 0.88 )                     * sqrt(energy^2*0.01^2 + energy*0.30^2)+
    (abs(eta) > 0.88 && abs(eta) <= 3.0)    * sqrt(energy^2*0.01^2 + energy*0.30^2)
    }
}

####################
# Energy flow merger
####################

module Merger EFlowMerger {
# add InputArray InputArray
  add InputArray Calorimeter/eflowTracks
  add InputArray Calorimeter/eflowPhotons
  add InputArray Calorimeter/eflowNeutralHadrons
  set OutputArray eflow
}

###################
# Photon efficiency
###################

module Efficiency PhotonEfficiency {
  set InputArray Calorimeter/eflowPhotons
  set OutputArray photons

  # set EfficiencyFormula {efficiency formula as a function of eta and pt}
  # efficiency formula for photons
  set EfficiencyFormula {
        (energy < 2.0)                                        * (0.000)+
        (energy >= 2.0) * (abs(eta) <= 0.88)                  * (0.99) +
        (energy >= 2.0) * (abs(eta) >0.88 && abs(eta) <= 3.0) * (0.99) +
        (abs(eta) > 3.0)                                      * (0.000)
  }
}

##################
# Photon isolation
##################

module Isolation PhotonIsolation {
  set CandidateInputArray PhotonEfficiency/photons
  set IsolationInputArray EFlowMerger/eflow

  set OutputArray photons

  set DeltaRMax 0.5

  set PTMin 0.5

  set PTRatioMax 999.
}

#################
# Electron filter
#################

module PdgCodeFilter ElectronFilter {
  set InputArray Calorimeter/eflowTracks
  set OutputArray electrons
  set Invert true
  add PdgCode {11}
  add PdgCode {-11}
}

#################
# Muon filter
#################

module PdgCodeFilter MuonFilter {
  set InputArray Calorimeter/eflowTracks
  set OutputArray muons
  set Invert true
  add PdgCode {13}
  add PdgCode {-13}
}


#####################
# Electron efficiency
#####################

module Efficiency ElectronEfficiency {
  set InputArray ElectronFilter/electrons
  set OutputArray electrons

  # set EfficiencyFormula {efficiency formula as a function of eta and pt}

  # efficiency formula for electrons
  set EfficiencyFormula {
        (energy < 2.0)                                         * (0.000)+
        (energy >= 2.0) * (abs(eta) <= 0.88)                   * (0.99) +
        (energy >= 2.0) * (abs(eta) >0.88 && abs(eta) <= 3.0)  * (0.99) +
        (abs(eta) > 3.0)                                       * (0.000)
  }
}

####################
# Electron isolation
####################

module Isolation ElectronIsolation {
  set CandidateInputArray ElectronEfficiency/electrons
  set IsolationInputArray EFlowMerger/eflow

  set OutputArray electrons

  set DeltaRMax 0.5

  set PTMin 0.5

  set PTRatioMax 0.12
}

#################
# Muon efficiency
#################

module Efficiency MuonEfficiency {
  set InputArray MuonFilter/muons
  set OutputArray muons

  # set EfficiencyFormula {efficiency as a function of eta and pt}

  # efficiency formula for muons
  set EfficiencyFormula {
        (energy < 2.0)                                         * (0.000)+
        (energy >= 2.0) * (abs(eta) <= 0.88)                   * (0.99) +
        (energy >= 2.0) * (abs(eta) >0.88 && abs(eta) <= 3.0)  * (0.99) +
        (abs(eta) > 3.0)                                       * (0.000)
  }
}

################
# Muon isolation
################

module Isolation MuonIsolation {
  set CandidateInputArray MuonEfficiency/muons
  set IsolationInputArray EFlowMerger/eflow

  set OutputArray muons

  set DeltaRMax 0.5

  set PTMin 0.5

  set PTRatioMax 0.25
}

###################
# Missing ET merger
###################

module Merger MissingET {
# add InputArray InputArray
  add InputArray EFlowMerger/eflow
  set MomentumOutputArray momentum
}

##################
# Scalar HT merger
##################

module Merger ScalarHT {
# add InputArray InputArray
  add InputArray UniqueObjectFinder/jets
  add InputArray UniqueObjectFinder/electrons
  add InputArray UniqueObjectFinder/photons
  add InputArray UniqueObjectFinder/muons
  set EnergyOutputArray energy
}

#####################
# Neutrino Filter
#####################

module PdgCodeFilter NeutrinoFilter {

  set InputArray Delphes/stableParticles
  set OutputArray filteredParticles

  set PTMin 0.0

  add PdgCode {12}
  add PdgCode {14}
  add PdgCode {16}
  add PdgCode {-12}
  add PdgCode {-14}
  add PdgCode {-16}
}


#####################
# MC truth jet finder
#####################

module FastJetFinder GenJetFinder {
  set InputArray NeutrinoFilter/filteredParticles

  set OutputArray jets

  # algorithm: 1 CDFJetClu, 2 MidPoint, 3 SIScone, 4 kt, 5 Cambridge/Aachen, 6 antikt
  set JetAlgorithm 6
  set ParameterR 0.4
  set JetPTMin 1.0
}


#########################
# Gen Missing ET merger
########################

module Merger GenMissingET {
# add InputArray InputArray
  add InputArray NeutrinoFilter/filteredParticles
  set MomentumOutputArray momentum
}

############
# Jet finder
############

module FastJetFinder FastJetFinder {
#  set InputArray Calorimeter/towers
  set InputArray EFlowMerger/eflow

  set OutputArray jets

  # algorithm: 1 CDFJetClu, 2 MidPoint, 3 SIScone, 4 kt, 5 Cambridge/Aachen, 6 antikt
  set JetAlgorithm 6
  set ParameterR 0.4
  set JetPTMin 1.0
}

##################
# Jet Energy Scale
##################

module EnergyScale JetEnergyScale {
  set InputArray FastJetFinder/jets
  set OutputArray jets

  # scale formula for jets
  set ScaleFormula {1.08}
}

########################
# Jet Flavor Association
########################

module JetFlavorAssociation JetFlavorAssociation {

  set PartonInputArray Delphes/partons
  set ParticleInputArray Delphes/allParticles
  set ParticleLHEFInputArray Delphes/allParticlesLHEF
  set JetInputArray JetEnergyScale/jets

  set DeltaR 0.5
  set PartonPTMin 1.0
  set PartonEtaMax 3.0
}

###########
# b-tagging
###########

module BTagging BTagging {
  set JetInputArray JetEnergyScale/jets

  set BitNumber 0

  # add EfficiencyFormula {abs(PDG code)} {efficiency formula as a function of eta and pt}

  # default efficiency formula (misidentification rate)
  add EfficiencyFormula {0} {0.01}

  # efficiency formula for c-jets (misidentification rate)
  add EfficiencyFormula {4} {0.10}

  # efficiency formula for b-jets
  add EfficiencyFormula {5} {0.80}
}

#############
# tau-tagging
#############

module TauTagging TauTagging {
  set ParticleInputArray Delphes/allParticles
  set PartonInputArray Delphes/partons
  set JetInputArray JetEnergyScale/jets

  set DeltaR 0.5
  set TauPTMin 1.0
  set TauEtaMax 3.0

  # default efficiency formula (misidentification rate)
  add EfficiencyFormula {0} {0.001}
  # efficiency formula for tau-jets
  add EfficiencyFormula {15} {0.6}
}


#####################################################
# Find uniquely identified photons/electrons/tau/jets
#####################################################

module UniqueObjectFinder UniqueObjectFinder {
# earlier arrays take precedence over later ones
# add InputArray InputArray OutputArray
  add InputArray PhotonIsolation/photons photons
  add InputArray ElectronIsolation/electrons electrons
  add InputArray MuonIsolation/muons muons
  add InputArray JetEnergyScale/jets jets
}



##################
# ROOT tree writer
##################

# Tracks, towers and eflow objects are not stored by default in the output.
# If needed (for jet constituent or other studies), uncomment the relevant
# "add Branch ..." lines.

module TreeWriter TreeWriter {
    # add Branch InputArray BranchName BranchClass

    add Branch Delphes/allParticles Particle GenParticle

    add Branch TrackMerger/tracks Track Track
    add Branch Calorimeter/towers Tower Tower

    add Branch Calorimeter/eflowTracks EFlowTrack Track
    add Branch Calorimeter/eflowPhotons EFlowPhoton Tower
    add Branch Calorimeter/eflowNeutralHadrons EFlowNeutralHadron Tower

    add Branch Calorimeter/photons CaloPhoton Photon
    add Branch PhotonEfficiency/photons PhotonEff Photon
    add Branch PhotonIsolation/photons PhotonIso Photon

    add Branch GenJetFinder/jets GenJet Jet
    add Branch GenMissingET/momentum GenMissingET MissingET

    add Branch UniqueObjectFinder/jets Jet Jet
    add Branch UniqueObjectFinder/electrons Electron Electron
    add Branch UniqueObjectFinder/photons Photon Photon
    add Branch UniqueObjectFinder/muons Muon Muon
    add Branch MuonEfficiency/muons  AllMuon Muon

    add Branch JetEnergyScale/jets AntiKtJet Jet

    add Branch MissingET/momentum MissingET MissingET
    add Branch ScalarHT/energy ScalarHT ScalarHT

    # add Info InfoName InfoValue
    add Info Bz $B
}
