const Helper = require('../common/Helper');
const DB = require('../common/DB');
const Researcher = require('../model').Researcher;
const ResearcherCopy = DB.createModelCopy('Researcher');
const logger = require('winston')

function* clean() {
	let journalMap = require('../resource/journals_abbr.json');
	let conferMap = require('../resource/conference_abbr.json');
	let wordsMap = require('../resource/IEEE_words_abbr.json');

	function handle(profiles) {
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
						.replace(/[-‐–—(;/)'’:]+/g, ' ')
						.replace(/\b(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|June?|July?|Aug(ust)?|Sept(ember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\b/ig,'')
						.replace(/\s+/g, ' ')
						.trim();
					venue = venue.split(' ').map(word => wordsMap[word] ? wordsMap[word] : word).join(' ');
					profiles[i].pubs[j].venue = venue;
				}
				else profiles[i].pubs[j].venue = ''
			}
		}
		return profiles;
	}
	for(let i = 0;i<52;i++){
		let profiles = yield Researcher.find().skip(i*500).limit(500);
		profiles = handle(profiles);
		yield ResearcherCopy.collection.insert(profiles);
		logger.log(`finish the ${i+1} round, ${profiles.length} have been inserted.`)
	}
	DB.connection.close();
}

module.exports = {
	clean: Helper.wrap(clean)
}