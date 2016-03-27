---
title: Functions as Monads and Applicative Functors
author: Taran Lynn
---

<span style="color: red">
  This is not a tutorial, it is just some of my thoughts. I expect the reader to
  be familiar enough with monads to recognize if I've made a mistake. Please
  contact me if you see any errors in this post.
</span>

# Functions are Monads #

Functions are monads, which also implies that they are applicative
functors. This can lead to some interesting computational models. Functions
implement the Monad class as

``` haskell
instance Monad ((->) r) where
  return :: t -> (r -> t)
  return = const

  (>>=) :: (r -> t) -> (t -> (r -> s)) -> (r -> s)
  f >>= g = \r -> g (f r) r
```

Where `((->) r)` is similar in form to `Map a`. Both of these are defined to be
monadic over their second type argument. This means that `(r -> t)` is monadic
over `t`, meaning the types for `return` and bind (`(>>=)`) have to be `t -> (r
-> t)` and `(r -> t) -> (t -> (r -> s)) -> (r -> s)`, respectively. The first
signature is obviously the same as `const`, hence this is what `return` is
defined as. The operation of bind is, however, far more interesting. Consider

``` haskell
foo = do x <- id
         y <- sqrt
         return $ x + y
    = id >>= (\x -> sqrt >>= (\y -> x + y))
    = \r -> (\x -> (\r' -> (\y -> x + y) (sqrt r'))) (id r) r
    = \r -> (\x r' -> (\y -> x + y) (sqrt r'))) (id r) r
    = \r -> ((\y -> (id r) + y) (sqrt r))
    = \r -> (id r) + (sqrt r)
```

If we use this function we find that `foo 4` is `6.0`, and `foo 9` is `12.0`. On
closer inspection it appears that `foo` is a function that passes its argument
to `id` and `sqrt` and adds the two results. Or, in code

``` haskell
foo r = (id r) + (sqrt r)
```

To find out why this is lets do some transformation on `foo`.

``` haskell
foo = do x <- id
         y <- sqrt
         return $ x + y
    = id >>= (\x -> sqrt >>= (\y -> x + y))
    = \r -> (\x -> (\r' -> (\y -> x + y) (sqrt r'))) (id r) r
    = \r -> (\x r' -> (\y -> x + y) (sqrt r'))) (id r) r
    = \r -> ((\y -> (id r) + y) (sqrt r))
    = \r -> (id r) + (sqrt r)
```

In general, we find that if we replace `id` and `sqrt` with any functions `f`
and `g`, then

``` haskell
do x <- f
   y <- g
   return $ h x y
= \r -> h (f r) (h r)
```

Something even more interesting happens when we look at `sqrt >>= (+)`. This
function is exactly the same as `foo`. If we analyze it we see that it expands
to

``` haskell
do x <- sqrt
   y <- (+) x
   return y
```

Notice that `y` will expand to `(+) x r`, and `x` will expand `sqrt r`, which
when combined gives

``` haskell
(+) (sqrt r) r = (+) (sqrt r) (id r) = (sqrt r) + (id r)
```

## A Practical Example ##

One example of the usefulness of this is

``` haskell
data Customer = Customer { getName :: String
                         , getEmail :: EmailAddr
                         , getAccountNumber :: Integer }

custComp :: Customer -> a
custComp = do name <- getName
              email <- getEmail
              accNum <- getAccountNumber
              return $ someComputation name email accNum
```

Without using do notation, this would instead be

``` haskell
custComp :: Customer -> a
custComp cust = someComputation (getName cust) (getEmail cust) (getAccountNumber cust)
```

# Functions as Applicative Functors #

I find that using the fact that functions are applicative functors to also be
useful. First let us look at the trivial implementation of Functor for
functions.

``` haskell
instance Functor ((->) r) where
  fmap :: (a -> b) -> (r -> a) -> (r -> b)
  fmap = (.)
```

This isn't particularly interesting until we consider the applicative
implementation.

``` haskell
instance Applicative ((->) r) where
  pure = const
  f <*> g = \x -> (f x) (g x)
```

The function `foo` can now be written as `(+) <$> id <*> sqrt`. The practical
example can also be written as

``` haskell
custComp :: Customer -> a
custComp = someComputation <$> getName <*> getEmail <*> getAccountNumber
```

I personally find this preferable to the two other ways of writing `custComp`,
as it is both concise and informative.

# Why Does This Matter? #

Using functions in this way allows us to write algorithms that use the results
of applying the same argument to multiple functions in a clear, concise way.

<img src="/images/function_monad.svg" alt="Drawing" style="width: 400px;"/>

As shown by the above image, we can write algorithms that are only concerned
with the outputs of `f`, `g`, and `h`, but still produces a function from `x` to
some result.
