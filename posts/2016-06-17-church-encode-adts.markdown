---
title: Church Encoding Haskell ADTs
author: Taran Lynn
---

**Note: The church encoded type aliases require Rank2Types or RankNTypes.**

Church encoding is a technique whereby data structures are represented by
functions.  To this end it can be shown that any Haskell ADT can be represented
by a function.  I will be ignoring GADTs, and focus only on product and sum
types.

To start, lets look at how product types can be encoded as a function. I will
use a triple, or 3-element tuple, as my example. First we can see the normal ADT
definition.

``` haskell
data Triple a b c = Triple a b c
```

One possible way to encode this as a function is as a function that takes
another function as an argument and passes its stored values to that
function. To see how this works, we can look at the type alias and constructor
for the church encoded version.

``` haskell
type Triple a b c = forall r. (a -> b -> c -> r) -> r

triple :: a -> b -> c -> Triple a b c
triple x y z f = f x y z
```

To create a triple we simply need to pass the data we want to store into this
function, such as `x = triple 1 2 3`. We can now access the stored values by
passing another function into our triple. For example, if we want to turn the
church triple into an ADT triple we could write `x (\a b c -> (a, b, c))` (or
more concisely `x (,,)`), which would return `(1, 2, 3)`.

It's also interesting to see how church encoding relates to pattern
matching. For example, the following
``` haskell
foo :: Triple a b c -> ...
foo trpl = trpl (\x y z -> ...)
```
can be directly translated to the ADT version as
``` haskell
foo :: Triple a b c -> ...
foo trpl@(Triple x y z) = ...
```

This relation to pattern matching is more interesting for types that are both
sum and product types, but first lets discuss pure sum types. The simplest
example is a boolean value `data Bool = False | True`. This can be encoded as a
function that takes multiple argument and chooses between them.

``` haskell
type Bool = forall r. r -> r -> r

false :: Bool
false x y = x

true :: Bool
true x y = y
```

We can now see that we can choose different values based on whether we have a
true or false value. To see why this important let's look at another pattern
matching example.  The ADT version
``` haskell
foo :: Bool -> ...
foo False = bar
foo True = baz
```
can be translated to the function encoded version as
``` haskell
foo :: Bool -> ...
foo b = b bar baz
```

This shows that the choice encoded into the function representation is directly
related to the choice made in pattern matching.

A more interesting case is when we have a type of sums of product. The typical
example would be the Either type. These cases can be encoded as a function that
takes multiple functions as arguments, and selectively applies it contained
values to these functions.  The encoding of Either is thus

``` haskell
type Either a b = forall r. (a -> r) -> (b -> r) -> r

left :: a -> Either a b
left x f g = f x

right :: b -> Either a b
right y f g = g y
```

Like the other encodings, this one also has a relation to pattern matching. The
following
``` haskell
foo :: Either a b -> ...
foo e = e (\x -> ...) (\y -> ...)
```
can be directly translated to a pattern match as
``` haskell
foo :: Either a b -> ...
foo e@(Left x) = ...
foo e@(Right y) = ...
```

These methods can be used to encode most ADTs, with one exception that I'll get
to. First, I'd like to demonstrate the power of these techniques with a more complicated example.
The following
``` haskell
data Foo a b c = Foo a b c
               | Bar a b
               | Baz a

sum :: Num a => Foo a a a -> a
sum (Foo x y z) = x + y + z
sum (Bar x y) = x + y
sum (Baz x) = x
```
can be translated to
``` haskell
type Foo a b c = forall r. (a -> b -> c -> r) -> (a -> b -> r) -> (a -> r) -> r

foo :: a -> b -> c -> Foo a b c
foo x y z f g h = f x y z

bar :: a -> b -> Foo a b c
bar x y f g h = g x y

baz :: a -> Foo a b c
baz x f g h = h x

sum :: Num a => Foo a a a -> a
sum f = f (\x y z -> x + y + z) (+) id
```

The area where church encoding ADTs becomes problematic is when encoding recursively defined
ADTs. The typical example of this is the List type, where `data List a = Cons a (List a) | Nil`.
The naive way to encode this would be as
``` haskell
type List a = forall b. (a -> List a -> b) -> b -> b

cons :: a -> List a -> List a
cons x xs f y = f x xs

nil :: List a
nil f y = y
```

However, recursive type aliases are not allowed in Haskell. One way to overcome
this issue by using a newtype declaration
``` haskell
newtype List a = List { runList :: forall r. (a -> List a -> r) -> r -> r }

cons :: a -> List a -> List a
cons x xs = List $ \f y -> f x xs

nil :: List a
nil = List $ \f y -> y
```

We can then apply these lists using the `runList` function. Here's an example
function
``` haskell
showList :: Show a => List a -> String
showList xs = runList xs (\y ys -> (show y) ++ " " ++ (showList ys)) ""
```
`showList (cons 1 (cons 2 (cons 3 nil)))` then produces the string `"1 2 3 "`.
