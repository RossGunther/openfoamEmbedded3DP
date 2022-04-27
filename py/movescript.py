#!/usr/bin/env python
'''Moves folders to server. Loops continuously.'''

# external packages
import os
import time
import socket
import sys

# local packages
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import foldermover as fm
import folderparser as fp
from config import cfg

# logging
LOGGERDEFINED = fp.openLog(os.path.realpath(__file__), LOGGERDEFINED)

# info
__author__ = "Leanne Friedrich"
__copyright__ = "This data is publicly available according to the NIST statements of copyright, fair use and licensing; see https://www.nist.gov/director/copyright-fair-use-and-licensing-statements-srd-data-and-software"
__credits__ = ["Leanne Friedrich"]
__license__ = "NIST"
__version__ = "1.0.0"
__maintainer__ = "Leanne Friedrich"
__email__ = "Leanne.Friedrich@nist.gov"
__status__ = "Production"

#---------------------------------------


SERVERFOLDER = os.path.join(cfg.path.server, 'yieldingsweep', 'HBHByielded')
CFOLDER = os.path.join(cfg.path.c, 'HBHByielded')
EFOLDER = os.path.join(cfg.path.e, 'HBHByielded')

if len(sys.argv)>1:
    waittime = float(sys.argv[1])
else:
    waittime = 0

fm.copyCtoServerFolders(SERVERFOLDER, CFOLDER,['k', 'n', 'tau0'], waittime, EFOLDER=EFOLDER)