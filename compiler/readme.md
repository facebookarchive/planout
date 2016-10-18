# PlanOut Compiler

## Reference compiler - Javascript Classical CFG grammar

`planout.js` is a script that parses a PlanOut experiment and outputs a serialized experiment in JSON format.

## Using the Compiler
The script can be run from the command line via [node.js](http://nodejs.org/) as follows.
```
node planout.js ../demos/sample_scripts/exp1.planout
```

Alternatively, the script may be run from a web page.
```
<script src="planout.js"></script>
<script>
  var json = planout.parse(script);
</script>
```

Here is a [demo](http://facebook.github.io/planout/demo/planout-compiler.html).

## Alternate compiler - Python PEG grammar
The python grammar is implemented in two parts, an EBNF as planout.ebnf and a semantics.py which implements the AST transformation.

It is built using grako like so
```
pip install grako
grako planout.ebnf -o parser.py
python test.py <planout-script>
```

## Extending the PlanOut language
The PlanOut grammar is specified in `planout.jison`. If you wish to extend PlanOut to support custom operators, you can modify the grammar file and generate a new compiler script using [Jison](http://zaach.github.io/jison/) library.
