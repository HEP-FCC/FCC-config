! main03.cmnd.
! This file contains commands to be read in for a Pythia8 run.
! Lines not beginning with a letter or digit are comments.
! Names are case-insensitive  -  but spellings-sensitive!
! The settings here are illustrative, not always physics-motivated.

! 1) Settings used in the main program.
Random:setSeed = on
Main:timesAllowErrors = 5          ! how many aborts before run stops

! 2) Settings related to output in init(), next() and stat().
Init:showChangedSettings = on      ! list changed settings
Init:showChangedParticleData = off ! list changed particle data
Next:numberCount = 10000             ! print message every n events
Next:numberShowInfo = 1            ! print event information n times
Next:numberShowProcess = 1         ! print process record n times
Next:numberShowEvent = 0           ! print event record n times

! 3) Beam parameter settings. Values below agree with default ones.
Beams:idA = 11                   ! first beam, e = 2212, pbar = -2212
Beams:idB = -11                   ! second beam, e = 2212, pbar = -2212

! Beam energy spread: 0.132% x 45.594 GeV = 0.0602 GeV
Beams:allowMomentumSpread  = on
Beams:sigmaPzA = 0.0602
Beams:sigmaPzB = 0.0602

! Vertex smearing :
Beams:allowVertexSpread = on
Beams:sigmaVertexX = 4.50e-3   !  6.4 mum / sqrt2
Beams:sigmaVertexY = 20.0E-6   !  28.3 nm / sqrt2
Beams:sigmaVertexZ = 0.30      !  0.30 mm


! 4) Hard process : Z->qqbar at Ecm=91 GeV
Beams:eCM = 91.188  ! CM energy of collision


WeakSingleBoson:ffbar2gmZ = on
23:onMode = off
23:onIfAny = 5

PartonLevel:ISR = on               ! initial-state radiation
PartonLevel:FSR = on               ! final-state radiation


! turn off hadronization
HadronLevel:all = off
! The hadronization is forced by evtgen interface

! turn off all B hadron decays
511:onMode = off
521:onMode = off
531:onMode = off
541:onMode = off
5122:onMode = off
5132:onMode = off
5142:onMode = off
5232:onMode = off
5242:onMode = off
5332:onMode = off
5342:onMode = off
5412:onMode = off
5414:onMode = off
5422:onMode = off
5424:onMode = off
5432:onMode = off
5434:onMode = off
5442:onMode = off
5444:onMode = off
5512:onMode = off
5514:onMode = off
5522:onMode = off
5524:onMode = off
5532:onMode = off
5534:onMode = off
5542:onMode = off
5544:onMode = off
5544:onMode = off

