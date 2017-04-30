const https = require('https');
const config = require('../config');
const iconv = require('iconv-lite');
const Stream = require('stream').Transform;

function fetchText(path, hostname) {
	const options = {
		hostname,
		port: 443,
		path,
		method: "GET",
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
				response.body = iconv.decode(Buffer.concat(buf), 'ISO-8859-1');
				resolve(response);
			});
		}).setTimeout(config.TIMEOUT, () => {
			reject(response);
		}).end();
	});
};

function fetchImg(path) {
	const options = {
		hostname: config.HOSTNAME,
		port: 443,
		path,
		method: 'GET'
	};

	const response = {};
	response.body = null;
	response.url = path;

	return new Promise((resolve, reject) => {
		const req = https.request(options, (res) => {
			const buf = new Stream();
			// const buf = []
			res.on('data', (d) => {
				buf.push(d)
			}).on('end', () => {
				response.body = buf;
				resolve(response);
			});
		}).setTimeout(config.TIMEOUT, () => {
			reject(response);
		}).end();
	});
}

module.exports = {
	fetchText,
	fetchImg
};