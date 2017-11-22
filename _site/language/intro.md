The programming language of Anglican
is a subset of Clojure, extended with a few special forms
introducing randomness into programs. The forms are `sample`
for drawing a sample from distribution, `observe` for
conditioning the posterior distribution on a value, and
`predict`, for including a value into the output sample.
There are other special forms — `mem`, `store`, and `retrieve`
— which make writing probabilistic programs easier.


## Language

### Core syntax

The Anglican language is a subset of Clojure. Within `defquery`,
`let`, `if`, `cond`, `and`, `or`, `case`, `fn` forms are
supported. In `let` bindings and `fn` argument lists,
vector destructuring (but not hash map destructuring) is
supported. Compound literals for vectors, hash maps, and
sets are supported just like in Clojure.

### `recur`

Anglican is stackless, therefore `recur` is
unnecessary, no recursive call can lead to stack overflow;
Recursive calls to functions should be used instead. However,
`loop`/`recur` is provided for convenience as a way to express
loops. `recur` outside of `loop` will lead to unpredictable
behaviour and hard-to-catch errors.

### Core library

All of Clojure core library, except for higher-order functions
(functions that accept other functions as arguments) is
available in Anglican. In addition, the following higher-order
functions are available: `map`, `reduce`, `filter`, `some`,
`repeatedly`, `comp`, `partial`.

### Definitions outside of `defquery`

Data variables may be defined outside of `defquery` using
`def` and used inside `defquery`. Anglican functions outside
of `defquery` may be defined using `defm` (with the same syntax
as `defn`). Their bodies may use the same subset of Clojure
as `defquery`, as well as probabilistic and state access forms.
`defm`-defined functions can be called from Anglican without
restrictions.

Functions defined outside of `defquery` using `defn` may use the
full Clojure syntax but none of Anglican extensions, and must be
declared primitive using `with-primitive-procedures`:

    (with-primitive-procedures [name ...]
       body)

Where `name ...` is the  list of primitive procedures. The names
can be namespace-qualified, but will be seen unqualified in the
lexical scope of the form. For example,

    (with-primitive-procedures [clojure.string/capitalize]
       (defquery foo
          (predict :hello (capitalize "hello"))))

Will predict `:hello` as `Hello` (capitalized).

### Probabilistic forms

There are three probabilistic forms: `sample`, `observe`, and
`predict`.

* `(sample distribution)` returns a sample from
  `distribution`.
* `(observe distribution value)` conditions the posterior
  distribution  by observing `value` from  `distribution`.
* `(predict [label] value)` adds `value` as a prediction for
  `label`  to the sample. `label` is optional; if omitted, the
  symbolic form of the `value` argument is used.

### State access and modification

Functions can be memoized using `mem`, which accepts a function
object as its argument. If the argument is a named `fn` form,
self-recursive calls will call the memoized version of the
function. For example, every `predict` in the following code

    (defquery fact
        (let [fact (mem (fn fact [n]
                            (if (= n 1) 1
                                * n (fact (- n 1))))))]
          (predict (fact 1))
          (predict (fact 2))
          (predict (fact 3))
          (predict (fact 4))))

will call `fact` once per program invocation.

Values can be stored in the state using `store`, values stored
during the same run of the program can be retrieved using
`retrieve`. The syntax is

* `(store key ... value)` stores `value` at `key ...` in the state.
* `(retrieve key ...)` retrieves and returns the value stored at
  `key ...`. `key ...` can be a sequence of any length.

For example:

    (defquery customer
      (store :customer 4 :age 18)
      (predict :age (retrieve :customer 4 :age)))

will predict ':age' to be 18.

### Distributions

Distributions are defined in
[../src/anglican/runtime.clj](../src/anglican/runtime.clj) and
include `bernoulli`, `beta`, `binomial`, `discrete`,
`dirichlet`, `exponential`, `gamma`, `normal`, `poisson`,
`uniform-continuous`, `uniform-discrete`, `mvn`, `wishart`.
In addition, so-called random processes are provided by the
runtime, including CRP (Chinese Restaurant Process), DP
(Dirichlet Process), and GP (Gaussian Process). Random processes
implement the `random-process` protocol.

Other distributions and processes can be defined by the user.
The definition can be placed into Clojure modules containing
Anglican programs. The constructors of user-defined distributions
and processes must be declared primitive using
`with-primitive-procedures`.

## Inference Algorithms

Anglican provides a range of inference algorithms, and the list
is growing. The most up-to-date list of available algorithms
is in the [code map](codemap.md); algorithm options are keyword
arguments of their `infer` methods.

Below are some algorithms of general interest:

lmh
:   Lightweight Metropolis-Hastings. No options.

pgibbs
:   Particle Gibbs.
Options:

      * `:number-of-particles` (2 by default) — number of
	    particles per sweep.

