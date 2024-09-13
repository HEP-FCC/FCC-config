! 1) Settings used in the main program.
Random:setSeed = on
Main:timesAllowErrors = 5          ! how many aborts before run stops
PDF:lepton = on

! 2) Settings related to output in init(), next() and stat().
Init:showChangedSettings = on      ! list changed settings
Init:showChangedParticleData = off ! list changed particle data
Next:numberCount = 10             ! print message every n events
Next:numberShowInfo = 1            ! print event information n times
Next:numberShowProcess = 1         ! print process record n times
Next:numberShowEvent = 0           ! print event record n times

! 3) Beam parameter settings. Values below agree with default ones.
Beams:idA = 11                   ! first beam, electron
Beams:idB = -11                  ! second beam, positron

Beams:allowMomentumSpread  = off

! Vertex smearing :
Beams:allowVertexSpread = on
Beams:sigmaVertexX = 5.96e-3   
Beams:sigmaVertexY = 23.8E-6 
Beams:sigmaVertexZ = 0.397     
Beams:sigmaTime = 10.89    !  36.3 ps

! 4) Tell Pythia that LHEF input is used
Beams:frameType             = 4
Beams:setProductionScalesFromLHEF = off
Beams:LHEF = events.lhe


! 5) Hard process : Z->qqbar at Ecm=91 GeV
Beams:eCM = 91.118  ! CM energy of collision
WeakSingleBoson:ffbar2ffbar(s:gmZ) = on
PartonLevel:ISR = on               ! initial-state radiation
PartonLevel:FSR = on               ! final-state radiation
