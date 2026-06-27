! e+e- -> Z/gamma* -> qq (inclusive, all quark flavours d,u,s,c,b) at sqrt(s) = 91.188 GeV (FCC-ee)
Random:setSeed = on
Main:timesAllowErrors = 5

Init:showChangedSettings = on
Init:showChangedParticleData = off
Next:numberCount = 100
Next:numberShowInfo = 1
Next:numberShowProcess = 1
Next:numberShowEvent = 0

Beams:idA = 11
Beams:idB = -11
Beams:eCM = 91.188

WeakSingleBoson:ffbar2gmZ = on
23:onMode = off
23:onIfAny = 1 2 3 4 5

PartonLevel:ISR = on
PartonLevel:FSR = on

! old convention: decay only inside the tracking cylinder, keep the rest stable
ParticleDecays:limitCylinder = on
ParticleDecays:xyMax = 2250.
ParticleDecays:zMax = 2500.
