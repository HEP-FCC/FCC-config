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

! 4) Hard process : Z->qqbar at Ecm=91 GeV
Beams:eCM = 91.188  ! CM energy of collision


WeakSingleBoson:ffbar2gmZ = on
23:onMode = off
23:onIfAny = 4

PartonLevel:ISR = on               ! initial-state radiation
PartonLevel:FSR = on               ! final-state radiation

! turn off hadronization
HadronLevel:all = off
! The hadronization is forced by evtgen interface

! turn off all c hadron decays
411:onMode = off  ! D+
421:onMode = off  ! D0
431:onMode = off  ! Ds+
4122:onMode = off
4222:onMode = off
4212:onMode = off
4112:onMode = off
4224:onMode = off
4214:onMode = off
4114:onMode = off
4232:onMode = off
4132:onMode = off
4322:onMode = off
4312:onMode = off
4324:onMode = off
4314:onMode = off
4332:onMode = off
4334:onMode = off
4412:onMode = off
4422:onMode = off
4414:onMode = off
4424:onMode = off
4432:onMode = off
4434:onMode = off
4444:onMode = off

