Random:setSeed = on
Main:numberOfEvents = 1000         ! number of events to generate
Main:timesAllowErrors = 5          ! how many aborts before run stops

! 2) Settings related to output in init(), next() and stat().
Init:showChangedSettings = on      ! list changed settings
Init:showChangedParticleData = off ! list changed particle data
Next:numberCount = 100             ! print message every n events
Next:numberShowInfo = 1            ! print event information n times
Next:numberShowProcess = 1         ! print process record n times
Next:numberShowEvent = 0           ! print event record n times

Beams:idA = 11                   ! first beam, e+ = 11
Beams:idB = -11                   ! second beam, e- = -11

! Beam energy spread: 0.165% x 120 GeV = 0.198 GeV
Beams:allowMomentumSpread  = on
Beams:sigmaPzA = 0.198
Beams:sigmaPzB = 0.198

! Vertex smearing :
Beams:allowVertexSpread = on
Beams:sigmaVertexX = 9.70e-3   !  13.7 mum / sqrt2
Beams:sigmaVertexY = 25.5E-6   !  36.1 nm / sqrt2
Beams:sigmaVertexZ = 0.64      !  0.64 mm


! 3) Hard process : WW at 240 GeV
Beams:eCM = 240  ! CM energy of collision
WeakDoubleBoson:ffbar2WW = on

! 4) Settings for the event generation process in the Pythia8 library.
PartonLevel:ISR = on               ! no initial-state radiation
PartonLevel:FSR = on               ! no final-state radiation

! W decays to mu nu :
24:onMode    = off                 ! switch off W boson decays
24:onIfAny   = 13                  ! switch on W boson decay to muons

