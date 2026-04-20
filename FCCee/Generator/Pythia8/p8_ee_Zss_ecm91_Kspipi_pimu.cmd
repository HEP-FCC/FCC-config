! 1) Settings
Random:setSeed = on
Main:timesAllowErrors = 5

! 2) Output level
Main:numberOfEvents = 100000
Next:numberCount = 1000
Next:numberShowInfo = 1
Next:numberShowProcess = 1
Next:numberShowEvent = 0

! 3) Beam parameter settings (FCC-ee IDEA values)
Beams:idA = 11
Beams:idB = -11
Beams:allowMomentumSpread = off
Beams:allowVertexSpread = off
Beams:sigmaVertexX = 5.96e-3
Beams:sigmaVertexY = 23.8E-6
Beams:sigmaVertexZ = 0.397
Beams:sigmaTime = 10.89

! 4) Hard process: Z->ss at Ecm=91.188 GeV
Beams:eCM = 91.188
WeakSingleBoson:ffbar2gmZ = on
23:onMode = off
23:onIfAny = 3

! 5) Radiation
PartonLevel:ISR = on
PartonLevel:FSR = on

! 6) Decay Constraints
ParticleDecays:limitCylinder = on
ParticleDecays:xyMax = 2250.
ParticleDecays:zMax = 2500.

! 7) Force the KS to decay to two pions
310:oneChannel = 1 1.0 0 211 -211 

! 8) Force pions to decay to muons
 211:onMode = off
 211:addChannel = 1 1.0 0 13 14
 -211:onMode = off
 -211:addChannel = 1 1.0 0 -13 -14

! Main:numberOfEvents = 1000000

