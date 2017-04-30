const Helper = require('../common/Helper');
const DB = require('../common/DB');
const Researcher = require('../model').Researcher;
const rule = require('./rule');
const ResearcherCopy = DB.createModelCopy('Researcher');
const stats = require('./stat');

function* clean() {
	let journalMap = require('../resource/journals_abbr.json');
	let conferMap = require('../resource/conference_abbr.json');
	let wordsMap = require('../resource/IEEE_words_abbr.json');

	let pool = {};

	function c(profiles) {
		for (let i in profiles) {
			for (let j in profiles[i].pubs) {
				let venue = profiles[i].pubs[j].venue;
				if (venue && venue !== '' && venue !== 'undefined') {
					venue = venue.trim();
					let origin = venue;
					if (journalMap[venue]) venue = journalMap[venue];
					if (conferMap[venue]) venue = conferMap[venue];
					venue = venue
						.replace(/\b\w*(\d+)?[-‐–—]\w*\d+\b|\b\w+\d+\b|e?\d+(th|st|rd|nd)?|S?\(.+\)|\[.+\]|\.{2,}|\b[IVX]+\b|[,.]+|\s+&\s+|\b(and|the|of|in|or|for|at|on)\b/ig, '')
						// .replace(/\..+/ig,'')
						.replace(/[-‐–—(;/)'’:]+/g, ' ')
						.replace(/\b(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|June?|July?|Aug(ust)?|Sept(ember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\b/ig,'')
						.replace(/\s+/g, ' ')
						.trim();
					// venue = venue.split(' ').map(word => wordsMap[word] ? wordsMap[word] : word).join(' ');
					// venue.split(' ').forEach((word)=>{
					// 	Helper.fuzzyCompare()
					// })
					profiles[i].pubs[j].venue = venue;
				}
				else profiles[i].pubs[j].venue = ''
			}
		}
		return profiles;
	}
	for(let i = 0;i<52;i++){
		let profiles = yield Researcher.find().skip(i*500).limit(500);
		profiles = c(profiles);
		yield ResearcherCopy.collection.insert(profiles);
		console.log(`finish the ${i+1} round, ${profiles.length} have been inserted.`)
	}
	// console.log(profiles);
	// profiles = yield Researcher.find().skip(1).limit(1);
	// console.log(profiles);
	DB.connection.close();
	// printInfos(profiles, type = 'sent', limit = 100, inv = true, sort = true)
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
	clean: Helper.wrap(clean)
}