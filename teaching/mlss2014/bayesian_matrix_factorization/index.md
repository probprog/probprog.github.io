---
title: Why Developing Models Is Easy In Probabilistic Programming Systems
layout: default
---

Probabilistic programming systems abstract model specification from inference.  Inference, in general, is provided automatically.  Initial development of models is generally easy.
Subsequent modifications to the same are extremely straightforward.  

Coding probabilistic matrix factorization illustrates this:

 - [Exercise](questions.pdf)
 
 A slightly larger data set consists of  10 movies and 20 users.  The movie ids are 

  1. Toy Story (1995)
  2. Twelve Monkeys (1995)
  3. Seven (Se7en) (1995)
  4. From Dusk Till Dawn (1996)
  5. Four Weddings and a Funeral (1994)
  6. Mask, The (1994)
  7. Jurassic Park (1993)
  8. Snow White and the Seven Dwarfs (1937)
  9. Independence Day (ID4) (1996)
  10. Pretty Woman (1990)
 
The dataset is [movies-10.csv](movies-10.csv).  There are two explicitly held out datapoints [holdout.csv](holdout.csv) against which predictive comparisons can be made.
 
Thanks to [Ziyu Wang](http://www.cs.ubc.ca/~ziyuw/) for helping to put together this exercise.
