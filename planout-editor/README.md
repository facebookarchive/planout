## PlanOut Editor

The PlanOut editor lets you interactively edit and test PlanOut code.  It's built on Flux and React.

## Running

The PlanOut editor executes PlanOut scripts and tests by sending data to a
Python-based kernel which responds to AJAX requests. To start the kernel,
run the following from your command line:

`python planout-editor-kernel.py`

Then, navigate to:

[http://localhost:5000/](http://localhost:5000/).


Note that the kernel requires that you have Flask and PlanOut already installed.
If you don't have either package, you can install them via
[pip](http://pip.readthedocs.org/en/latest/installing.html) by typing
`pip install Flask` and `pip install planout`.


## Hacking the Editor
If you want to make changes or contribute to the PlanOut editor, you must first
have [npm](https://www.npmjs.org/) installed on your computer.

You can then install all the package dependencies by going to the root directory
and entering in the following into the command line.

`npm install`

If you don't already have watchify installed, you may have to type `npm install watchify` before entering `npm install`.

Then, to build the project, run this command:

`npm start`

This will perform an initial build and start a watcher process that will
continuously update the main application file, `bundle.js`, with any changes you make.  This way, you can test your changes to the editor by simply saving your code and hitting refresh in your Web browser.

This watcher is
based on [Browserify](http://browserify.org/) and
[Watchify](https://github.com/substack/watchify), and it transforms
React's JSX syntax into standard JavaScript with
[Reactify](https://github.com/andreypopp/reactify).
