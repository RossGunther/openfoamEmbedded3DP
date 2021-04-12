#!/usr/bin/env pvpython
'''Collecting line traces through the bath in vtk files. Scripting for many folders and many images and tables.'''

import os
import logging
import sys

from paraview.simple import * # import the simple module from the paraview

from paraview_line import csvfolder, convertToRelative

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

# load the virtual environment
virtualEnv = os.path.join(parentdir, 'env', 'Scripts', 'activate_this.py')
if sys.version_info.major < 3:
    execfile(virtualEnv, dict(__file__=virtualEnv))
else:
    exec(open(virtualEnv).read(), {'__file__': virtualEnv})
    
from config import cfg

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

__author__ = "Leanne Friedrich"
__copyright__ = "This data is publicly available according to the NIST statements of copyright, fair use and licensing; see https://www.nist.gov/director/copyright-fair-use-and-licensing-statements-srd-data-and-software"
__credits__ = ["Leanne Friedrich"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Leanne Friedrich"
__email__ = "Leanne.Friedrich@nist.gov"
__status__ = "Production"


#################################################################

#------------------------------

tlist = [1]        # times at which to collect the traces
xlist = [-0.001]      # positions at which to collect the trace

forceOverwrite = False # True to overwrite existing files

folders = []
nlist = range(0, 1000)   # list of nb folder numbers that we will search

SERVERFOLDER = cfg.path.server
topfolders = [os.path.join(SERVERFOLDER,'viscositysweep', s) for s in ['newtnewtsweep', 'HBnewtsweep', 'newtHBsweep', 'HBHBsweep']]
for topfolder in topfolders:
    for f in os.listdir(topfolder):
        if f.startswith('nb'):
            n1 = float(f[2:])
            if n1 in nlist:
                folders.append(os.path.join(topfolder, f))
                
logging.info(f'Exporting line traces.\nX positions: {[convertToRelative(x) for x in xlist]} mm behind nozzle.\nTime list: {tlist} s.\nFolders:{[os.path.basename(f) for f in folders]}')
                

for folder in folders:
    logging.debug('Checking '+folder)
    for xpos in xlist:
        csvfolder(folder, xpos, tlist, forceOverwrite=forceOverwrite)
print('Done exporting csv files')
 


