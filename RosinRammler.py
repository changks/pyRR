#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      user19
#
# Created:     04/09/2012
# Copyright:   (c) user19 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from scipy.optimize import curve_fit
from numpy import exp, log10
from matplotlib import pyplot
from matplotlib import scale as mscale
from RRYScale import RRYScale

def RosinRammler(x,k,n):
    return 100*exp(-(x/k)**n)

def FitRR(x,y):
    popt, pcov = curve_fit(RosinRammler,x,y)
    k, n = popt[0], popt[1]
    return k, n

def Pass2Retain(PP):
    return [PP[0] - x for x in PP]

if __name__ == '__main__':
    x =  [float(x) for x in [70.0, 50.0, 32.0,20.0,6.3,1.0,0.0]]
    y = [float(y) for y in Pass2Retain([100.0,94.2,80.2,59.4,28.2,4.5,0.0])]
##    k, n = FitRR(x,y)
    k, n = 20.23, 1.04
    print 'k = %s, n = %s' % (k, n)

    mscale.register_scale(RRYScale)
    pyplot.gca().set_yscale('rry')
    pyplot.gca().set_xscale('log')
    pyplot.plot(x, y, 'ro')
    pyplot.show()