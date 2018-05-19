

// import


const spawn = require("child_process").spawn;
const fs = require("fs");

const yaml_js = require('yaml-js');

const translate = require(process.env.SPACE_SHIP_HOME + '/api/webserver/query_translators/main.js').translate;
const translate_post = require(process.env.SPACE_SHIP_HOME + '/api/webserver/query_translators/main.js').translate_post;


// set global variables


var LAST_RESPONSE_CHUNK_SIGN = '';

fs.readFile(process.env.SPACE_SHIP_HOME + '/api/webserver/config.yaml', 'utf8', function(err, contents) {
    var config = yaml_js.load(contents)

	LAST_RESPONSE_CHUNK_SIGN = config.last_response_chunk_sign;
});

function send_response(query, res){
	console.log(query)

	let python_process = spawn('python3', [process.env.SPACE_SHIP_HOME + "/api/background/main.py", query]);

	res.write('')

	python_process.stdout.on('data', function(data){
		if (data.indexOf(LAST_RESPONSE_CHUNK_SIGN) == -1){
			res.write(data.toString('utf8'));
		} else {
			res.end(data.toString('utf8').replace(LAST_RESPONSE_CHUNK_SIGN, '') + '');
		}
		console.log(data.toString('utf8'));
	});

	python_process.stderr.on('data', function(data){
		console.log(data.toString('utf8'));
	});
}


function handle_api_request(req, res){
	query = translate(req.originalUrl).replace(/%20/g, ' ');
	send_response(query, res);
}

function handle_api_post_request(req, res){
	query = translate_post(req.body);
	//console.log(query);
	send_response(query, res);
}

exports.handle_api_request = handle_api_request;
exports.handle_api_post_request = handle_api_post_request;