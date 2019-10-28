
import matplotlib.pyplot as plt

from common import *


xs = [x/1000 - 1 for x in range(3000)]
ys = []

for x in xs:
    y = foo(x, lambda x: x, 1, 4.5, 8, 10)
    ys.append(y)

plt.plot(xs, ys)
plt.savefig("f_only.png")

