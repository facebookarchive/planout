/* These functions are all from the wonderful Underscore package http://underscorejs.org/  */

var deepCopy = function (obj) {
  return JSON.parse(JSON.stringify(obj));
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

var extendHelper = function(obj) {
  if (!isObject(obj)) return [];
  var keys = [];
  for (var key in obj) keys.push(key);

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

var extend = extendHolder(extendHelper);

var shallowCopy = function(obj) {
  if (!isObject(obj)) return obj;
  return isArray(obj) ? obj.slice() : extend({}, obj);
};

export default { deepCopy, shallowCopy, extend, isObject, isArray }
