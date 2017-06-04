---
title: Implementing a Dependently Typed Language
author: Taran Lynn
---

I've recently implemented a dependently typed language called
[TTyped](https://github.com/lambda-11235/ttyped). It took a little over a week
to complete. This project allowed me to learn how to implement a type checker,
as well as the difficulties of implementing a dependently typed language.

## Ramping Up

Before working on TTyped I wrote a series of projects that built up to it. I
first implemented the untyped [lambda
calculus](https://en.wikipedia.org/wiki/Lambda_calculus), then the [simply typed
lambda](https://en.wikipedia.org/wiki/Simply_typed_lambda_calculus) calculus,
and finally [System F](https://en.wikipedia.org/wiki/System_F). Implementing the
untyped lambda calculus was easy, even with lazy evaluation added on top of it.
When I started implementing the type checker for the simply typed lambda
calculus I quickly learned that my view of how a type checker worked was wrong.
Starting from C++ or Java one would think that a type checker simply determines
whether a value matches its given type. For example, in the declaration `String
s = "foo"` we simply have to determine that `"foo"` has type `String`. However,
before we can determine that `"foo"` is of type `String` we first have to
determine what type `"foo"` has.  This hints at the main task a type checker
has; to determine the types of terms and **optionally** determine whether they
match our expectations (or throw an error if they can't be typed). This
distinction becomes more apparent in a language like the simply typed lambda
calculus where we don't state the return types of functions. For example,
consider what the type of `(λx : a. x)` would be if `a` was some type. In the
body of the function we know that `x` is of type `a`, and since `x` is the
returned value the return type must also be `a`, thus the type of the whole
function is `a → a`. Now consider what the type of `(λx : a. (x x))` might be.
In the body of the function we know that `x : a`, and we also know only function
types can be applied, so when we see `(x x)` we look at the left side of the
application to see if it's a function type, which it isn't. The expression is
thus untypable, so we throw an error.

Next, I decided to tackle System F. Even with parametric polymorphism added in
the type checker wasn't that different from the one for simply typed lambda
calculus and was rather easy to implement. However, at this time I decided to
implement a reducer that reduced terms to their normal form, as compared to the
evaluator that I had been using that a simply lexical scoping scheme. I
immediatly ran into the problem of lambda capturing of variables. After much
heartache I decided to use [de Bruijn
indices](https://en.wikipedia.org/wiki/De_Bruijn_index), which vastly simplified
the problem of reduction.

## To Dependent Typing

The next step after System F is System Fω, but I decided to skip it and go to
full dependent types. The first version of TTyped was based on [intuitionistic
type theory](https://en.wikipedia.org/wiki/Intuitionistic_type_theory) trimmed
down to non-cumulative universes and functions. I later made the universes
cumulative and added finite (bottom, unit, boolean, etc.) types. However, a
couple of things left me unsatisfied. One problem was that I could not pass the
identity function to itself, since an identity funtion over the `n`th universe
belong to the universe `n + 1`. This also meant that I couldn't properly Church
encode data. To able to handle all the data types I wanted I would thus have to
add three built in inductive types, namely sigma, sum, and well-founded types. I
haven't yet implemented these.

Seeking a way around these limitations I turned to the [Calculus of
Constructions (CoC)](https://en.wikipedia.org/wiki/Calculus_of_constructions). I
forked the implementation out into a second branch and started implementing CoC
based off of Coquand and Huet's 1986 paper "The Calculus of Constructions". The
implementation was fairly straight forward, especially with Coquand's thourough
and detailed discriptions. In the CoC the type of types `*` does not have a type
and isn't allowed at the value level.  This removes the need for universes and
allowed me to pass the identity function to itself and to Church encode data.
Unfortunately this meant that Church encoded data either had to operate over
types or values, and couldn't operate over both.

## Conclusions

I think I prefer the CoC implementation of TTyped over the ITT version. It is
simpler and more flexible from a programming perspective, although from a logic
perspective I believe it would be harder to use. Overall, both were fairly easy
to implement and were fun to program in. For someone wishing to implement their
own dependently typed language I would suggest reading three papers.
"Constructive Mathematics and Computer Programming" be Martin Löf gives a short
description of ITT with cumulative universes. In "A Tutorial Implementation of a
Dependently Typed Lambda Calculus" by Andres Löh, Conor McBride, and Wouter
Swierstra lead the reader through implementing a dependently typed language
(called LambdaPi) in Haskell. Finally, Coquand's paper is a must read for
dependently type theory.
