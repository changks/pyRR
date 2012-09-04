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
from numpy import exp, log10, linspace
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
    x =  [0.08, 0.50, 1.25, 2, 4, 6.3, 8, 12.5, 16, 40]
    y = [95.61, 87.71, 82.45, 79.78, 73.28, 66.98, 63.21, 55.4, 49.91, 23.95]
    k, n = FitRR(x,y)
    s ='k = %.2f, n = %.2f' % (k, n)

    rrx = linspace(min(x),max(x),num=50,endpoint=True)
    rry = RosinRammler(rrx,k,n)

    pyplot.plot(x, y, 'ro')
    pyplot.plot(rrx,rry,'g-')

    mscale.register_scale(RRYScale)
    pyplot.grid(b=True,which='major',axis='y')
    pyplot.grid(b=True,which='both',axis='x')
    pyplot.axis([10**-2,10**2,0.1,99.8])
    pyplot.gca().set_yscale('rry')
    pyplot.gca().set_xscale('log')
    pyplot.gca().invert_yaxis()

    pyplot.text(10**-1.7,9,s)
    pyplot.xlabel('Size [mm]')
    pyplot.ylabel('Retained on Screen [%]')
    pyplot.title('Rosin-Rammler Plot')

    pyplot.show()
