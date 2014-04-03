---
id: about-planout
title: About PlanOut
layout: docs
permalink: /docs/about-planout.html
prev: planout-language.html
---

PlanOut was developed at Facebook as a language for describing complex
experimental designs for behavioral science experiments.
PlanOut is one of a few ways of setting up experiments at Facebook.
This open source release, in addition to being a complete implementation of
PlanOut, includes core aspects of the experimentation system we've developed
to make experiments easier to run, and prevent common pitfalls in deploying and
analyzing experiments.

### Why are you open sourcing PlanOut?
We wanted to share our knowledge and experiences with running and analyzing
many large experiments at Facebook. This open source release accompanies
[Designing and Deploying Online Field Experiments](https://www.facebook.com/download/255785951270811/planout.pdf) by Eytan Bakshy, Dean Eckles,
and Michael S. Bernstein.

While we often communicate our work through writing academic papers,
we felt that most users of experimentation platforms who have little
background in the design and analysis of experiments, would be better
reached through software and online documentation.


### Who is PlanOut for?
We hope that the software is useful for researchers and businesses who
want to run experiments out of the box. We have also tried to build things in a
way that is easy to port to other platforms and adapt to work with production
systems with additional performance and organizational requirements.

### Can I contribute to PlanOut?
The main goal with this release is to provide an implementation of how we
run experiments at Facebook, and set developers and researchers along in this
direction. We intend on lightly maintaining PlanOut, but hope that the
community can continue to develop it, either through contributing directly to
the original repository, or by forking it.

We welcome bug fixes, ports to other platforms, like Node.js and Rails,
and graphical interfaces for constructing serialized,
JSON-formatted experiment definitions.

### Acknowledgements
PlanOut was originally developed by Eytan Bakshy, Dean Eckles, and Michael S.
Bernstein. Aspects of the logging and experimental management system were largely
inspired by QuickExperiment, a tool developed by Breno Roberto and Wesley May.
Many of the best practices for running experiments were developed through
collaboration with Daniel Ting and Wojeich Galuba on the Decision Tools team.
Sean Taylor helped with the design and packaging of the Python implementation
of PlanOut. "Ta" Virot Chiraphadhanakul developed the [PlanOut language to JSON
compiler](http://facebook.github.io/planout/demo/planout-compiler.html) for
JavaScript. We would also like to thank former collaborators that
played a role in the development of PlanOut, including John Fremlin.
In addition, we'd like to thank Ben Congleton for his comments and
suggestions on this release, and dice concept and design by Cat Le.
 Finally, we would like to thank James Pearce for all his help with the site.
