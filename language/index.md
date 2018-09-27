---
title: Anglican Language 
layout: default
---

# Language Syntax

The programming language of Anglican
is a subset of Clojure, extended with a few special forms that make it a
probabilistic programming language. These forms are `sample`
for drawing a samples from distributions and `observe` for
conditioning on data.
There are other special forms — `mem`, `store`, and `retrieve`
— which make writing probabilistic programs easier.

The following documentation is quite terse because 
Anglican is, to a large extent, intentionally syntactially indistiguishable from Clojure.  
Clojure reference
materials, obtainable from the web via standard search procedures,
are as essential to programming in Anglican as is this Anglican
language documentation.  The key to Anglican knowing
 Clojure _and_ understanding `defquery`, the interface between
 Clojure and Anglican.
 
 This interface is meant to be as transparent as possible and for
 as much Clojure functionality to work inside `defquery` as possible.

In general the documentation that follows indicates functionality _relative to Clojure_.
For instance, the absence of an explicit statement of existence means 
that the Clojure language feature probably isn't supported in Anglican.  

## A First Example Program

Anglican programs reside in Clojure source code modules,
and are delimited by `defquery` (a macro). In order to
enable the Anglican language in a Clojure module, at the minimum namespaces
`anglican.runtime` and `anglican.emit` must be used. A simple way to
do this is to write

~~~clojure
(ns example
  (:use [anglican emit runtime]))
~~~

in the beginning of a Clojure module, for example 'example.clj'. Clojure
namespacing is notably complex; arguably the best strategy for writing
a namespace that includes Anglican functionality is to copy namespace 
declarations from the provided [examples](../examples/index.html).

The rest of the module
may contain one or more Anglican programs, aka _queries_.   Queries
are delimited by the keyword `defquery`, followed by the query name
and the program text. If there is only one program in a
namespace, it customarily bears the same name as the namespace:

~~~clojure
(defquery example
  (let [bet (sample (beta 5 3))]
    (observe (flip bet) true)
    (> bet 0.7)))
~~~

`defquery` assigns a value to `example` that allows it to be passed
as the argument to a `doquery`.  `doquery` uses inference algorithms to
produce lazy sequence of weighted samples that characterize the
conditional distribution of the value of the expression in the tail position of 
the defquery, here `(> bet 0.7)`.  

Syntactically `defquery` denotes a joint distribution, `observe`'s denote
which random variables' values are known, and the value of the last, "return" 
expression, is the variable whose conditional distribution is of interest.

<!-- Note that queries are composable and inference is customizable
at the level of a query. -->

What follows is a description of what program text can go inside `defquery`, i.e. a 
description of the Anglican language.  Note that while the source code inside `defquery`
intentionally bears a great deal of resemblance to Clojure, it is not Clojure code, 
it is Anglican code.

## Core Anglican syntax

The Anglican language is a subset of Clojure. Within `defquery`,
`let`, `if`, `when`, `cond`, `case`, `and`, `or`, `fn` forms are
supported (others may be in the future but are not now). 
In `let` bindings and `fn` argument lists,
vector destructuring (but not hash map destructuring) is
supported. Compound literals for vectors, hash maps, and
sets are supported just like in Clojure.

## `recur`

Anglican is stackless, therefore `recur` is
unnecessary, no recursive call can lead to stack overflow;
Recursive calls to functions should be used instead. However,
`loop`/`recur` is provided for convenience as a way to express
loops. `recur` outside of `loop` will lead to unpredictable
behaviour and hard-to-catch errors.

## Core library

All of Clojure's [core library](http://clojure.github.io/clojure/clojure.core-api.html), 
except for higher-order functions
(functions that accept other functions as arguments) is
available in Anglican. In addition, the following higher-order
functions are implemented: `map`, `reduce`, `filter`, `some`,
`repeatedly`, `comp`, `partial`.

## Definitions outside of `defquery`

The border between Clojure and Anglican is subtle and usually will
pose no problem to most programmers, however, some confusion can arise 
from the fact that Anglican programs are macro compiled into CPS-style
Clojure functions.  This means that some wrapping of "native" Clojure functions
needs to happen in order to use them in Anglican.  Errors 
arising due to misunderstanding this boundary crop up in the form of 
"wrong number of argument" exceptions.  Carefully following the guidance in 
this section will resolve most if not all such difficulties. 

