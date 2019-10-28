
from math import *

def adjSin(x):
    return (sin(pi*x - pi/2)+1)/2

def foo(x, g, mn, md, mx, a):
    return md + (mx - md)/((a*(1 - g(x)))**2 + 1) + (mn - md)/((a*g(x))**2 + 1)
