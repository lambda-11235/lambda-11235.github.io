set terminal svg
set output "2019-08-08-1.svg"

set size ratio 1
set xlabel "Time" norotate
unset xtics
set ylabel "Debt" norotate
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
p = 0.5

a = 1 + r/n

f(x) = a**x*P - p*(1 - a**x)/(1 - a)

plot [0:500] [0:100] f(x) > 0 ? f(x) : 0 lc rgb "#CC4444"
