
module EDM4HepOutput EDM4HepOutput {
    add ReconstructedParticleCollections EFlowTrack EFlowPhoton EFlowNeutralHadron
    add GenParticleCollections           Particle
    add JetCollections                   Jet JetDurhamN2
    add MuonCollections                  Muon
    add ElectronCollections              Electron
    add PhotonCollections                Photon
    add MissingETCollections             MissingET GenMissingET
    set RecoParticleCollectionName       ReconstructedParticles
    set RecoMCParticleLinkCollectionName  RecoMCLink
}
