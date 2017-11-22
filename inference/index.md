---
title: Inference Methods
layout: default
---

# Inference Methods

From Clojure, the syntax for calling an inference algorithm on a query is `(doquery
:method foo args & method-opts)`. For example, we could run the `smc` algorithm with
`:number-of-particles` set to 100 on a program `foo` defined by `(defquery foo [x] ...)` as follows

~~~clojure
(doquery :smc
  foo [xval]
  :number-of-particles 100)
~~~


When a `query` object is passed to `doquery` or `conditional` the user has a choice of what kind of inference should be used to perform the characterization of the denoted conditional distribution.  In general we recommend `rmh` if all observes occur at the end of the program, `smc` with as many particles as can fit in memory if observes occur with the program, and `ipmcmc` for programs with internal observes that are too large for `smc` to solve well.

*CRITICAL*: the default arguments supplied for all inference methods are the _minimum_ required.  This design make interactive debugging easier but nearly absolutely ensures poor inference performance unless non-default parameter values are chosen.  For instance `smc` performance will only get better with more particles; ultimately how many particles to use should be chosen so as to maximize the joint criteria of how long you want to wait and how good you want your results to be.

Anglican provides 4 general categories of inference methods and several instances of each:

- Importance sampling (IS),
- Markov chain Monte Carlo (MCMC),
- Particle Markov chain Monte Carlo (PMCMC),
- Maximum a posteriori (MAP).

The current list of algorithms that are included with Anglican is

| Method       | Type  | Description                                                      |
|--------------|-------|------------------------------------------------------------------|
| `importance` | IS    | Importance sampling (likelihood weighting)                       |
| `smc`        | IS    | Sequential Monte Carlo                                           |
| `pcascade`   | IS    | Particle cascade (asynchronous sequential Monte Carlo)           |
| `pgibbs`     | PMCMC | Particle Gibbs (iterated conditional SMC)                        |
| `pimh`       | PMCMC | Particle independent Metropolis-Hastings                         |
| `pgas`       | PMCMC | Particle Gibbs with ancestor sampling                            |
| `ipmcmc`     | PMCMC | Interacting particle Markov chain Monte Carlo                    |
| `lmh`        | MCMC  | Lightweight Metropolis-Hastings                                  |
| `rmh`        | MCMC  | Random-walk Lightweight Metropolis-Hastings                      |
| `almh`       | MCMC  | Adaptive scheduling lightweight Metropolis-Hastings              |
| `palmh`      | MCMC  | Parallelised adaptive scheduling lightweight Metropolis-Hastings |
| `plmh`       | MCMC  | Parallelised lightweight Metropolis-Hastings                     |
| `bamc`       | MAP   | Bayesian Ascent Monte Carlo                                      |
| `siman`      | MAP   | MAP estimation via simulated annealing                           |

# Method-specific Options

Some algorithms have optional arguments, which can be specified with `(doquery :method prog args :option value)`. These are

| Method      | Keyword              | Default              | Description                                   |
|-------------|----------------------|----------------------|-----------------------------------------------|
| `smc`       | :number-of-particles | 1                    | Number of particles                           |
| `rmh`       | :alpha               | 0.5                  | Probability of using a local MCMC move        |
|             | :sigma               | 1                    | Spread of the local move                      |
| `ipmcmc`    | :number-of-particles | 2                    | Number of particles per sweep                          |
|             | :number-of-nodes     | 32                    | Number of nodes running SMC and CSMC          |
|             | :number-of-csmc-nodes| (/ :number-of-nodes 2) | Number of nodes CSMC          |
|             | :all-particles?      | true                 | Return all particles or just one per node        |
|             | :pool                | (+ (npus) 2)         | Number of threads to use |
| `pgibbs`    | :number-of-particles | 2                    |                                               |
| `pgas`      | :number-of-particles | 2                    |                                               |
| `pimh`      | :number-of-particles | 2                    |                                               |
| `plmh`      | :number-of-threads   | 2                    | Number of processor threads                   |
| `palmh`     | :number-of-threads   | 2                    |                                               |
| `pcascade`  | :number-of-threads   | 16                   |                                               |
|             | :number-of-particles | :number-of-threads/2 | Initial number of particles                   |
| `bamc`      | :predict-candidates  | false                | Output samples with non-increasing log-weight |
| `siman`     | :predict-candidates  | false                |                                               |
|             | :cooling-rate        | 0.99                 | Cooling rate (should be less than 1)          |
|             | :cooling-schedule    | :exponential         | Cooling schedule, :exponential or :lundy-mees |


<!-- `importance`
: (no options)

`lmh`
: (no options)

`almh`
: (no options)

`pgibbs`
:   Particle Gibbs.
Options:

      * `:number-of-particles` (2 by default) — number of
        particles per sweep.

`pgas`
:   Particle Gibbs with ancestor sampling.
Options:

     * `:number-of-particles` (2 by default) - number of particles per sweep.

`pimh`
:   Particle Independent Metropolis-Hastings.
Options:

     * `:number-of-particles` (2 by default) - number of particles per sweep.

`pcascade`
:   Particle Cascade. Options:

      * `:number-of-threads` (16 by default) — number of threads.
      * `:number-of-particles` (number-of-threads/2 by default)
       — number of initial particles.
 -->
<!-- ### Importance Sampling (`importance`)

|(no optional arguments)|

### Sequential Monte Carlo (`smc`)

| Keyword              | Default  | Description         |
|----------------------|----------|---------------------|
| :number-of-particles  | 1        | Number of particles |

### Particle cascade (`pcascade`)

| Keyword              | Default              | Description                          |
|----------------------|----------------------|--------------------------------------|
| :number-of-threads    | 16                   | Number of processor threads to use   |
| :number-of-particles  | :number-of-threads/2 | Number of initial particles          |

### Particle Gibbs (`pgibbs`)

| Keyword              | Default  | Description         |
|----------------------|----------|---------------------|
| :number-of-particles  | 1        | Number of particles |

### Particle independent Metropolis-Hastings (`pimh`)

| Keyword              | Default  | Description         |
|----------------------|----------|---------------------|
| :number-of-particles  | 1        | Number of particles |

### Particle Gibbs with Ancestor Sampling (`pgas`)

| Keyword              | Default  | Description         |
|----------------------|----------|---------------------|
| :number-of-particles  | 1        | Number of particles |




 -->
