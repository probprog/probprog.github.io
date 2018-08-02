---
title: Anglican Home Page
layout: default
---

## Anglican - A Probabilistic Programming System


[Anglican](https://bitbucket.org/probprog/anglican) is a probabilistic
programming language integrated with [Clojure](http://clojure.org/) and
[ClojureScript](http://clojurescript.org/).

While Anglican incorporates a sophisticated theoretical background that you are
invited to explore, its value proposition is to allow intuitive modeling in a
stochastic environment. It is not an academic exercise, but a practical everyday
machine learning tool that makes probabilistic reasoning effective for you.

Do you interact with users or remote systems? Then you often make the
unfortunate experience that they act unpredictably. Mathematically speaking you
observe undeterministic or stochastic behaviour. Anglican allows you to express
random variables capturing all this stochasticity for you and helps you to learn
from data to execute informed decisions in your Clojure programs. 

### Contact

[Join us on slack](https://clojurians.slack.com/messages/anglican/) if you have
any questions or suggestions. We are happy to learn about your experience!

## Getting started

Add the following dependency to your project (e.g. with
[Leiningen](https://leiningen.org/)):

[![Clojars Project](https://img.shields.io/clojars/v/anglican.svg)](https://clojars.org/anglican)

You can also clone the [examples
repository](https://bitbucket.org/probprog/anglican-examples/) and run `lein
gorilla` to get a quick setup.

A typical hello world example in statistics is a [coin flip
model](https://en.wikipedia.org/wiki/Coin_flipping). Our coin has two sides,
head and tail. Intuitively given a set of observed values of a coin you would
now like to know how fair it is. Mathematically speaking we want to know the
probability of head turning up. Let's encode a model for this:

~~~clojure
(ns anglican.coin-flips
  (:use [anglican core emit runtime]))
  

(defquery coin-model [coin-series]
  (let [prob (sample (beta 1 1))] ;; 1. prior
    (loop [[f & r] coin-series]
      (when f
        (observe (flip prob) f) ;; 2. incorporate data
        (recur r)))
    prob))
~~~

Anglican provides us primitives to build a model for our coin. If you are
familiar with Clojure, you will spot them: `defquery`, `sample` and `observe`.
`defquery` just sets up the scope of our model and allows us to give it the name
`coin-model` and define an input slot for our data as `coin-series`. In 1. we
define our prior belief without seeing any data. Let's just pick the [beta
distribution](https://en.wikipedia.org/wiki/Beta_distribution), because it
defines a probability between 0 and 1 and we assume that the coin is rather
fair. You can incorporate any other prior belief by tweaking the two parameters
of the Beta distribution though. 

~~~clojure
(sample* (beta 1 1)) ;; => 0.7185479773538508
~~~
(Note: `sample*` has to be used if you run it outside a query.)

In our model we then `sample` this value in the query and will plug it into the
`flip` distribution to `observe` each data point in 2.. If we have no data then
the loop will not run and we will get just our prior belief samples. This is not
really that helpful though. Anglican does its magic when you start to provide
observed values from the coin. For this we use `doquery`.


~~~clojure
(->> (doquery :smc coin-model [[true]] :number-of-particles 10000)
   (take 10)
   (map :result))

;; => (0.98529804829141 0.5948306954057996 0.5948306954057996 0.3579256597687244 0.9818148690925241 0.9818148690925241 0.4539746712124162 0.8944478678159888 0.8944478678159888 0.3433014675748332)
~~~

(Note: `doquery` receives a few arguments for the Sequential Monte Carlo method.
You can [look up each of those for inference](./inference/). An attribute of the
method is that you might get the same value multiple times in a statistically
consistent manner.)

You might know from real-life or a statistics course that having very few
examples, only one here, will not allow you to infer the probability of head.
Anglican provides you a so called posterior distribution after seeing the
values. As you can see our distribution is already considerably tilted towards 1.

Let's assume we observe 8 times heads:

~~~clojure
(->> (doquery :smc coin-model [[true true true true true true true true]] :number-of-particles 10000)
   (take 10)
   (map :result))
   
;; => (0.9068541546104443 0.9068541546104443 0.9664328786599636 0.9664328786599636 0.9664328786599636 0.9664328786599636 0.9664328786599636 0.9664328786599636 0.9664328786599636 0.9664328786599636)
~~~

Our posterior distribution confirms our intuition that this coin is very
unlikely, but still incorporates some uncertainty about the actual flipping
probability. We can be pretty sure that somebody is trying to cheat with this
coin here... Congratulations! You have just conducted your first
[Bayesian](https://en.wikipedia.org/wiki/Bayesian_probability) inference.
Bayesian inference allows you to both intuitively incorporate expert knowledge
in the prior to work in a small data regime, while correcting wrong prior
beliefs with more data.

What happens if you pick a different prior, e.g. tweaking the `beta` parameters
to 10 and 10? Try to use a larger data set. Do you see that the effect of the
prior belief vanishes?

## Theory

{% include youtubePlayer.html id="6Lqt07enBGs" %}


Anglican and Clojure share a common syntax, and can be invoked from
each other. This allows Anglican programs to make use of a rich
set of libraries written in both Clojure and Java.  Conversely
Anglican allows intuitive and compact specification of models
for which inference may be performed as part of a larger Clojure
project.

### Language

Anglican provides a language to abstract the statistical inference from the
Clojure runtime. If you are just interested in using Anglican, you can read the
details of it [in the language section](./language/) and ignore
the details about inference. You might have to try to different inference
methods depending on the nature of your model, but you do not need to learn any
of the statistics involved.

### Inference

The underlying inference methods are document [in the inference
section](./inference/). If you have a statistics background or are interested to
learn more about the mechanics behind Anglican's language primitives you are
invited to study the details. If you have any particular questions feel free to
join our slack channel.


### Background

The theoretical background is documented in peer-reviewed, state-of-the-art
[academic literature](./literature/).

## Contributors

Core contributors, in order of joining:

- [Frank Wood](http://www.robots.ox.ac.uk/~fwood/) – original prototype, smc and particle gibbs
- [Jan Willem van de Meent](http://www.robots.ox.ac.uk/~jwvdm/) – first release, inference methods
- [David Tolpin](http://offtopia.net/) – second release, CPS transformation, inference methods

as well as many others, in alphabetical order:

- [Tuan Anh Le](http://www.tuananhle.co.uk/)
- [Brooks Paige](http://www.robots.ox.ac.uk/~brooks/)
- [Yura Perov](http://www.yuraperov.com/)
- [Tom Rainforth](http://www.robots.ox.ac.uk/~twgr/)
- [Hongseok Yang](http://www.cs.ox.ac.uk/people/hongseok.yang/Public/Home.html)

## Funding

This work is supported under DARPA PPAML through the U.S. AFRL
under Cooperative Agreement number FA8750-14-2-0004. The U.S.
Government is authorized to reproduce and distribute reprints
for Governmental purposes notwithstanding any copyright notation
heron. The views and conclusions contained herein are those of
the authors and should be not interpreted as necessarily
representing the official policies or endorsements, either
expressed or implied, of DARPA, the U.S. Air Force Research
Laboratory or the U.S. Government.
