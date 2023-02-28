Random:setSeed = on
Main:numberOfEvents = 1000         ! number of events to generate
Main:timesAllowErrors = 5          ! how many aborts before run stops

! 2) Settings related to output in init(), next() and stat().
Init:showOneParticleData = 24	   ! to check the decay channel numbers for W->mu and W->tau
Init:showChangedSettings = on      ! list changed settings
Init:showChangedParticleData = off ! list changed particle data
Next:numberCount = 1000             ! print message every n events
Next:numberShowInfo = 1            ! print event information n times
Next:numberShowProcess = 1         ! print process record n times
Next:numberShowEvent = 0          ! print event record n times


Beams:idA = 11                   ! first beam, e+ = 11
Beams:idB = -11                   ! second beam, e- = -11

Beams:allowMomentumSpread  = off

! Vertex smearing :
Beams:allowVertexSpread = on
Beams:sigmaVertexX = 9.80e-3   !  9.80 mum
Beams:sigmaVertexY = 25.4E-6   !  25.4 nm
Beams:sigmaVertexZ = 0.64      !  0.64 mm


! 3) Hard process : WW at 240 GeV
Beams:eCM = 240  ! CM energy of collision
WeakDoubleBoson:ffbar2WW = on

! 4) Settings for the event generation process in the Pythia8 library.
PartonLevel:ISR = on               ! no initial-state radiation
PartonLevel:FSR = on               ! no final-state radiation

! W decays to e and to taus :
24:onMode    = off                 ! switch off W boson decays
24:onIfAny   = 11                  ! switch on W boson decay to electrons or taus
24:onIfAny   = 15

! To ensure the proper mixture of W -> mu and W -> tau -> mu :
! (the BRs are internally rescaled such that the sum is one)
24:6:bRatio  = 1. 		! W -> e
24:8:bRatio  = 0.1739		! W  -> tau  x  tau -> mu
24:6:meMode  = 100		! set meMode = 100 so that
24:8:meMode  = 100              ! branching ratios are not overwritten at initialization
24:0:bRatio  = 0 
24:1:bRatio  = 0
24:2:bRatio  = 0
24:3:bRatio  = 0
24:4:bRatio  = 0
24:5:bRatio  = 0
24:7:bRatio  = 0
24:0:meMode  = 100
24:1:meMode  = 100
24:2:meMode  = 100
24:3:meMode  = 100
24:4:meMode  = 100
24:5:meMode  = 100
24:7:meMode  = 100


! tau decays to muons only :
15:onMode   = off
15:onIfAny  = 11		!    tau  -> e

