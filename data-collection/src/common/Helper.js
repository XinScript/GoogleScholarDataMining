const co = require('co');
const logger = require('winston');
// const csv = require('csv');
const fs = require('fs');

function wrap(fn) {
	return function(...args) {
		co(fn.apply(null, args)).catch((err) => {
			logger.error(err);
		})
	}
}

// function readCSV(pathName) {
// 	return new Promise((resolve) => {
// 		let map = {};
// 		let fd = fs.createReadStream(__dirname + '/' + pathName, {
// 				flags: 'r',
// 				encoding: 'utf8',
// 				autoClose: true
// 			})
// 			.on('end', () => {
// 				resolve(map);
// 			})
// 			.pipe(csv.parse()).pipe(csv.transform((record) => {
// 				map[record[2].trim()] = record[1].trim();
// 			}));
// 	});
// }

function isUupperCase(str){
	return str === str.toUupperCase();
}

function printInfos(profiles, type = 'word', limit = 10, inv = false, sort = false) {
	const wordObj = {};
	const sentObj = {};
	const wordArr = [];
	const sentArr = [];
	for (let i in profiles) {
		for (let j in profiles[i].pubs) {
			let venue = profiles[i].pubs[j].venue;
			if (venue && venue !== '' && venue !== 'undefined') {
				venue = venue.toLowerCase();
				if (sentObj[venue]) sentObj[venue]++;
				else sentObj[venue] = 1;
				let words = venue.split(' ');
				for (let k in words) {
					if (wordObj[words[k]]) wordObj[words[k]]++;
					else wordObj[words[k]] = 1;
				}
			}
		}
	}
	for (let key in wordObj) {
		wordArr.push([key, wordObj[key]]);
	}
	for (let key in sentObj) {
		sentArr.push([key, sentObj[key]]);
	}
	if (sort) {
		wordArr.sort((a, b) => b[1] - a[1]);
		sentArr.sort((a, b) => b[1] - a[1]);
	}
	if (type === 'word') {
		console.log('words count:' + wordArr.length);
		for (num = i = inv ? wordArr.length - limit : 0; i < num + limit; i++) {
			// if (wordsArr[1] === 1)
			console.log(wordArr[i]);
		}
	}
	if (type === 'sent') {
		console.log('sentences count:' + sentArr.length);
		for (num = i = inv ? sentArr.length - limit : 0; i < num + limit; i++) {
			// if (sentArr[1] === 1)
			console.log(sentArr[i]);
		}
	}
}


module.exports = {
	wrap,
	readCSV,
	isUupperCase,
	fuzzyCompare,
	printInfos,
}