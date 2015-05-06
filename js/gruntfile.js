module.exports = function(grunt) {
	require('load-grunt-tasks')(grunt); 
	grunt.loadNpmTasks('grunt-contrib-jasmine');
	grunt.loadNpmTasks('grunt-browserify');
	grunt.loadNpmTasks('grunt-contrib-uglify');

	grunt.initConfig({
	  "babel": { //es6 -> es5
	  		dist: {
	  			files: {
	  				'es5jk/assignment.js' : 'es6/assignment.js',
	  				'es5jk/interpreter.js': 'es6/interpreter.js',
			  		'es5jk/experiment.js' : 'es6/experiment.js',
			  		'es5jk/ops/base.js'   : 'es6/ops/base.js',
			  		'es5jk/ops/utils.js'  : 'es6/ops/utils.js',
			  		'es5jk/ops/random.js' : 'es6/ops/random.js',
			  		'es5jk/ops/core.js'   : 'es6/ops/core.js',
	  			}
	  		}
	  },
	  "browserify": { //to actually deal with modules properly
	      dist: {
	        files: {
	        	'es5/assignment.js' : 'es5jk/assignment.js',
		        'es5/interpreter.js': 'es5jk/interpreter.js',
		  		'es5/experiment.js' : 'es5jk/experiment.js',
		  		'es5/ops/base.js'   : 'es5jk/ops/base.js',
		  		'es5/ops/utils.js'  : 'es5jk/ops/utils.js',
		  		'es5/ops/random.js' : 'es5jk/ops/random.js',
		  		'es5/ops/core.js'   : 'es5jk/ops/core.js',
	        }
	      }
	  },
	  "uglify": {
	  	dist: {
	  		files: {
	  			'planout.min.js' : ['es5/assignment.js', 'es5/interpreter.js', 'es5/experiment.js', 'es5/ops/random.js', 'es5/ops/core.js', 'es5/ops/base.js', 'es5/ops/utils.js']
	  		}
	  	}
	  }

	});
	 
	grunt.registerTask('default', ['babel', 'browserify', 'uglify' ]);
}