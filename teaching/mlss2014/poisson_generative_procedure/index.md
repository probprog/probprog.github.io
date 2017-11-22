---
title: How Probabilistic Programming Works
layout: default
---

# The Actual Randomness Sampled when Exploring Traces

<!--Inference in general-purpose probabilistic programs differs fundamentally from inference performed on models specified declaratively.
Rather than attempt to perform inference on the model directly, instead inference is performed over *execution traces* of the probabilistic program.

An execution trace in Anglican consists of the sequence of memory states encountered by the interpreter over the course of running the program code;
the generated samples are actually posterior samples of execution traces.
The functionals of the posterior distribution specified in `predict` statements can be computed from the memory states of the sampled execution traces.-->

In this exercise we write a conceptually non-trivial rejection procedure that when applied generates samples that follow a Poisson distribution.  The point of the exercise is insubstantially about writing the code (the code is reasonably easy to write) but instead is to get you to think very carefully about how random DB and PMCMC inference over the space of program execution traces works in this case.

 - [Exercise](questions.pdf)
