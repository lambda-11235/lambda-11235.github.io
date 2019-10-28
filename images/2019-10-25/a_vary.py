
import matplotlib.pyplot as plt

from common import *

samples = 10000

def alp(a):
    xs = [6*x/samples for x in range(samples)]
    ys = []

    mn = 5
    md = 5
    mx = 5

    for x in xs:
        y = foo(x, adjSin, 0.9*mn, md, 1.1*mx, a)
        ys.append(y)

        y = max(1, min(y, 8))

        mn = min(mn, y)
        mx = max(mx, y)
        md = mn + (mx - mn)*0.2

    return (xs, ys)

avs = [1, 2, 5, 10, 30, 100, 1000]

for i in range(len(avs)):
    (xs, ys) = alp(avs[i])
    plt.plot(xs, ys, color=(i/len(avs), 0, 1 - i/len(avs)))

plt.savefig("a_vary.png")

