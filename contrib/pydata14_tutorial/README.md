# PyData '14 PlanOut Tutorial
Welcome to the PyData '14 Silicon Valley PlanOut tutorial! You'll find a collection of IPython notebooks for Eytan Bakshy's tutorial on PlanOut.

If you want to follow along the live tutorial on your own computer (or are not at PyData!), you need to install some software and clone the PlanOut git repository.

## Requirements
### Software requirements
The tutorial requires IPython, Pandas, and PlanOut. The former two come with Anaconda. PlanOut has only been tested on Mac OS X and Linux.

 * IPython ([installation instructions](http://ipython.org/install.html). We recommend Anaconda.)
 * PlanOut v0.2 or greater (first timers `sudo easy_install planout`, older timers `sudo easy_install --upgrade planout`)
 * Node.js - optional (installation link on the [node.js homepage](http://nodejs.org))

Note that you may need to re-install the `planout` package if you installed PlanOut before installing IPython.

### Downloading the tutorial files
If you have git, you can checkout PlanOut by typing:

```
git clone https://github.com/facebook/planout.git
```

or you can [click here](https://github.com/facebook/planout/archive/master.zip) to download a zip archive.


## Loading up the tutorial notebooks
Navigate to your checked out version of PlanOut and type:

```
cd contrib/pydata14_tutorial/
ipython notebook --pylab inline
```

Tutorial files include:
 * `0-getting-started.ipynb`: This teaches you the basics of how to implement experiments in pure Python.
 * `1-logging.ipynb`: How data is logged in PlanOut and examples of how to analyze PlanOut log data with Pandas.
 * `2-interpreter.ipynb`: How to generate serialized experiment definitions using (1) the PlanOut domain-specific language (2) automatically, e.g., via configuration files or GUIs.
 * `3-namespaces.ipynb`: How to manage simultaneous and follow-on experiments.
