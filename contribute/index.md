---
title: Contribute to Anglican
layout: default
---
# Examples

We would love for you to share the models you develop using Anglican 
with the community.  To share an interesting model follow these steps.


1. git fork [Anglican Examples](https://bitbucket.org/probprog/anglican-examples).
2. Make a new worksheet containing your model in the fork. 
3. Create a pull request.
4. Explain your new model and what it teaches in the comment.


# Improvements to Anglican

Anglican is open source and we encourage community involvement of all
kinds.  

## Proposing patches:


1. git fork [Anglican](https://bitbucket.org/probprog/anglican/fork).
2. Make changes in the fork. The code map in the repository
   explains the source tree layout and module contents.
3. Create a pull request.
4. If the pull request resolves an issue, refer to the issue
   in the comment.


## Reporting bugs

* Use [issue tracker](https://bitbucket.org/probprog/anglican/issues) to
  report bugs and suggest features.

### Contributor Style guide

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