Data variables may be defined outside of `defquery` using `def`
and used inside `defquery`. Anglican functions outside of
`defquery` may be defined using `defm` (with the same syntax as
`defn`, albeit with a single arity only). Their bodies may use
the same subset of Clojure as `defquery`, as well as
probabilistic and state access forms.  `defm`-defined functions
can be called from Anglican without restrictions.

Functions defined outside of `defquery` using `defn` may use the
full Clojure syntax but no Anglican extensions, and must be
declared primitive using `with-primitive-procedures`:

~~~clojure
(with-primitive-procedures [name ...]
   body)
~~~

Where `name ...` is the  list of primitive procedures. The names
can be namespace-qualified, but will be seen unqualified in the
lexical scope of the form. For example,

~~~clojure
(with-primitive-procedures [clojure.string/capitalize]
   (defquery foo
      (capitalize "hello")))
~~~

Denotes the dirac distribution over `Hello` (capitalized).

## Probabilistic forms

In Anglican there are two probabilistic forms: `sample` and `observe`.

* `(sample distribution)` returns a sample from a
  `distribution`.  
* `(observe distribution value)` returns value; *critical* produces
  conditioning side-effect.   It does this by adding
  the value of `(observe* distribution value)` (see below)
  to the log probability of the trace.  
  
## State access and modification

Functions can be memoized using `mem`, which accepts a function
object as its argument. If the argument is a named `fn` form,
self-recursive calls will call the memoized version of the
function. For example, every `fact` call in the following code

~~~clojure
(defquery fact
    (let [fact (mem (fn fact [n]
                        (if (= n 1) 1
                            * n (fact (- n 1)))))]
      [(fact 1) (fact 2) (fact 3) (fact 4)]))
~~~

will reuse previous computation.

Values can be stored in the state using `store`, values stored
during the same run of the program can be retrieved using
`retrieve`. The syntax is

* `(store key ... value)` stores `value` at `key ...` in the state.
* `(retrieve key ...)` retrieves and returns the value stored at
  `key ...`. `key ...` can be a sequence of any length.

For example:

~~~clojure
(defquery customer
  (store :customer 4 :age 18)
  (retrieve :customer 4 :age))
~~~

will return be 18 in :result.

## Distributions

Distributions are *Clojure* implementations of a `distribution` protocol, consisting
of two methods:

**(sample* distribution)** accepts a distribution instance and returns a sample from the distribution.  The *Anglican* `sample` uses this method to generate random variable values.

**(observe* distribution value)** accepts a distribution and a value and returns log probability of the value given the distribution.  *Anglican* inference backends stop at `observe` statements and often use the return value from calling `observe*` with the same original arguments as the `observe` call to effect conditioning.  

The core runtime library provides the following distribution constructors which can be used either in Clojure or Anglican, remembering the difference between `sample` and `sample*`, and, `observe` and `observe*`:

**(bernoulli p)** constructs a single binomial trial. Calling `sample` on the returned distribution instance generates 1 with probability `p` and 0 with probability `1-p`.

**(beta a b)** constructs a Beta distribution with pseudocounts `a` and `b`. Calling `sample` on the returned distribution instance generates a `double` on interval `[0,1)`. 

**(binomial n p)** constructs a Binomial distribution with success probability `p` and number of trials `n`. Calling `sample` on the returned distribution instance generates a `long` on the interval `[0 ... n]`.

**(categorical pairs)** constructs a categorical distribution parameterized by a list of pairs `(val p)`. Calling `sample` on the returned distribution instance generates `val-k` with probability `p-k`.

**(dirichlet [alpha-1 ... alpha-K])** constructs a Dirichlet distribution parameterized by a vector of pseudocounts `alpha`. Calling `sample` on the returned distribution instance generates a vector of probabilities `prob` such that `(sum prob) = 1.0` and `(count prob) = (count alpha)`. 

**(discrete p)** constructs a discrete distribution parameterized by a list probabilities `p`. Calling `sample` on the returned distribution instance generates a `long` in the range `[0 ... K-1]`, with `K = (count p)`. The result `k` is returned with probability `(nth p k)`. 