pcascade
:   Particle Cascade. Options:

      * `:number-of-threads` (16 by default) — number of threads.
      * `:number-of-particles` (number-of-threads/2 by default)
	   — number of initial particles.

## Anglican in Gorilla REPL

Yet another way to run Anglican programs is [Gorilla
REPL](http://gorilla-repl.org). Anglican distribution contains
a wrapper for gorilla REPL, in `mrepl` directory of the
repository. Go `mrepl` and run `lein gorilla`.
Open the REPL URL in the browser, and either start a new
worksheet, or load a sample worksheet from `worksheets/`
subfolder. `worksheets/tworoads.clj` is provided as a starting
point.

A worksheet should start with a namespace declaration that
imports necessary and useful symbols into the worksheet's
namespace:

    (ns tworoads
      (:require [gorilla-plot.core :as plot])
        (:use [mrepl core]
                [anglican emit runtime]))

An Anglican program is defined in the usual way using `defquery`.
The inference is initiated by a call to `doquery` which accepts
the algorithm (for example, :lmh), the program name, and the
initial value (which will be `nil` for basic examples).
`doquery` returns a lazy sequence of samples.

    (def samples (doquery :lmh example nil))

Optionally, `doquery` accepts algorithm options as keyword
arguments, as well as the following additional options:

* `:warmup`, boolean and `true` by default. When `false`, the
program is not pre-evaluated. May be useful for tricks and
debugging. 
* `:debug`, boolean and `false` by default. When `true`, the
stack trace of exception thrown during inference is printed
on the standard output.

Take a look at
[worksheets/tworoads.clj](../../mrepl/worksheets/tworoads.clj),
as well as at [Gorilla REPL
documentation](http://gorilla-repl.org/start.html) to get
inspired.
---
title: Contribute to Anglican
layout: default
---
# Developer Guide

## Extending Anglican

* Using Anglican as a library: Anglican is on
  [clojars](https://clojars.org/anglican). If you want to use Anglican
  to develop your algorithms and applications, include [anglican
  "X.Y.Z"] (with a recent version instead of "X.Y.Z") into your project.

* Proposing patches:

    1. [Fork Anglican](https://bitbucket.org/probprog/anglican/fork).
    1. Make changes in the fork. The [code map](codemap.md)
       explains the source tree layout and module contents.
    1. Create a pull request.
    1. If the pull request resolves an issue, refer to the issue
       in the comment.

## Reporting bugs

* Use [issue tracker](https://bitbucket.org/probprog/anglican/issues) to
  report bugs and suggest features.

## Style guide

When suggesting fixes/changes/improvements, stick to the following
rules, or discuss before breaking them knowingly.

### General Formatting

* Keep the line width within the limit of 80 characters
  strictly, below 70 characters whenever possible.
* Use consistent indentation. Whatever your editor (Vim, Emacs, 
  LightTable) suggests is most probably good enough, but do
  not override the indentation manually on a case-by-case
  basis.
* In Lisp, a closing bracket or parenthesis does not
  traditionally start a line. Put closing brackets/parentheses
  at the end of expressions they close.

### Documenting the code

* Every namespace must have a documentation string describing
  the purpose and essential functionality of the namespace.
* Every function must have a documentation string explaining
  what the function does and returns.

### Comments

* Do not leave dead code (commented out code fragments) in the
  committed source code. Comments are for humans. Use timbre
  (https://github.com/ptaoussanis/timbre) if you need debugging
  printouts in the code.
* Comments that take up their own line (or start after an
  opening square bracket) should start with a
  double semicolon (three, four, five for headers).
* Inline comments should use a single semicolon.

### Unit testing

* Prepare enough tests to ensure that the code works correctly,
  and changes that break the code are immediately identified.
  Place unit tests for module anglican.foo into
  test/anglican/foo_test.clj (namespace anglican.foo-test).
* All tests much pass (lein test) before a change to the public
  repository.

## Implementation Guides

### Distributions and random processes

Two abstractions of random sources are used in Anglican, a
_distribution_ and a _random process_, the former corresponding
to 'elementary random procedure' (ERP), the latter 
related to 'exchangeable random procedure' (XRP).

Distributions and random processes are defined through
implementation of protocols `anglican.runtime/distribution` and
`anglican.runtime/random-process`. In addition, a multivariate
distribution may optionally implement protocol
`anglican.runtime/multivariate-distribution`. Several
distributions are defined in `anglican.runtime`, and other
distributions may be defined in terms of the 'basic'
distributions. 

For example, the Bernoulli distribution can be defined in terms
of uniform-continuous distribution:

	(defn bernoulli
	  "Bernoulli distribution"
	  [p]
	  (let [dist (uniform-continuous 0. 1.)]
		(reify
		  distribution
		  (sample [this] (if (< (sample dist) p) 1 0))
		  (observe [this value]
				   (Math/log (case value
							   1 p
							   0 (- 1. p)
							   0.))))))

where `sample` and `observe` are two methods of the
`distribution` protocol that must be provided.

A better and easier way to implement a distribution is macro
`defdist`.  In addition to defining the distribution function,
`defdist` assigns each distribution a record type, as well
as arranges for pretty-printing of the distribution instances.
The above declaration using `defdist` is:

	(defdist bernoulli
	  "Bernoulli distribution"
	  [p] [dist (uniform-continuous 0. 1.)]
	  (sample [this] (if (< (sample dist) p) 1 0))
	  (observe [this value]
			   (Math/log (case value
						   1 p
						   0 (- 1. p)
						   0.))))))

The first square brackets define the parameter list of the
function that creates the distribution instance. The second square
brackets define additional bindings (which may depend on the
parameters) used by the methods. Behind the scenes, `defdist`
does more than the `reify`-based definition above: it also 
defines a record type `bernoulli-distribution`, and instantiates
`print-method` for the type so that the distribution instance is
printed nicely. Consult the source code in
[`src/anglican/runtime.clj`](../src/anglican/runtime.clj) for the 
implementation of `defdist`.

Likewise, `defproc` is the macro for implementing random
processes. The two methods that must be implemented are
`produce` and `absorb`. `produce` returns a distribution
corresponding to the current state of the process instance.
`absorb` receives a sample and returns a new process instance
updated with the sample. For example, the Chinese Restaurant
process can be defined in the following way:

	(defproc CRP
	  "Chinese Restaurant process"
	  [alpha] [counts []]
	  (produce [this] 
		(let [dist (discrete (conj counts alpha))]
		  (reify 
			distribution
			(sample [this] (sample dist))
			(observe [this value]
			  (observe dist (min (count counts) value))))))
	  (absorb [this sample] 
		(CRP alpha
			 (-> counts
				 ;; Fill the counts with alpha (corresponding to
				 ;; the zero count) until the new sample.
				 (into (repeat (+ (- sample (count counts)) 1) alpha))
				 (update-in [sample] inc)))))

Of course, instead of reifying the distribution inside the
`produce` method, one can define a new distribution using
`defdist` (as in the implementation of CRP in
[src/anglican/runtime.clj]('../src/anglican/runtime.clj')).

### Inference algorithms

An inference algorithm must implement the
`anglican.inference/infer` multimethod. The method dispatches
on a keyword. If the algorithm is defined in a namespace
`anglican.foo`, and the keyword is `:foo`, the algorithm's
namespace will be loaded automatically by either
`anglican.core/m!` or `mrepl.core/doquery`.  However, an algorithm
may be implemented in any namespace and loaded explicitly before
infer is called.

The simplest algorithm to implement is importance sampling:

	(ns anglican.importance
	  (:refer-clojure :exclude [rand rand-int rand-nth])
	  (:use [anglican state inference]))

	(derive ::algorithm :anglican.inference/algorithm)

	(defmethod infer :importance [_ prog value & {}]
	  (letfn [(sample-seq []
				(lazy-seq
				  (cons (:state (exec ::algorithm
				                      prog value initial-state))
						(sample-seq))))]
				(sample-seq)))

For more examples, look at implementations of SMC, Particle
Gibbs, Lightweight Metropolis-Hastings. The [code
map](codemap.md) points at the Clojure modules containing
the implementations.

Although not required, a convenient function for implementing
an inference algorithm is `anglican.inference/exec`. This function
runs the probabilistic program until a so-called checkpoint,
a point in execution that requires intervention of the inference
algorithm. There are three types of checkpoints:

    anglican.trap.sample
	anglican.trap.observe
	anglican.trap.result

corresponding to `sample` and `observe` probabilistic forms, as
well as to returning the final result of a program execution,
which encapsulates, among other things, the list of predicts
and the log weight of the sample. The multimethod
`anglican.inference/checkpoint` should be used together with
`exec`. Default implementations of the multimethod for each type
of checkpoint are provided by the `anglican.inference` namespace,
and correspond to actions performed during importance sampling.

## First program

### Writing a program

Anglican programs reside in Clojure source code modules,
and are defined by the `defquery` macro. In order to
enable the Anglican language in a namespace, namespaces
`anglican.runtime` and `anglican.emit` must be used. A simple way to
do this is to write

    (ns example
      (:use [anglican emit runtime]))

in the beginning of a Clojure source file. The rest of the module
may contain one or more Anglican programs, or _queries_ (as well as
other Clojure code).  Queries are defined using the 
 keyword `defquery`, followed by the query name
and Anglican program text. If there is only one program in a
namespace, it customarily bears the same name as the namespace:

    (defquery example
      (let [bet (sample (beta 5 3))]
        (observe (flip bet) true)
        (predict (> bet 0.7))))

This together with the namespace above, placed in a file
 `example.clj` constitutes a first Anglican program.
