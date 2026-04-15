#!/usr/bin/env python


class TestAlg:
    def __init__ (self, name):
        self._name = name
        return

    def name (self):
        return self._name


class TestSvc:
    def __init__ (self, name):
        self._name = name
        return

    def name (self):
        return self._name


class TestSvc2:
    def __init__ (self, name, xlist = []):
        self._name = name
        self.xlist = xlist
        return

    def name (self):
        return self._name


    def mergeTo (self, other):
        for x in self.xlist:
            if not x in other.xlist:
                other.xlist.append (x)
            else:
                return False
        return True


    def convertTo (self):
        return self.xlist


def _catest1():
    """ComponentAccumulator test 1
    >>> from FCC_config.ComponentAccumulator import ComponentAccumulator
    >>> ca1 = ComponentAccumulator()
    >>> alg1 = TestAlg ('alg1')
    >>> ca1.addAlg (alg1)
    >>> assert len(ca1.algs()) == 1
    >>> assert ca1.algs()[0] is alg1
    >>> try:
    ...   ca1.addAlg (TestAlg('alg1'))
    ... except (AssertionError):
    ...   print ('caught')
    ERROR: Duplicate algorithm alg1
    caught
    >>> svc1 = TestSvc ('svc1')
    >>> ca1.addSvc (svc1)
    >>> assert len(ca1.svcs()) == 1
    >>> assert ca1.svcs()[0] == svc1
    >>> try:
    ...   ca1.addSvc (TestAlg('svc1'))
    ... except (AssertionError):
    ...   print ('caught')
    ERROR: Unmergable duplicate service svc1
    caught
    >>> ca2 = ComponentAccumulator()
    >>> alg2 = TestAlg ('alg2')
    >>> ca2.addAlg (alg2)
    >>> assert len(ca2.algs()) == 1
    >>> assert ca2.algs()[0] is alg2
    >>> svc2 = TestSvc ('svc2')
    >>> ca2.addSvc (svc2)
    >>> assert len(ca2.svcs()) == 1
    >>> assert ca2.svcs()[0] == svc2
    >>> ca1.merge (ca2)
    >>> assert len(ca1.algs()) == 2
    >>> assert ca1.algs()[0] is alg1
    >>> assert ca1.algs()[1] is alg2
    >>> assert len(ca1.svcs()) == 2
    >>> assert ca1.svcs()[0] == svc1
    >>> assert ca1.svcs()[1] == svc2
    >>> try:
    ...   ca1.merge (ca2)
    ... except (AssertionError):
    ...   print ('caught')
    ERROR: Duplicate algorithm alg2
    caught
    >>> topAlg = []
    >>> extSvc = []
    >>> ca1.toVars (topAlg, extSvc)
    >>> assert topAlg == [alg1, alg2]
    >>> assert extSvc == [svc1, svc2]
    >>> try:
    ...   ca2.toVars (topAlg, extSvc)
    ... except (AssertionError):
    ...   print ('caught')
    ERROR: Duplicate algorithm alg2
    caught
    >>> ca3 = ComponentAccumulator()
    >>> ca3.addSvc (svc2)
    >>> try:
    ...   ca3.toVars (topAlg, extSvc)
    ... except (AssertionError):
    ...   print ('caught')
    ERROR: Unmergable duplicate service svc2
    caught
    """

def _catest2():
    """ComponentAccumulator test 2
    >>> from FCC_config.ComponentAccumulator import ComponentAccumulator
    >>> ca1 = ComponentAccumulator()
    >>> svc1a = TestSvc2 ('svc1', [1, 2])
    >>> svc1b = TestSvc2 ('svc1', [3, 4]) 
    >>> ca1.addSvc (svc1a)
    >>> ca1.addSvc (svc1b)
    >>> assert len(ca1.svcs()) == 1
    >>> assert ca1.svcs()[0].name() == 'svc1'
    >>> assert ca1.svcs()[0].xlist == [1,2,3,4]
    >>> svc1c = TestSvc2 ('svc1', [4, 5]) 
    >>> try:
    ...   ca1.addSvc (svc1c)
    ... except (AssertionError):
    ...   print ('caught')
    ERROR: Unmergable duplicate service svc1
    caught
    >>> topAlg = []
    >>> extSvc = []
    >>> ca1.toVars (topAlg, extSvc)
    >>> assert topAlg == []
    >>> assert extSvc == [[1,2,3,4]]
    """


import doctest
doctest.testmod()
