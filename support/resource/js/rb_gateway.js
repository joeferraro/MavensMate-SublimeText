/* Git JS gateway */
/* Tim Harper (tim.harper at leadmediapartners.org) */
TM_BUNDLE_SUPPORT = ENV('TM_BUNDLE_SUPPORT')

function e_sh(str) { 
  return '"' + (str.toString().replace('"', '\\"').replace('\\$', '\\$')) + '"';
}

function exec(command, params) {
  params = params.map(function(a) { return e_sh(a) }).join(" ")
  return TextMate.system(command + " " + params, null)
}

function ENV(var_name) {
	return $.trim(TextMate.system("echo $" + var_name, null).outputString);
}

function gateway_command(command, params) {
  // var cmd = arguments.shift
  // var params = arguments
  try {
    command = "ruby " + e_sh(TM_BUNDLE_SUPPORT) + "/gateway/" + command
    return exec(command, params).outputString
  }
  catch(err) {
    return "ERROR!" + err;
  }
}

function dispatch(params) {
	console.log('dispatching')
	try {
		arr = new Array();
		$.each(params, function(key, value) { 
			val = (value == null || value == "") ? "" : value.toString()
			arr.push(key + '=' + val); 
		});
		console.log(arr)
		command = "ruby " + e_sh(TM_BUNDLE_SUPPORT) + "/dispatch.rb";
    return exec(command, arr).outputString
  }
  catch(err) {
    console.log(err);
		return "ERROR!" + err;
  }
}