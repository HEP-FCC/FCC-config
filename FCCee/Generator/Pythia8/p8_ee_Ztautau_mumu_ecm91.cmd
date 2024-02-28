! main03.cmnd.
! This file contains commands to be read in for a Pythia8 run.
! Lines not beginning with a letter or digit are comments.
! Names are case-insensitive  -  but spellings-sensitive!
! The settings here are illustrative, not always physics-motivated.

! 1) Settings used in the main program.
Random:setSeed = on
Main:timesAllowErrors = 5          ! how many aborts before run stops
Stat:showProcessLevel = on
Stat:showErrors = off

! 2) Settings related to output in init(), next() and stat().
Init:showChangedSettings = on      ! list changed settings
Init:showChangedParticleData = off ! list changed particle data
Init:showAllSettings = off
Next:numberCount = 1000             ! print message every n events
Next:numberShowInfo = 10            ! print event information n times
Next:numberShowProcess = 10         ! print process record n times
Next:numberShowEvent = 10           ! print event record n times

! 3) Beam parameter settings. Values below agree with default ones.
Beams:idA = 11                   ! first beam, e = 2212, pbar = -2212
Beams:idB = -11                   ! second beam, e = 2212, pbar = -2212

! 4) Hard process : Z->qqbar at Ecm=91 GeV
Beams:eCM = 91.188  ! CM energy of collision

! full interference between the gamma and Z
WeakSingleBoson:ffbar2gmZ = on

! Only allow Taus in the final state
23:onMode = off
23:onIfAny = 15
22:onMode = off
22:onIfAny = 15

! Force Tau decays to mu nu_tau nu_mu
15:onMode = off
15:onIfAny = 14
