const https = require('https');
const config = require('../config');
const iconv = require('iconv-lite');

function fetch(path) {
	const options = {
		hostname: 'scholar.google.co.uk',
		port: 443,
		path,
		method: 'GET'
	};
	const response = {};
	response.body = '';
	response.url = path;
	return new Promise((resolve, reject) => {
		const req = https.request(options, (res) => {
			const buf = []
			res.on('data', (d) => {
				buf.push(d)
			}).on('end', () => {
				response.body = iconv.decode(Buffer.concat(buf),'ISO-8859-1');
				resolve(response);
			});
		}).setTimeout(config.TIMEOUT, () => {
			reject(response);
		}).end();
	});
};

module.exports = {
	fetch
};