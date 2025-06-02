! main03.cmnd.
! This file contains commands to be read in for a Pythia8 run.
! Lines not beginning with a letter or digit are comments.
! Names are case-insensitive  -  but spellings-sensitive!
! The settings here are illustrative, not always physics-motivated.

! 1) Settings used in the main program.
Random:setSeed = on
Main:timesAllowErrors = 5          ! how many aborts before run stops
Stat:showProcessLevel = on

! 2) Settings related to output in init(), next() and stat().
Init:showChangedSettings = on      ! list changed settings
Init:showChangedParticleData = off ! list changed particle data
Next:numberCount = 100             ! print message every n events
Next:numberShowInfo = 1            ! print event information n times
Next:numberShowProcess = 1         ! print process record n times
Next:numberShowEvent = 0           ! print event record n times

! 3) Beam parameter settings. Values below agree with default ones.
Beams:idA = 11                   ! first beam, e = 2212, pbar = -2212
Beams:idB = -11                   ! second beam, e = 2212, pbar = -2212

! Beam energy spread: 0.132% x 45.594 GeV = 0.0602 GeV
Beams:allowMomentumSpread  = off

! Vertex smearing :
Beams:allowVertexSpread = on
Beams:sigmaVertexX = 5.96e-3   
Beams:sigmaVertexY = 23.8E-6 
Beams:sigmaVertexZ = 0.397     
Beams:sigmaTime = 10.89    !  36.3 ps


! 4) Hard process : Z->tau+tau- at Ecm=91 GeV
Beams:eCM = 91.188  ! CM energy of collision

! set nu_tau mass 
ParticleData:mass(16) = 0.0001 ! 0.1 MeV

WeakSingleBoson:ffbar2gmZ = on
23:onMode = off
23:onIfAny = 15
