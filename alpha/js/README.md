# PlanoutJS #
=============


This provides an implementation of PlanOut in ES6.

##Installation##
-----------
```
npm install planout
```

##Comparison with Python Implementation##
-----

The only two places where this implementation differs from the Python implementation is that it does not include an implementation of namespaces and setting experiment assignment parameters explicitly requires calling .set instead of the setter used in the Python implementation.

##Usage##
-----

If you are lucky enough to be writing in a codebase that is using ES6 here is how to use this library to define a sample experiment

```javascript
import PlanOut from ‘planout’

class MyExperiment extends PlanOut.Experiment {
	
	configure_logger() {
		return;
		//configure logger
	}

	log(event) {
		//log the event somewhere
	}

	previously_logged() {
		//check if we’ve already logged an event for this user
	}

	setup() {
		//set experiment name, etc.
	}
	
	assign(params, args) {
		params.set(‘foo’, new PlanOut.UniformChoice({‘choices’: [‘a’, ‘b’], ‘unit’: args.id});
		args.val++; //args is an arbitrary 
	}

}
```

Then, to use this experiment you would simply need to do 

```javascript
var exp = new MyExperiment({‘id’: user.id, ‘val’: 0});
console.log(“User has foo param set to “ + exp.get(‘foo’));
```

If you are using ES5, here is an example of how to use this library: 

```javascript
TODO
```




	