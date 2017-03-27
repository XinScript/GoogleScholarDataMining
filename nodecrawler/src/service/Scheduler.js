'use strict';

const Request = require('./Request');
const Parser = require('./Parser');
const config = require('../config');
const Model = require('../model');
const logger = require('winston');
const co = require('co');
const Helper = require('./Helper');

const interval = (60 / config.REQ_PER_MIN) * 1000;

function* fetchProfile(START_URL) {
	let pool = config.START_URL.map(url => url);
	let count = 0;
	const urls = yield Model.Researcher.find({}, 'url -_id');
	const seen_URLs = new Set(urls.map((obj)=>obj.url));
	// const journals = new Set();
	// let limit = config.PROFILE_LITMIT;

	function* handle() {
		if (pool.length) {
			const path = pool.shift();
			if (!seen_URLs.has(path)) {
				const res = yield Request.fetch(path);
				if (!res.body) {
					logger.info(`Request url:${res.url} timeout, reappending to pool.`);
					pool.append(res.url);
				} else {
					seen_URLs.add(path);
					logger.info(`Start Parsing ${res.url}`);
					let [profile, urls] = Parser.parseProfile(res.body);
					profile.url = res.url;
					profile.ID = res.url.split('user=')[1].substring(0, 12);
					pool = pool.concat(urls);
					yield Model.Researcher.create(profile);
					logger.info(`Sucessful Profile Fetching:${++count}`)
				}
			}
		} else {
			clearInterval(handler);
		}
	}
	const handler = setInterval(Helper.wrap(handle), interval);
}

function* fetchPubs(cs) {
	let cstart = cs;
	let pool = yield Model.Researcher.find({'pubs': {'$size': cstart}}, 'url _id').limit(config.PUBS_LIMIT).exec();
	let count = 0;
	function* handle() {
		if (pool.length) {
			const o = pool.shift();
			let _id = o._id;
			let path = o.url;
			if (path.indexOf('cstart') == -1) {
				path = path + `&cstart=${cstart}&pagesize=100`;
			}
			const res = yield Request.fetch(path);
			if (!res.body) {
				logger.info(`Request url:${res.url} timeout, reappending to pool.`);
				pool.append({
					"url": res.url,
					"_id": _id
				});
			} else {
				logger.info(`Start Parsing ${res.url}`);
				let [pubs, ifContinue] = Parser.parsePubs(res.body);
				if (ifContinue) {
					let cs = parseInt(res.url.split('cstart=')[1].split('&')[0]) + 100;
					let url = res.url.replace(/cstart=(.+)&/, `cstart=${cs}&`);
					pool.push({
						"url": url,
						"_id": _id
					});
				}
				const profile = yield Model.Researcher.findById(_id);
				profile.pubs = profile.pubs.concat(pubs);
				yield profile.save();
				logger.info(`Successful Pubs Fetching:${++count}`);
			}
		} else {
			clearInterval(handler);
		}
	}
	const handler = setInterval(Helper.wrap(handle), interval);
}



module.exports = {
	Profile: Helper.wrap(fetchProfile),
	Pubs: Helper.wrap(fetchPubs)
}