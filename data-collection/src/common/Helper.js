const co = require('co');
const logger = require('winston');
const csv = require('csv');
const fs = require('fs');
const wuzzy = require('wuzzy');

function wrap(fn) {
	return function(...args) {
		co(fn.apply(null, args)).catch((err) => {
			logger.error(err);
		})
	}
}

function readCSV(pathName) {
	return new Promise((resolve) => {
		let map = {};
		let fd = fs.createReadStream(__dirname + '/' + pathName, {
				flags: 'r',
				encoding: 'utf8',
				autoClose: true
			})
			.on('end', () => {
				resolve(map);
			})
			.pipe(csv.parse()).pipe(csv.transform((record) => {
				map[record[2].trim()] = record[1].trim();
			}));
	});
}

function isUupperCase(str){
	return str === str.toUupperCase();
}

function fuzzyCompare(a,b){
	return wuzzy.levenshtein(a,b);
}

module.exports = {
	wrap,
	readCSV,
	isUupperCase,
	fuzzyCompare
}