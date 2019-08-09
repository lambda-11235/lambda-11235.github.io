set terminal svg
set output "2019-08-08-2.svg"

set size ratio 1
set xlabel "Payment Made each Cycle" norotate
unset xtics
set ylabel "Time to Payoff" norotate
unset ytics

#
# Determine whether or not you want a key to be displayed.
#
#set key textcolor rgb "black"
#show key
unset key

set samples 100000

r = 0.05
n = 12
P = 100

a = 1 + r/n

f(x) = -log((1 - a)*P/x + 1)/(n*log(a))

plot [0:2] [-1:200]  f(x) lc rgb "#CC4444"

