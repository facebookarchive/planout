/*  Most of these functions are from the wonderful Underscore package http://underscorejs.org/  
    This file exists so that the planoutjs library doesn't depend on a few unneeded third party dependencies
    so that consumers of the library don't have to include dependencies such as underscore. As well, this helps reduce
    the file size of the resulting library.
*/


var deepCopy = function (obj) {
  var newObj = obj;
  if (obj && typeof obj === 'object') {
      newObj = Object.prototype.toString.call(obj) === "[object Array]" ? [] : {};
      for (var i in obj) {
          newObj[i] = deepCopy(obj[i]);
      }
  }
  return newObj;
}

var isObject = function(obj) {
  var type = typeof obj;
  return type === 'function' || type === 'object' && !!obj;
};

var isArray = function(object) {
  if (Array.isArray) {
    return Array.isArray(object);
  } else {
    return Object.prototype.toString.call( planout_code ) === '[object Array]';
  }
};

var isFunction = function(obj) {
  return typeof obj == 'function' || false;
};

//extend helpers

var keys = function(obj) {
  if (!isObject(obj)) return [];
  if (Object.keys) return Object.keys(obj);
  var keys = [];
  for (var key in obj) if (has(obj, key)) keys.push(key);

  if (hasEnumBug) collectNonEnumProps(obj, keys);

  return keys;
};

var allKeys = function(obj) {
  if (!isObject(obj)) return [];
  var keys = [];
  for (var key in obj) keys.push(key);

  if (hasEnumBug) collectNonEnumProps(obj, keys);

  return keys;
};

var extendHolder = function(keysFunc, undefinedOnly) {
  return function(obj) {
    var length = arguments.length;
    if (length < 2 || obj == null) return obj;
    for (var index = 1; index < length; index++) {
      var source = arguments[index],
          keys = keysFunc(source),
          l = keys.length;
      for (var i = 0; i < l; i++) {
        var key = keys[i];
        if (!undefinedOnly || obj[key] === void 0) obj[key] = source[key];
      }
    }
    return obj;
  };
};

//extend functionality from underscore
var extend = extendHolder(allKeys);
var extendOwn = extendHolder(keys);


/* underscore helpers */
var identity = function(value) {
  return value;
};

var isMatch = function(object, attrs) {
  var keys = keys(attrs), length = keys.length;
  if (object == null) return !length;
  var obj = Object(object);
  for (var i = 0; i < length; i++) {
    var key = keys[i];
    if (attrs[key] !== obj[key] || !(key in obj)) return false;
  }
  return true;
};

var matcher = function(attrs) {
  attrs = extendOwn({}, attrs);
  return function(obj) {
    return isMatch(obj, attrs);
  };
};

var cb = function(value, context, argCount) {
  if (value == null) return identity;
  if (isFunction(value)) return optimizeCb(value, context, argCount);
  if (isObject(value)) return matcher(value);
  return property(value);
};

var optimizeCb = function(func, context, argCount) {
  if (context === void 0) return func;
  switch (argCount == null ? 3 : argCount) {
    case 1: return function(value) {
      return func.call(context, value);
    };
    case 2: return function(value, other) {
      return func.call(context, value, other);
    };
    case 3: return function(value, index, collection) {
      return func.call(context, value, index, collection);
    };
    case 4: return function(accumulator, value, index, collection) {
      return func.call(context, accumulator, value, index, collection);
    };
  }
  return function() {
    return func.apply(context, arguments);
  };
};

//from underscore
var forEach =  function(obj, iteratee, context) {
  iteratee = optimizeCb(iteratee, context);
  var i, length;
  if (isArrayLike(obj)) {
    for (i = 0, length = obj.length; i < length; i++) {
      iteratee(obj[i], i, obj);
    }
  } else {
    var keys = keys(obj);
    for (i = 0, length = keys.length; i < length; i++) {
      iteratee(obj[keys[i]], keys[i], obj);
    }
  }
  return obj;
};

//map functionality from underscore
var map = function(obj, iteratee, context) {
  iteratee = cb(iteratee, context);
  var keys = !isArrayLike(obj) && keys(obj),
      length = (keys || obj).length,
      results = Array(length);
  for (var index = 0; index < length; index++) {
    var currentKey = keys ? keys[index] : index;
    results[index] = iteratee(obj[currentKey], currentKey, obj);
  }
  return results;
};

//reduce functionality from underscore
var reduce = function(obj, iteratee, memo, context) {
  iteratee = optimizeCb(iteratee, context, 4);
  var keys = !isArrayLike(obj) && keys(obj),
  length = (keys || obj).length,
  index = 0;
 
  if (arguments.length < 3) {
    memo = obj[keys ? keys[index] : index];
    index += 1;
  }
  for (; index >= 0 && index < length; index ++) {
    var currentKey = keys ? keys[index] : index;
    memo = iteratee(memo, obj[currentKey], currentKey, obj);
  }
  return memo;
};

//clone functionality from underscore
var shallowCopy = function(obj) {
  if (!isObject(obj)) return obj;
  return isArray(obj) ? obj.slice() : extend({}, obj);
};

/* helper functions from underscore */
var property = function(key) {
  return function(obj) {
    return obj == null ? void 0 : obj[key];
  };
};

var MAX_ARRAY_INDEX = Math.pow(2, 53) - 1;
var getLength = property('length');
var isArrayLike = function(collection) {
  var length = getLength(collection);
  return typeof length == 'number' && length >= 0 && length <= MAX_ARRAY_INDEX;
};

var has = function(obj, key) {
  return obj != null && Object.prototype.hasOwnProperty.call(obj, key);
};

/* All these are helper functions to deal with older versions of IE  :(*/
var hasEnumBug = !{toString: null}.propertyIsEnumerable('toString');
var nonEnumerableProps = ['valueOf', 'isPrototypeOf', 'toString',
                    'propertyIsEnumerable', 'hasOwnProperty', 'toLocaleString'];

function collectNonEnumProps(obj, keys) {
  var nonEnumIdx = nonEnumerableProps.length;
  var constructor = obj.constructor;
  var proto = (isFunction(constructor) && constructor.prototype) || Object.Prototype;

  var prop = 'constructor';
  if (has(obj, prop) && !contains(keys, prop)) keys.push(prop);

  while (nonEnumIdx--) {
    prop = nonEnumerableProps[nonEnumIdx];
    if (prop in obj && obj[prop] !== proto[prop] && !contains(keys, prop)) {
      keys.push(prop);
    }
  }
}
var contains = function(obj, item, fromIndex, guard) {
  if (!isArrayLike(obj)) obj = values(obj);
  if (typeof fromIndex != 'number' || guard) fromIndex = 0;
  return obj.indexOf(item) >= 0;
};

var vals = function(obj) {
  var keys = _.keys(obj);
  var length = keys.length;
  var values = Array(length);
  for (var i = 0; i < length; i++) {
    values[i] = obj[keys[i]];
  }
  return values;
};

export default { deepCopy, map, reduce, forEach, shallowCopy, extend, isObject, isArray }
