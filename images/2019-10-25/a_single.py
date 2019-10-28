
import matplotlib.pyplot as plt

from common import *


xs = [x/100 for x in range(1000)]
ys = []

mn = 5
md = 5
mx = 5

for x in xs:
    y = foo(x, adjSin, 0.9*mn, md, 1.1*mx, 100)
    ys.append(y)

    y = max(1, min(y, 8))

    mn = min(mn, y)
    mx = max(mx, y)
    md = mn + (mx - mn)*0.2

plt.plot(xs, ys)
plt.savefig("a_single.png")
