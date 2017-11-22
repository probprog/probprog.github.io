---
title: Anglican Home Page
layout: default
---

## Introduction

[Anglican](https://bitbucket.org/probprog/anglican) is an open
source, compiled probabilistic programming language
integrated with [Clojure](http://clojure.org/), a general
purpose functional programming language that just-in-time compiles 
to the [Java Virtual Machine
(JVM)](https://en.wikipedia.org/wiki/Java_virtual_machine).

To get started right away, follow the [installation and getting started guide](https://bitbucket.org/probprog/ppaml-summer-school-2016/raw/master/docs/getting-started-guide.pdf).

Anglican and Clojure share a common syntax, and can be invoked from
each other. This allows Anglican programs to make use of a rich
set of libraries written in both Clojure and Java.  Conversely
Anglican allows intuitive and compact specification of models
for which inference may be performed as part of a larger Clojure
project.

In Anglican, distributions are first class and user-definable.  Matrix 
primitives and multidimensional distributions are natively supported. 
A novel query syntax is introduced that combines ideas from both 
[Church](https://probmods.org/play-space.html) and 
[Venture](http://probcomp.csail.mit.edu/venture/) in a way that allows 
composition of models and inference at query boundaries.  Stateful random
procedures are user-definable too.

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

## License

Anglican is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

You should receive a copy of the [GNU General Public
License](gpl-3.0.txt) along with Anglican.  If not, see
[http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).

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
