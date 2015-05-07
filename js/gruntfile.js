var webpack = require('webpack');

module.exports = function(grunt) {
	require('load-grunt-tasks')(grunt); 
	grunt.loadNpmTasks('grunt-contrib-jasmine');
	grunt.loadNpmTasks('grunt-contrib-uglify');
	grunt.loadNpmTasks('grunt-webpack');

	grunt.initConfig({
    'webpack': {
      build: {
        progress: true,
        output: {
          path: 'es6/',
          filename: 'planout.js'
        },
        module: {
          loaders: [{
            test: /\.js$/,
            exclude: /node_modules/,
            loader: 'babel-loader'
          }]
        },
        resolve: {
          extensions: ['', '.js']
        }
      }
    },
    uglify: {
      options: {
        sourceMap: true,
        sourceMapName: 'planout.map.js'
      },
      build: {
        files: {
          'planout.min.js': 'planout.js'
        }
      }
    }
   });
	 
	grunt.registerTask('default', ['webpack', 'uglify']);
}