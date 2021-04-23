#!/usr/bin/env python
'''Functions for plotting overall metrics, such as simulation time, folder name, simulation rate, cross-sectional area...'''

import sys
import os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import math
from typing import List, Dict, Tuple, Union, Any, TextIO
import logging

import folderparser as fp
import interfacemetrics as intm
from plot_general import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['font.size'] = 10

__author__ = "Leanne Friedrich"
__copyright__ = "This data is publicly available according to the NIST statements of copyright, fair use and licensing; see https://www.nist.gov/director/copyright-fair-use-and-licensing-statements-srd-data-and-software"
__credits__ = ["Leanne Friedrich"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Leanne Friedrich"
__email__ = "Leanne.Friedrich@nist.gov"
__status__ = "Production"

#-------------------------------------------

 

def plotSquare(ax:plt.Axes, x0:float, y0:float, dx:float, caption:str, color) -> None:
    '''plotSquare plots a square
    ax is axis to plot on
    x0 is the x position
    y0 is the y position
    dx is the spacing between xlist
    caption is the label
    color is the color of the circle'''
    if len(caption)>0:
        # calculate brightness of color
        l = 0.2126 * color[0] + 0.7152 * color[1] + 0.0722 * color[2]
        if l>0.4:
            txtcolor = 'black'
        else:
            txtcolor = 'white'
        ax.text(x0, y0, caption, horizontalalignment='center', verticalalignment='center', color=txtcolor)
    box = plt.Rectangle([x0-dx/2,y0-dx/2], dx, dx, color=color, ec=None)
    ax.add_artist(box)
    
    
def plotSS(ss:pd.DataFrame, column:str, tmin:float) -> None:
    '''plot slice summaries. produces a row of 2 plots: column as a function of x and as a function of time
    ss is a dataframe of slice summary data, e.g. as imported by importSS or created by summarize
    column is the column name, e.g. 'centery'
    tmin is the minimum time to include in these plots'''
    size=4
    ss2 = ss[ss['time']>=tmin]
    fig, axes = plt.subplots(nrows=1, ncols=2, sharex=False, figsize=(10, 4))
    p = ss2.plot.scatter(x='xbehind', y=column, c='time', legend=False, ax=axes[0], colormap = 'RdBu')
    axes[0].set_xlabel('Position (mm)')
    axes[0].set_ylabel(column)   
    p = ss2.plot.scatter(x='time', y=column, c='x', legend=False, ax=axes[1], colormap = 'RdBu')
    axes[1].set_xlabel('Time (s)')
    axes[1].set_ylabel(column)
    
      

#------------------------------------------
# text plot, shows which folders correspond to which viscosities    


def txtPlot(folder:str, cp:folderPlots, dt:float) -> None:
    '''txtPlot assigns a single folder to the plot
    folder is a full path name
    cp is a comboPlot object
    dt is the spacing between text items. A good value is 0.2'''
    try:
        [color, x0, y0, sigmapos] = vvplot(folder, cp) # find the position of this plot within the big plot
    except Exception as e:
        return
    xmid = x0
    ymid = y0+dt*(sigmapos-1) # xmid and ymid are positions in the plot
    b = os.path.basename(folder)
    if cp.split:
        axnum = sigmapos
    else:
        axnum = 0
    cp.axs[axnum].text(xmid, ymid, b, horizontalalignment='center', verticalalignment='center', c=color) # put the folder name on the plot
   
    
def txtPlots0(topFolder:str, exportFolder:str, overwrite:bool=False, **kwargs) -> None:
    '''write names of a list of folders on one big plot
    topFolder is the folder that holds all of the folders
    exportFolder is the folder to export the figure to
    overwrite true to overwrite existing files'''
    labeli = 'names'
    fn = intm.imFn(exportFolder, labeli, topFolder, **kwargs)
    if not overwrite and os.path.exists(fn+'.png'):
        return
    cp = comboPlot(topFolder, [-0.6, 0.6], [-0.6, 0.6], 6.5, **kwargs)
    if cp.split:
        dt = 0
    else:
        dt = 0.2
        
    for folder in cp.flist:
        txtPlot(folder, cp, dt)
    cp.figtitle = 'Folder names'
    cp.clean()

    intm.exportIm(fn, cp.fig)

#------------------------------------------   
# run time plot: how long the simulation ran in simulation seconds


def runtimePlot(folder:str, cp:folderPlots, dt:float) -> None:
    '''runtimePlot assigns a single folder to the plot
    folder is a full path name
    cp is a comboPlot object
    dt is the spacing between text items. A good value is 0.2'''
    try:
        [color, x0, y0, sigmapos] = vvplot(folder, cp) # find the position of this plot within the big plot
    except:
        return
    xmid = x0
    ymid = y0+dt*(sigmapos-1) # xmid and ymid are positions in the plot
    b = fp.currentTime(folder)
    if cp.split:
        axnum = sigmapos
    else:
        axnum = 0
    cp.axs[axnum].text(xmid, ymid, b, horizontalalignment='center', verticalalignment='center', c=color) # put the folder name on the plot
   
    
def runtimePlots0(topFolder:str, exportFolder:str, overwrite:bool=False, **kwargs) -> None:
    '''write names of a list of folders on one big plot
    topFolder is the folder that holds all of the folders'''
    labeli = 'runtime'
    fn = intm.imFn(exportFolder, labeli, topFolder, **kwargs)
    if not overwrite and os.path.exists(fn+'.png'):
        return
    cp = comboPlot(topFolder, [-0.6, 0.6], [-0.6, 0.6], 6.5, **kwargs)
    dt = 0.2
    for folder in cp.flist:
        runtimePlot(folder, cp, dt)
    cp.figtitle = 'Run times'
    cp.clean()
    intm.exportIm(fn, cp.fig)
    
 #------------------------------------------   
#### generic value plots

def valueCaption(val:str, tmax:str, tmin:str) -> str:
    '''Caption that shows the value, with an appropriate number of decimals. If the val is outside the captioning region, don't generate a caption. If the val is large or tmax is large, use 0 decimals. If they are small, use 2.'''
    if math.isnan(val):
        return ''
    if val>=tmax or val<=tmin:
        if val>10 or tmax>100:
            caption='%2.0f'%(val)
        else:
            caption = '%1.2f'%(val)
    else:
        caption = ''
    return caption
        
        
def plotTableVals(t1:pd.DataFrame, cp:comboPlot, tminmode:int, timeplot:bool=False) -> Dict:
    '''Plot a list of values on a comboPlot using either circle size plot or color density plot. 
    t1 is a dataframe made from timePlot outputs
    cp is the comboPlot to plot the values on
    tminmode=0 to set the minimum to 0. tminmode=1 to set the minimum to the min value in the table.
    timeplot true if we are plotting times. This is necessary for circle scaling.'''
    
    if len(t1)<1:
        raise ValueError
    if 'tmin' in cp.kwargs:
        tmin = cp.kwargs['tmin']
    else:
        if tminmode==0:
            tmin = 0
        else:
            tmin = t1['rate'].min()
    if 'tmax' in cp.kwargs:
        tmax = cp.kwargs['tmax']
    else:
        tmax = t1['rate'].max()
    
        
    t1 = t1.sort_values(by=['rate'])
    t1 = t1.reset_index()

    
    # set circle size
    if not cp.split:
        rmax = cp.dx/2 # maximum radius of circle is the spacing between points/2
        if tmax>(100*t1['rate'].median()) or timeplot:
            rmax = rmax*np.sqrt(tmax/500)
    #         rmax = rmax*(tmax/(100*t1['rate'].median()))

    
    #cmap = sns.cubehelix_palette(as_cmap=True, rot=-0.4)
    cmap = sns.diverging_palette(220, 20, as_cmap=True)
    #cmap = sns.cubehelix_palette(as_cmap=True)
    # label only evenly spaced across values
    spacing = max(float(np.floor(len(t1)/20)),1)
    dummy = tmin
    for index,t in t1.iterrows():
        if float(index)%spacing==0 or cp.split:
            dummy = t['rate']
        caption = valueCaption(t['rate'], tmax, dummy)
        val = (t['rate']-tmin)/(tmax-tmin) # actual value, normalized to range
        
        if cp.split:
            if val>1:
                color = [138/256, 75/256, 60/256]
            elif val<0:
                color = [33/256, 85/256, 101/256]
            else:
                color = cmap(val)
            sp = t['sigmapos']
            if sp<len(cp.axs):
                ax = cp.axs[t['sigmapos']]
                plotSquare(ax, t['x0'], t['y0'], cp.dx, caption, color)
        else:
            ax = cp.axs[0] 
            plotCircle(ax, t['x0'], t['y0'], np.sqrt(val)*rmax, caption, t['color'], sigmapos=t['sigmapos'])

    return {'tmin':tmin, 'tmax':tmax, 'cmap':cmap}


def folderToPlotVals(folder:str, cp, rate) -> Dict:
    '''this is the output dictionary for a timePlot or metricPlot entry from one simulation
    folder is a full path name
    cp is a comboPlot object
    rate is a value to plot'''
    try:
        color, x0, y0, sigmapos = vvplot(folder, cp) # find the position of this plot within the big plot
    except:
        raise ValueError
    return {'color':color, 'x0':x0, 'y0':y0, 'rate':rate, 'sigmapos':sigmapos}


def plotAllFolderVals(function, cp:comboPlot, tminmode:int, timeplot:bool=False) -> Dict:
    '''Go through all of the folders in the folder list stored in cp, and construct a table of values to plot.
    function is the function to use on each folder. Usually some variation on folderToPlotVals
    tminmode is 0 to use 0 as the min value, 1 to use the min value in the table as min value for choosing colors
    timeplot=True if we are plotting simulation rates. Important for circle size scaling.'''
    t1 = []
    for f in cp.flist:
        try:
            row = function(f, cp)
            #row = metricPlot(f, cp, time, xbehind, label)
        except NameError as n:
            raise n
        except Exception as e:
            pass
        else:
            t1.append(row)
    t2 = pd.DataFrame(t1)
    t2 = t2.dropna()
    return plotTableVals(t2, cp, tminmode, timeplot)
    
def valueLegend(cp:comboPlot, vpout:Dict) -> None:
    '''Put a color legend for the gradient plot on the bottom'''
    if cp.split:
        cbaxes = cp.fig.add_axes([0.2, 0.1, 0.6, 0.05])
        nm = plt.Normalize(vmin=vpout['tmin'], vmax=vpout['tmax'])
        sm = plt.cm.ScalarMappable(cmap=vpout['cmap'], norm=nm)
        plt.colorbar(sm, cax=cbaxes, orientation="horizontal")



#------------------------------------------
# time plots: how fast the simulation ran, in real hr per simulation s
        

def timePlot(folder:str, cp:comboPlot):
    '''timePlot determines the position and size of circle to plot
    folder is a full path name
    cp is a comboPlot object'''
    
    le = intm.importLegend(folder)
    rate = float((le[le['title']=='simulation rate (hr/s)']).val) # find the simulation rate
    return folderToPlotVals(folder, cp, rate) 
       
       

def timePlots(topFolder:str, exportFolder:str, overwrite:bool=False, **kwargs) -> None:
    '''timePlots plots computation rates as circles
    topFolder is a full path name to the folder containing all the simulations
    exportFolder is the folder to export the plot to'''
    
    labeli = 'simrate'
    fn = intm.imFn(exportFolder, labeli, topFolder, **kwargs)  # file name for the plot
    if not overwrite and os.path.exists(fn+'.png'):            # quit if this plot already exists and overwrite==False
        return
    
    cp = comboPlot(topFolder, [-0.6, 0.6], [-0.6, 0.6], 6.5, **kwargs)  # create a plot
    lfunc = lambda folder, cp: timePlot(folder,cp)                      # we are going to run timePlot on every folder
    try:
        vpout = plotAllFolderVals(lfunc, cp, 0, timeplot=True)          # plot all the files
    except:
        return
    cp.figtitle = 'Simulation time (real hr/simulation s)'
    cp.clean()                  # clean up the plot
    valueLegend(cp, vpout)      # add a color legend
    intm.exportIm(fn, cp.fig)   # export figure


#------------------------------------------  
# slice summary metrics plots


def metricVals(folder:str, time:float, xbehind:float, labels:List[str]) -> Dict:
    '''Find the value of slice summary metrics for a single simulation.
    folder is the full path name to a simulation folder
    time is the time of the slice
    xbehind is the position of the slice, relative to the center of the nozzle
    labels is a list of metrics to collect, e.g. ['area', 'centery']'''
    
    if not os.path.exists(folder):
        raise ValueError

    le, units = intm.importSS(folder)
        # get slice summaries
    if len(le)<2:
        raise ValueError
    xreal = intm.closest(le['xbehind'], xbehind) 
        # this is the actual x value that we measured that's 
        # closest to the one we're asking for
        
    if abs(xreal-xbehind)>0.2:
        # if the x value is too far away, abort
        raise ValueError
        
    row = le[(le['xbehind']==xreal) & (le['time']==time)] 
        # select the slice summary at the position and time we asked for
    if not len(row)==1:
        raise ValueError
    try:
        rates = {label:row.iloc[0][label] for label in labels}
        # find the value of the metric we're looking for
    except:
        logging.debug(folder)
        raise NameError
    return rates



def metricPlot(folder:str, cp:comboPlot, time:float, xbehind:float, label:str) -> Dict:
    '''metricPlot determines the position and size of circle or square to plot
    folder is a full path name
    cp is a comboPlot object
    time is the time since extrusion started in s
    xbehind is the distance behind the center of the nozzle in mm
    label is the column label, e.g. 'maxz'.
    '''
    
    try:
        rate = metricVals(folder, time, xbehind, [label])
        rate = rate[label]
    except Exception as e:
        raise e
    return folderToPlotVals(folder, cp, rate)
       
        

def metricPlots(topFolder:str, exportFolder:str, time:float, xbehind:float, label:str, overwrite:bool=False, **kwargs) -> None:
    '''# metricPlots plots slice summaries as color density plots
    topFolder is a full path name to the folder containing all the simulations
    exportFolder is the folder to export plots to
    time is the time since extrusion started in s
    xbehind is the distance behind the center of the nozzle in mm
    label is the column label, e.g. 'maxz' '''
    
    labeli = label+'_'+str(xbehind)+'_t_'+str(time)
    fn = intm.imFn(exportFolder, labeli, topFolder, **kwargs)
    if not overwrite and os.path.exists(fn+'.png'):
        return
    
    cp = comboPlot(topFolder, [-0.6, 0.6], [-0.6, 0.6], 6.5, gridlines=False, **kwargs)
    lfunc = lambda f, cp: metricPlot(f, cp, time, xbehind, label)
    
    try:
        vpout = plotAllFolderVals(lfunc, cp, 1) # use tminmode 1 so the min of the color map is the min of the metric
    except Exception as e:
        logging.error(str(e))
        return
    cp.figtitle = label+', '+str(xbehind)+' mm behind nozzle, t = '+str(time)+' s'
    cp.clean()
    valueLegend(cp, vpout)
    intm.exportIm(fn, cp.fig)