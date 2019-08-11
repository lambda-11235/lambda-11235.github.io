---
title: Setting Pacing Rate of Packets
author: Taran Lynn
---

Here's a question that can be more complicated than it appears, "How does one
pace the delivery of packets so that data is sent at a specific rate?"
I'm approaching this question from a networking perspective, as some newer TCP
congestion control protocols, like BBR, rely on packet pacing rather than
traditional window based control.
Hopefully some fields outside of computer science will also find the insights
here to be useful.
First let's define some notation.
$x_n$ is the amount of data (or something else for other fields) delivered at
time step $t_n$, and $\overline{r}(m, n)$ is the average rate of delivery during
the time range $[m,n)$. $\overline{r}$ may be defined mathematically as

$$
\overline{r}(m, n) = \frac{\sum_{i = m}^{n - 1} d_i}{t_n - t_m}
$$
Where our ideal case is that for a chosen constant $R$, $\overline{r}(m, n) = R$
for all $m$ and $n$.

Now let's consider the simple, but naive, solution.
We can deliver packets at time such that such that
$t_n = t_{n-1} + \frac{d_{n-1}}{R}$.
Plugging this into the formula for the average delivery rate we get

$$\begin{align*}
\overline{r}(m, n) &= \frac{\sum_{i = m}^{n - 1} d_i}{t_n - t_m}\\
&= \frac{\sum_{i = m}^{n - 1} d_i}{\frac{d_{n - 1}}{R} + t_{n - 1} - t_m}\\
&\vdots\\
&= \frac{\sum_{i = m}^{n - 1} d_i}{\frac{\sum_{i = m}^{n - 1} d_{n - 1}}{R} + t_m - t_m}\\
&= \frac{\sum_{i = m}^{n - 1} d_i}{\frac{\sum_{i = m}^{n - 1} d_{n - 1}}{R}}\\
&= R
\end{align*}$$

This gives the ideal operation, but it has one flaw that makes it unusable in
practice.
The flaw is that if we can't accurately deliver all packets at the exact time we
need to, then the rate that we send at can very substantially from $R$.
This inaccuracy can be caused by delays in the processing of packet delivery.
To see this we look specifically at the second expansion

$$
\overline{r}(m, n) = \frac{\sum_{i = m}^{n - 1} d_i}{t_{n - 1} + \frac{d_{n-1}}{R} - t_m}
$$

The problem here is that if $t_{n-1} \neq t_{n-2} + d_{n-2}/R$, then the average
rate will never become $R$.
To get around this we can compute the time to send the packet as not just a
function of the last packet, but all the packets before it.

$$\begin{align*}
\overline{r}(0, n) &= R\\
\frac{\sum_{i = 0}^{n - 1} d_i}{t_n - t_0} &= R\\
t_n &= t_0 + \frac{\sum_{i = 0}^{n - 1} d_i}{R}
\end{align*}$$

We can plug this into the average rate formula to confirm that it gives ideal
operation similar to the naive implementation.

$$\begin{align*}
\overline{r}(n - 1, n) &= \frac{d_{n-1}}{t_n - t_{n-1}}\\
&= \frac{d_{n-1}}{t_0 + \frac{\sum_{i = 0}^{n - 1} d_i}{R} - \left( t_0 -
\frac{\sum_{i = 0}^{n - 2}}{R} \right)}\\
&= \frac{d_{n-1}}{\frac{d_{n-1}}{R}}\\
&= R
\end{align*}$$

Notice that $\overline{r}(m, n)$ now does not depend on any intermediate time
values, only the starting time value $t_0$ and the amount of data sent
previously.
These values can be very accurately tracked and are not subject to the common
inaccuracies that affect sending time.
Thus, if one is not set correctly the average rate it will correct itself back
to $R$.
This ability to self correct the delivery rate helps to overcome issues with
the timing of deliveries.

<!--
## The Continuous Case

Note that the result is lot less interesting if one is controlling the rate of
a flow, for example in a chemical plant.
In this case we can directly set the instantanious rate $r(t)$ at time $t$.
Even though this flow may fluctuate, we may define the average rate between
times $t_1$ and $t_2$ as
$$
\overline{r}(t_1, t_2) = \frac{\int_{t_1}^{t_2} r(\tau) \text{d}\tau}{t_2 - t_1}
$$

If we solve for the $r(t)$ needed to make the average equal to $R$ like before,
then we get
$$\begin{align*}
\overline{r}(t_0, t) &= R\\
\frac{\int_{t_0}^{t} r(\tau) \text{d}\tau}{t - t_0} &= R\\
\int_{t_0}^{t} r(\tau) \text{d}\tau &= R (t - t_0)\\
\frac{}{\text{d}{t}} \int_{t_0}^{t} r(\tau) \text{d}\tau &= \frac{}{\text{d}{t}} R (t - t_0)\\
r(t) &= R
\end{align*}$$
so there isn't any special consequence of non-uniform flows (as far as I know,
chemical engineers correct me if I'm wrong).
-->
