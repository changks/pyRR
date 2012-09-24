#-------------------------------------------------------------------------------
# Name:        RRPlotter.py
# Purpose:     Function to fit and plot a RR curve
#
# Author:      Tom Robinson
#
# Created:     04/09/2012
# Copyright:   (c) Tom Robinson 2012
#-------------------------------------------------------------------------------

from scipy.optimize import curve_fit
from numpy import *
from matplotlib import pyplot
from matplotlib import scale as mscale
from RRYScale import RRYScale
from tempfile import mkstemp
from os import close


def RosinRammler(x,k,n):
    return 100*exp(-(x/k)**n)


def FitRR(x,y):
    popt, pcov = curve_fit(RosinRammler,x,y)
    k, n = popt[0], popt[1]
    return k, n


def Pass2Retain(PP):
    return [PP[0] - x for x in PP]


def AddPoints(x,y,yname):
    pyplot.hold(True)
    pyplot.plot(x, y, marker='.', label=str(yname[0]))


def AddTrend(rrx,rry,yname):
    pyplot.hold(True)
    pyplot.plot(rrx, rry, marker='--', label=str(yname[0]))


def PlotSetXRange(x):
    minex = (log10(min(x))+(-log10(min(x))%1))//1 - 1 # Always round up then take 1
    maxex = log10(max(x))//1 + 1 #Always round down then add 1
    pyplot.axis([10**minex,10**maxex,0.1,99.8])


def PlotSetScale():
    mscale.register_scale(RRYScale)
    pyplot.grid(b=True,which='major',axis='y')
    pyplot.grid(b=True,which='both',axis='x')
    pyplot.gca().set_yscale('rry')
    pyplot.gca().set_xscale('log')
    pyplot.gca().invert_yaxis()


def PlotSetAnotation():
    pyplot.xlabel('Screen Size [mm]')
    pyplot.ylabel('Retained on Screen [%]')
    pyplot.title('Rosin-Rammler Plot')
    pyplot.legend(loc=0, borderaxespad=0.5,
        prop={'size':10},fancybox=True, shadow=True, ncol=2)


def PlotAddData(x,y,yname,trend):
    for yi, ynamei in zip(y, yname):
        AddPoints(x,yi,ynamei)
        if trend == True:
            k, n = FitRR(x,yi)
            rrx = linspace(min(x),max(x),num=50,endpoint=True)
            rry = RosinRammler(rrx,k,n)
            rryname = ynamei[0] + ' RR Trend'
            AddTrend(rrx, rry, rryname)


def PlotRR(x, y, yname = [['Size Distribution']], trend = False, passing = True):
    f, fn = mkstemp(suffix='.png')
    PlotAddData(x, y, yname, trend)
    PlotSetXRange(x)
    PlotSetScale()
    PlotSetAnotation()
    #pyplot.show()
    pyplot.savefig(fn,dpi=300,format='png',
        bbox_inches='tight',pad_inches=0.1)
    close(f)
    pyplot.clf()
    return fn


if __name__ == '__main__':
    x = [[50,11.2,3,1,0.125]]
    y =[[0,2.6,16.5,31.8,42.9],[0,18.1,35.3,46.6,56.8],[0,28.2,53.9,63.1,74.3]]
    yname = [['Roto North'],['Roto South #1'],['Roto South #2']]
    print PlotRR(x[0], y, yname)
