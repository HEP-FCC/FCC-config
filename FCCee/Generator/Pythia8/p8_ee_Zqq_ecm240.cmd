Random:setSeed = on
Main:numberOfEvents = 1000         ! number of events to generate
Main:timesAllowErrors = 5          ! how many aborts before run stops


! 2) Settings related to output in init(), next() and stat().
Init:showChangedSettings = on      ! list changed settings
Init:showChangedParticleData = off ! list changed particle data
Next:numberCount = 100            ! print message every n events
Next:numberShowInfo = 1            ! print event information n times
Next:numberShowProcess = 1         ! print process record n times
Next:numberShowEvent = 0           ! print event record n times
Stat:showPartonLevel = off

! 3) Beam parameter settings. Values below agree with default ones.
Beams:idA = 11                   ! first beam, e- = 11
Beams:idB = -11                  ! second beam, e+ = -11

Beams:eCM = 240               ! CM energy of collision

Beams:allowMomentumSpread  = off

! Vertex smearing :
Beams:allowVertexSpread = on
Beams:sigmaVertexX = 9.80e-3   !  9.80 mum
Beams:sigmaVertexY = 25.4E-6   !  25.4 nm
Beams:sigmaVertexZ = 0.64      !  0.64 mm

WeakSingleBoson:ffbar2ffbar(s:gmZ) = on

PartonLevel:ISR = on               ! initial-state radiation
PartonLevel:FSR = on               ! final-state radiation

! Decays
!Z0
23:onMode = off
23:onIfAny = 1 2 3 4 5 6

ParticleDecays:limitCylinder = on
ParticleDecays:xyMax = 2250.
ParticleDecays:zMax = 2500.

