---
id: about-planout
title: About PlanOut
layout: docs
permalink: /docs/about-planout.html
prev: planout-language.html
next: how-planout-works.html
---

PlanOut was developed at Facebook as a language for describing complex
experimental designs for behavioral science experiments.
PlanOut is one of a few ways of setting up experiments at Facebook.
This open source release, in addition to being a complete implementation of
PlanOut, includes core aspects of the experimentation system we've developed
to make experiments easier to run, and prevent common pitfalls in deploying and
analyzing experiments.

### Why are you open sourcing PlanOut?
We wanted to share our experiences with running and analyzing
many large experiments at Facebook. This open source release accompanies a
research paper on running online experiments:
[Designing and Deploying Online Field Experiments](https://www.facebook.com/download/255785951270811/planout.pdf).

We hope that with this release, we will get others to get excited about running
experiments, and do so in an effective and sound fashion.  We are always learning
new things about what works and what doesn't, and hope that by engaging with the
community, we will all come to develop experimentation software whose use cases
extend beyond the initial release of the Python-based reference implementation.


### Who is PlanOut for?
We hope that the software is useful for researchers and businesses who
want to run experiments out of the box. We have also tried to build things in a
way that is easy to port to other platforms and environments.

### Can I contribute to PlanOut?
The main goal with this release is to provide an implementation of how we
run experiments at Facebook, and set developers and researchers along in this
direction. We intend on keeping PlanOut up to date, and hope that the
community can continue to develop it, either through contributing directly to
the original repository, or by forking it.

We also welcome bug fixes, ports to other platforms, extensions, and graphical
interfaces for constructing and analyzing experiments.

### Acknowledgements
PlanOut was originally developed by Eytan Bakshy, Dean Eckles, and Michael S.
Bernstein, and is written and maintained by Eytan Bakshy at Facebook.
Aspects of the logging and experimental management system were largely
inspired by QuickExperiment, a tool developed by Breno Roberto, Andy Pincombe, Wesley May.
Andy and Wes have been instrumental in reviewing and providing feedback on the
current implementation PlanOut at Facebook.
Many of the best practices for running experiments were developed through
collaboration with Daniel Ting and Wojeich Galuba on the Decision Tools team.
Sean Taylor helped with the design and packaging of the Python implementation
of PlanOut. "Ta" Virot Chiraphadhanakul developed the [PlanOut language to JSON
compiler](http://facebook.github.io/planout/demo/planout-compiler.html) for
JavaScript. We would also like to thank former collaborators that
played a role in the development of PlanOut, including John Fremlin.
In addition, we'd like to thank Cat Le for the dice design and easter egg concept.
 Finally, we would like to thank James Pearce for his help with setting up this site.
