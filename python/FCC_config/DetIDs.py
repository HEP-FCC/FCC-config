#
# File: python/FCC_config/DetIDs.py
# Author: scott snyder <snyder@bnl.gov>
# Date: Jun, 2026
# Purpose: Helper to translate detector names to IDs.
#
# Works by reading the DetID constants from DectDimentions.xml.
#

import xml.etree.ElementTree as ET
import os

# All dictionaries we've read.
# Indexed by the compact file name, gives a dictionary of name->ID mappings.
_allDicts = {}

def _makeIdDict (flags):
    """Read detector ID mappings.

The file to read is found by looking for DectDimentions.xml in the same
directory as flags.compactFile."""    

    # Find and read the XML file.
    pathToDetector = os.path.dirname (flags.compactFile)
    xmlfile = os.path.join (pathToDetector, 'DectDimensions.xml')
    tree = ET.parse (xmlfile)
    root = tree.getroot()
    d = {}

    # Look for DetID constants.
    for constant in root.find('define').findall('constant'):
        name = constant.get('name')
        if name.startswith('DetID'):
            # Found one.  Find the corresponding ID and enter in the dictionary.
            val = int(constant.get('value'))
            d[name[6:]] = val

            # Special case.
            if name == 'DetID_Muon_Endcap_1':
                d[name[6:-2]] = val
    return d
                

def _detIdDict (flags):
    """Return the name->ID mapping for a particular compact file.

The configuration used is given by flags.compactFile."""

    compactFile = flags.compactFile
    if compactFile not in _allDicts:
        _allDicts[compactFile] = _makeIdDict (flags)
    return _allDicts[compactFile]


def detIDs (flags, ids):
    """Return detector IDs for a set of names.

ids can either be a single name, in which case a single ID is returned,
or a list of names, in which case a list of IDs is returned.

The configuration used is given by flags.compactFile."""

    d = _detIdDict (flags)
    if isinstance(ids, list):
        return [d[x] for x in ids]
    return d[ids]