**(exponential l)** constructs an exponential distribution with with rate parameter `l`. Calling `sample` on the returned distribution instance generates a double in the domain `[0, Inf)`.

**(flip p)** constructs a single binomial trial. Calling `sample` on the returned distribution instance generates `true` with probability `p` and `false` with probability `1-p`.

**(gamma a b)** constructs a Gamma distribution with shape `a` and rate `b`. Calling `sample` on the returned distribution instance generates a `double` on the domain `(0, Inf)`.

**(mvn mean cov)** constructs a Multivariate normal distribution with mean
`mean` and covariance matrix `cov`. Calling `sample` on the returned distribution instance generates a `double` vector of the
same size as `mean`.

**(normal mean std)** constructs a normal distribution with mean
`mean` and standard deviation `std`. 

**(poisson l)** constructs a Poisson distribution with rate `l`. Calling `sample` on the returned distribution instance generates a non-negative `long`.

**(uniform-continuous min max)** constructs a uniform continuous distribution. Calling `sample` on the returned distribution instance generates a `double` in the domain `[min, max]`.

**(uniform-discrete min max)** constructs a uniform discrete distribution. Calling `sample` on the returned distribution instance generates a `long` from the range `[min ... max-1]`.

**(wishart n V)** constructs a Wishart distribution with `n` degrees of
freedom and scale matrix `V`. Calling `sample` on the returned distribution instance generates a matrix of `double` of the
same size as `V`.

In addition, so-called random processes are provided by the
runtime, including CRP (Chinese Restaurant Process), DP
(Dirichlet Process), and GP (Gaussian Process). Random processes
implement the `random-process` protocol, consisting of two
methods:

**(produce process)** accepts a process instance and returns a
distribution object (which can be passed as a parameter to
`observe` and `sample`) corresponding to the current state of
the process.

**(absorb process value)** updates the process by incorporating
a value sampled or observed from the distribution produced by
the processes.

The following random process constructors are included into the
core runtime library:

**(CRP alpha)** is a Chinese restaurant process with concentration
`alpha`.

**(DP alpha H)** is a Dirichlet process with concentration `alpha`
over base distribution `H`.

**(GP m k)** is a Gaussian process with mean function `m` and
covariance function `k`.

Other distributions and processes can be defined by the user.
The definition can be placed into Clojure modules containing
Anglican programs. A user-defined distribution is specified
using `defdist`:

~~~clojure
(defdist dirac
  "Dirac distribution"
  [x]  ; distribution parameters
  []   ; auxiliary bindings
     (sample* [this] x)
     (observe* [this value] (if (= x value) 0.0 (- (/ 1.0 0.0)))))
~~~

Similarly, a user-defined random process is specified using
`defproc`:

~~~clojure
(defproc DSD
  "discrete-symmetric-dirichlet process"
  [alpha N]                                ; process parameters
  [counts (vec (repeat N (double alpha)))] ; auxiliary bindings
  (produce [this] (discrete counts))
  (absorb [this sample]
	(DSD alpha N (update-in counts [sample] + 1.))))
~~~
	  
Constructors of user-defined distributions and processes must be
declared primitive using `with-primitive-procedures`.

<!-- ## Inference Algorithms

Anglican provides a range of inference algorithms, and the list
is growing. Algorithm options are keyword
arguments of their `infer` methods.

Below are some algorithms of general interest:

lmh
:   Lightweight Metropolis-Hastings. No options.

almh
:   Adaptive Lightweight Metropolis-Hastings. No options.

pgibbs
:   Particle Gibbs.
Options:

      * `:number-of-particles` (2 by default) — number of
	    particles per sweep.

pgas
:   Particle Gibbs with ancestor sampling.
Options:
    
     * `:number-of-particles` (2 by default) - number of particles per sweep.

pimh
:   Particle Independent Metropolis-Hastings.
Options:

     * `:number-of-particles` (2 by default) - number of particles per sweep.

pcascade
:   Particle Cascade. Options:

      * `:number-of-threads` (16 by default) — number of threads.
      * `:number-of-particles` (number-of-threads/2 by default)
	   — number of initial particles.
 -->
