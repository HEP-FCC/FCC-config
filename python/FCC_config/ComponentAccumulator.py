#
# File: python/FCC_config.ComponentAccumulator.py
# Author: scott snyder <snyder@bnl.gov>
# Date: Feb, 2026
# Purpose: ComponentAccumulator-style configuration for key4hep.
#

"""This module provides a ComponentAccumulator class for structured
configuration, along the lines of ATLAS (see
https://doi.org/10.1051/epjconf/201921405015 and section 3.2 of
https://doi.org/10.1140/epjc/s10052-024-13701-w).
Only the bare minimum required to try this out is implemented at this point;
in particular, component de-duplication is not implemented (except for an
ad-hoc facility for Services, see below).  More functionality from ATLAS
can be added as needed.

key4hep configurations have tended to be monolithic python scripts.
For any significant configuration, maintaining this gets tedious and
error-prone, and results in large amounts of duplicated configuration code,
making it complicated to introduce changes in how components get configured.

In this model, components are configured via configuration functions,
which ideally are provided via by the library defining the components.
Each function creates Gaudi Configurables for one component or a set of
closely related components and returns them via a ComponentAccumulator object.
These functions have no access to global state, taking all their information
via arguments; however, their first argument is conventionally a flags
object conveying information about what sort of configuration is desired.

As an example, a configuration function might look something like this:

  from FCC_config.ComponentAccumulator import ComponentAccumulator
  import Configurables as C
  def PairCaloClustersPi0Cfg (flags, inputClusters, clusterNameRoot):
      cfg = ComponentAccumulator()
      alg = C.PairCaloClustersPi0('resolvedPi0FromClusterPair' + clusterNameRoot,
                                  inClusters = inputClusters,
                                  unpairedClusters = 'Unpaired' + inputClusters,
                                  pairedClusters  = 'Paired' + inputClusters,
                                  reconstructedPi0 = 'ResolvedPi0Particle' + clusterNameRoot,
                                  massPeak = flags.CaloTopo.pi0MassPeak,
                                  massLow  = flags.CaloTopo.pi0MassLow,
                                  massHigh = flags.CaloTopo.pi0MassHigh)
      cfg.addAlg(alg)
      return cfg

One can then create the needed flags structure like this:

  class Flags:
      pass
  flags = Flags()
  flags.CaloTopo = Flags()
  flags.CaloTopo.pi0MassPeak = 0.122201
  flags.CaloTopo.pi0MassLow  = 0.0754493
  flags.CaloTopo.pi0MassHigh = 0.153543

and then use it like:

  cfg = ComponentAccumulator()
  cfg.merge (PairCaloClustersPi0Cfg (flags,
                                     'AugmentedEMBCaloTopoClusters',
                                     'EMBCaloTopoClusters'))
  cfg.merge (...)
  cfg.toVars (TopAlg, ExtSvc)


Service merging
---------------

As mentioned above, the de-duplication which is a key part of the ATLAS
configuration is not yet implemented here.  In fact, it cannot really be
implemented with the original Gaudi Configurable classes that key4hep
still uses, in which Configurables are regarded as singletons based
on the component name; GaudiConf2 is required to do it sensibly.

Nevertheless, there are a few places where this sort of functionality
is really needed, such as the IOSvc, where we want to accumulate the
output commands.  We can kind of so this on an ad-hoc basis like this:

 - Create a wrapper class to hold the configuration interface for the Service,
   but which it not itself a Configurable.  It should, however, define
   a name() method.

 - Define a mergeTo() method.  When a Service with a duplicate name is called,
   mergeTo is called on the object being added, with the existing object
   passed as an argument.  If the two can the merged, then mergeTo should
   update the existing object and return True.  Otherwise, it should
   return False.

 - Define a convertTo() method, which will create the corresponding
   Configurable.  This will be called when toVars is called.
"""


def _mergeSvc (old, new):
    """Helper for merging services.

    Test if we can merge together Services old and new.
    If so, modify old accordingly and return True.
    Otherwise, return False.
    """
    mergef = getattr (new, 'mergeTo', None)
    if not mergef or not callable(mergef):
        return False
    return mergef (old)


class ComponentAccumulator:
    """Basic ComponentAccumulator functionality. xxx
    """


    def __init__ (self):
        """Make an empty ComponentAccumulator."""

        return self.__reset()


    def __reset (self):
        """Clear the state of this ComponentAccumulator."""

        # Algorithms in sequence order.
        self._algSeq = []

        # Map from algorithm names to algorithms.
        self._algs = {}

        # Map from service name to services.
        self._svcs = {}
        return


    def addAlg (self, a):
        """Add a new Algorithm.

        There must be no existing algorithm with the same name.
        """
        
        if a.name() in self._algs:
            print ('ERROR: Duplicate algorithm', a.name())
            assert 0
        self._algSeq.append(a)
        self._algs[a.name()] = a
        return

    
    def algs (self):
        """Return the list of accumulated Algorithms."""
        return self._algSeq


    def addSvc (self, s):
        """Add a new Service.

        There must be no existing Service with the same name, unless
        it is mergable as discussed above.
        """

        if s.name() in self._svcs:
            if not _mergeSvc (self._svcs[s.name()], s):
                print ('ERROR: Unmergable duplicate service', s.name())
                assert 0
        else:
            self._svcs[s.name()] = s
        return


    def svcs (self):
        """Return the list of accumulated Services."""

        return list(self._svcs.values())


    def merge (self, other):
        """Merge another ComponentAccumulator into this one.

        There must be no duplicate Algorithms or Services (except for
        mergable Services, as discussed above).
        """
        for a in other.algs():
            self.addAlg (a)
        for s in other.svcs():
            self.addSvc (s)
        return


    def toVars (self, topAlg, extSvc):
        """Merge contents into AppMgr variables.

        topAlg and extSvc are the ApplicationMgr's lists of Algorithms
        and Services.  The ones we hold will be appended.  Duplicates are
        errors, except for mergable Services as discussed above.
        If a Service object we hold defines convertTo, then we call that
        and use that as the result.

        After this call, the state of this object is reset.
        """
        for a in topAlg:
            if a.name() in self._algs:
                print ('ERROR: Duplicate algorithm', a.name())
                assert 0
        topAlg += self.algs()

        for s in extSvc:
            sname = s if isinstance(s, str) else s.name()
            if sname in self._svcs:
                if _mergeSvc (s, self._svcs[sname]):
                    del self._svcs[sname]
                else:
                    print ('ERROR: Unmergable duplicate service', sname)
                    assert 0
        for sname, s in self._svcs.items():
            cnv = getattr (s, 'convertTo', None)
            if cnv and callable(cnv):
                s = cnv()
            extSvc.append(s)

        return self.__reset()
