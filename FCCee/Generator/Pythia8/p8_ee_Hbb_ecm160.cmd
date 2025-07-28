
! 1) Settings that will be used in a main program.
Random:setSeed = on
Main:timesAllowErrors = 5          ! how many aborts before run stops

! 2) Settings related to output in init(), next() and stat() functions.
Init:showChangedSettings = on      ! list changed settings
Init:showAllSettings = off         ! list all settings
Init:showChangedParticleData = on  ! list changed particle data
Init:showAllParticleData = off     ! list all particle data
Next:numberCount = 10              ! print message every n events
Next:numberShowLHA = 10            ! print LHA information n times
Next:numberShowInfo = 10           ! print event information n times
Next:numberShowProcess = 10        ! print process record n times
Next:numberShowEvent = 10          ! print event record n times
Stat:showPartonLevel = off         ! additional statistics on MPI

! 3) Tell Pythia that LHEF input is used
Beams:frameType = 4
Beams:setProductionScalesFromLHEF = off
Beams:allowMomentumSpread  = off
Beams:LHEF = LHE_OUT.LHE

! Vertex smearing
Beams:allowVertexSpread = on
Beams:sigmaVertexX = 1.47e-2   !  13.7 mum / sqrt2
Beams:sigmaVertexY = 46.5E-6   !  36.1 nm / sqrt2
Beams:sigmaVertexZ = 0.97      !  0.97 mm

! 4) Settings for the event generation process in the Pythia8 library.
PartonLevel:ISR = off               ! initial-state radiation
PartonLevel:FSR = on                ! final-state radiation

Check:epTolErr = 1e-1               ! default 1e-4, necessary to allow BES
LesHouches:matchInOut = off


! 5) decay Higgs
25:onMode = off
25:onIfAny = 5
