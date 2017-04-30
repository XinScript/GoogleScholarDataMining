const Request = require('../service/Request');
const Helper = require('../common/Helper');
const cheerio = require('cheerio');
const fs = require('fs');

const options = {
	hostname: 'images.webofknowledge.com',
	port: 443,
	method: 'GET'
};

function* fetch() {
	let path = '/WOK46P9/help/WOS/0-9_abrvjt.html';
	let res = yield Request.fetchText(path, options);
	let $ = cheerio.load(res.body);
	let links = $('.paragraph_standard a').map((i, elem) => $(elem).attr('href')).get();
	let mapper = {};

	function* handle(url) {
		res = yield Request.fetchText('/WOK46P9/help/WOS/' + url, options);
		$ = cheerio.load(res.body);
		let all = $('.paragraph_standard').find('dt').eq(0).text();
		let lines = all.split('\n');
		lines.pop();
		while (lines.length) {
			let abbr = lines.pop();
			let name = lines.pop();
			mapper[abbr.trim()] = name.trim();
		}
		fs.writeFileSync('./JOURNALS_ABBR.json', JSON.stringify(mapper, null, 2), {
			encoding: 'utf8',
			flag: 'a'
		});
		mapper = {};
	}
	let d = setInterval(function() {
		if (!links.length) clearInterval(d);
		Helper.wrap(handle)(links.pop())
	}, 1000)
}

const fn = Helper.wrap(fetch);

fn();