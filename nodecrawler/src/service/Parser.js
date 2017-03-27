'use strict';
const cheerio = require('cheerio');

function parseProfile(body) {
	const profile = {};
	const $ = cheerio.load(body);

	profile.name = $('#gsc_prf_in').text();
	profile.labels = $('.gsc_prf_ila').map((i, elem) => $(elem).text()).get();
	profile.info = $('div[class=gsc_prf_il]').first().find('a').text();
	profile.portrait_url = $('#gsc_prf_pup').attr('src');
	profile.index = $('#gsc_rsb_st tr').eq(3).find('td').eq(2).text();

	if (profile.portrait_url === '/citations/images/avatar_scholar_150.jpg') {
		profile.portrait_url = '';
	}

	if (!profile.info) {
		profile.info = $('.gsc_prf_il').first().text();
	}

	profile.pubs = [];

	const urls = $('.gsc_rsb_aa').map((i, elem) => $(elem).attr('href')).get();

	return [profile, urls];
};

function parsePubs(body) {
	const $ = cheerio.load(body);
	const parent = $('#gsc_a_b .gsc_a_tr');
	const n = parent.length;
	const pubs = []
	for (let i = 0; i < n; i++) {
		const pub = {};
		const current = parent.eq(i);
		pub.title = current.find('.gsc_a_t a').text();
		if (pub.title == ''||pub.title.toLowerCase() == 'untitled'){
			continue;
		}
		pub.url = current.find('.gsc_a_t a').attr('href');
		pub.author = current.find('.gsc_a_t div').eq(0).text();
		pub.venue = current.find('.gsc_a_t div').eq(1).text();
		pub.citation = current.find('.gsc_a_c a').text();
		pub.year = current.find('.gsc_a_y span').text();

		let v = pub.venue;

		pub.venue = v.replace(/[(!@#$*\'%"),.\/-\d]/g,'').replace(/\s+/g,' ');
		pubs.push(pub);
	};
	const ifContinue = n == 100 ? true : false;
	return [pubs, ifContinue];
};

module.exports = {
	parsePubs,
	parseProfile
};