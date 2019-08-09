---
title: Mathematics Behind Loan Repayment
author: Taran Lynn
---

Textbooks often discuss the formula for the amount owed using compound interest,
$P \left(1 + \frac{r}{n}\right)^{nt}$.
This is usually done to showoff continuous compound interest, where $n$ goes to
infinity, and demonstrate a potential use of Euler's number in the resulting
equation $Pe^t$.
However, in all practicality this isn't useful for finances.
This is because when considering finances one would like to include payments in
their calculations.
I have yet to see a textbook that covers how a payment plan affects the formula.
As such I will discuss the math behind it in this post.

First let's describe what each variable represents.
$P$ is the principal, $r$ is interest rate, $n$ is the number of times the
interest is compounded per year, and $t$ is the number of years the debt is left
unpaid.
Now consider what happens if one pays an amount $p$ every time the interest is
compounded, and assume it's paid after compounding is taken into account.
To see what happens we'll let $D_k$ be the debt owed on the $k$th compounding
period.
To make the formulas more manageable we'll also define $a \equiv \left(1 -
\frac{r}{n}\right)$.
From this we can derive the formula
$$
\begin{align*}
D_0 &= P\\
D_{k+1} &= aD_k - p
\end{align*}
$$
Doing some series gymnastics we get
$$D_k = a^k P - p \sum_{i = 0}^{k - 1} a^i$$
Using the exponential series this simplifies to
$$D_k = a^k P - p \frac{1 - a^k}{1 - a}$$

When graphed this curve will look like the following, assuming minimum payments
are being made (i.e. the amount that needs to be paid so as not to go further
into debt).

![A downward curve representing time vs amount owed.](/images/2019-08-08-1.svg)

This is much different from the big, scary exponential curve we see with the
equation that does not take payments into account.
It's interesting to note the slope of the graph.
As time goes on the slope becomes more negative, which indicates that the debt
is being payed off faster.
This makes sense, as not as much is compounded on each cycle, and thus the
payments have more of an impact.

While knowing how debt changes over time is all well in good, a more pressing
question for most people is "how long will it take to pay off my debt?"
If we substitute 0 for $D_k$, $nt$ (the number of compound cycles in $t$ years)
for $k$, and solve for $t$, then we can get the approximate number of years it
will take to pay off the debt.
The resulting formula is
$$t = -\frac{\log_a \left( (1 - a) \frac{P}{p} + 1 \right)}{n}$$
That formula is not intuitive to look at, so let's plot a graph.

![Exponential decay in time to payoff versus amount paid per cycle.](/images/2019-08-08-2.svg)

This graph demonstrates why the advise to "pay a little bit more than the
minimum" is well deserved.
We can see that as we approach the minimum payment the time to payoff the debt
approaches infinity, that is to say it will never be paid off.
However, just a tiny increase in payment dramatically shortens the time it takes
to payoff the debt.
On the other hand, paying larger and larger sums beyond that gives diminishing
returns.
As a general rule of thumb, we would ideally pay twice the minimum payment.
Finally, if it wasn't obvious, paying off the debt faster saves one more money
(the total amount paid by the time all debt is cleared is $ntp$).

## The More Complex Case

I'll briefly discuss a more complex payment plan.
Consider what well happen if the payment period and compounding period are not
the same, such as when one pays every month on a loan that is compounded daily.
For this case we need to introduce a new variable $m$, which is how many times a
year payment is made.
This results in the original equations becoming
$$
\begin{align*}
D_0 &= P\\
D_{k+1} &= a^{n/m} D_k - p
\end{align*}
$$
I'll spare you the messy details, but the final resulting equations are
$$
\begin{align*}
D_k &= a^k P - p \frac{1 - a^k}{1 - a^{n/m}}\\
t &= -\frac{\log_a \left( (1 - a^{n/m}) \frac{P}{p} + 1 \right)}{n}
\end{align*}
$$
This results in much the same behavior as for the simple case.

## Personal Plug: My Open Source Program

Using these formulas I've created an open source program to help manage and
analyze debt.
It's called debtTools and is available on
[GitHub](https://github.com/lambda-11235/debtTools).
The repo also contains a paper with the mathematical derivations for the above
formulas.
