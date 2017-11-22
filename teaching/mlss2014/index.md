---
title: A Path to Learning Probabilistic Programming
layout: default
---

# Learning Probabilistic Programming

For the broadest possible perspective on probabilistic programming see [probabilistic-programming.org](http://probabilistic-programming.org/wiki/Home), a site that tracks the latest developments in probabilistic programming and maintains links to many probabilistic programming languages and systems as well as links to related literature.

A nice, short academic article on probabilistic programming is [The principles and practice of probabilistic programming](http://dl.acm.org/citation.cfm?id=2429117).

## Exercises 

These materials are designed to teach the characteristics of higher order Turing-complete probabilistic programming systems in general.  The materials, though, are directly source compatible with the [Anglican](../) probabilistic programming language.  Anglican [language documentation](../../language/), [installation instructions](../../download/),
and [examples](../../examples/) are available.  You may find the helper shell scripts [compute_counts.sh](./scripts/compute_counts.sh) and [compute_moments.sh](./scripts/compute_moments.sh) useful.

 - [Automatic Bayesian Inference via Probabilistic Programming](beta_binomial/)
 - [Things Higher Order Probabilistic Programming Systems Can Do That Others Can't](arithmetic_expression/)
 - [How Probabilistic Programming Works; The Actual Randomness Sampled When Exploring Traces](poisson_generative_procedure/)
 - [Why Developing Models Is Easy In Probabilistic Programming Languages But Eagerness Sometimes Hurts](bayesian_matrix_factorization/)
 - [A Natural Connection To Bayesian Nonparametrics](py_mem/)

These tutorial materials are straightforwardly syntactically compatible with 
the [Venture](http://probcomp.csail.mit.edu/venture/)
probabilistic programming system.  People learning probabilistic programming
will do well by themselves if they try solving these problems in Venture as well.  
Venture highlights a different, language-within-a-language (Python) interaction model, stressing interactivity and programmable inference.  

Another great resource is [Forest](http://forestdb.org/), a repository for generative 
models.  This site contains many fascinating examples of the expressivity of higher order Turing-complete probabilistic programming systems.  It also allows visitors to actually run said generative models in written in the [Church](http://arxiv.org/pdf/1206.3255.pdf) language in [Webchurch](https://probmods.org/play-space.html).  Note that the [Church wiki](http://projects.csail.mit.edu/church/wiki/Church) has a great deal of excellent and insightful material as well.

## Reporting Anglican bugs

There is a public [issue tracker](https://bitbucket.org/fwood/anglican/issues) to which bug reports can be posted.


## Developing probabilistic programming languages

The development of Turing-complete probabilistic programming languages remains a highly
specialized discipline.  Existing implementations include

- [Anglican](https://bitbucket.org/fwood/anglican)
- [jsChurch](https://github.com/stuhlmueller/jschurch)
- [Venture](https://github.com/mit-probabilistic-computing-project/Venturecxx)

though two of these repositories are currently remain private.

Arguably the best papers for learning how to develop probabilistic programming systems include

{% bibliography --file developing-prob-prog-languages.bib %}
