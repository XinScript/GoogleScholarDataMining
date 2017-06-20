const Request = require('./Request');
const Parser = require('./Parser');
const config = require('../config');
const Researcher = require('../model').Researcher;
const logger = require('winston');
const Helper = require('../common/Helper');
const fs = require('fs');

logger.level = config.LOG_LEVEL;

const interval = (60 / config.REQ_PER_MIN) * 1000;

function* fetchProfile(START_URL) {
	let pool = config.START_URL.map(url => url);
	let count = 0;
	const urls = yield Researcher.find({}, 'url -_id');
	const seen_URLs = new Set(urls.map(obj => obj.url));

	function* handle() {
		if (pool.length) {
			const path = pool.shift();
			if (!seen_URLs.has(path)) {
				const res = yield Request.fetchText(path, config.HOSTNAME);
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
					yield Researcher.create(profile);
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
	let pool = yield Researcher.find({
		'pubs': {
			'$size': cstart
		}
	}, 'url _id').limit(config.PUBS_LIMIT).exec();
	let count = 0;

	function* handle() {
		if (pool.length) {
			const o = pool.shift();
			let _id = o._id;
			let path = o.url;
			if (path.indexOf('cstart') == -1) {
				path = path + `&cstart=${cstart}&pagesize=100`;
			}
			const res = yield Request.fetchText(path, config.HOSTNAME);
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
				const profile = yield Researcher.findById(_id);
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

function* fetchPortrait(count) {
	const crawledUrls = new Set(fs.readdirSync(`${__dirname}/../resource/portraits`).filter(filename => filename.endsWith('jpeg')).map(id => id.replace('.jpeg', '')));
	const profiles = yield Researcher.find({}, 'portrait_url').limit(count).exec().filter(profile => profile.portrait_url !== '' && !crawledUrls.has(profile._id.toString()));

	function* handle() {
		if (profiles.length > 0) {
			let profile = profiles.pop();
			let url = profile.portrait_url;
			let res = yield Request.fetchImg(url);
			fs.writeFileSync(`${__dirname}/../resource/portraits/${profile._id}.jpeg`, res.body.read());
			logger.info(`Get Portrait from ${url}, _id:${profile._id}`);
		} else {
			logger.info('Protrait fetching done.');
			clearInterval(handler);
		}

	}
	const handler = setInterval(Helper.wrap(handle), interval);
}

function* fetchCollaborator(count){
	const pool = yield Researcher.find({'collaborator':{'$exists':false}}, 'ID').limit(count).exec();

	function* handle() {
		if (pool.length) {
			const profile = pool.shift();
			const res = yield Request.fetchText(`/citations?view_op=list_colleagues&hl=en&oe=ASCII&user=${profile.ID}`, config.HOSTNAME);
			
				if (!res.body) {
					logger.info(`Request url:${res.url} timeout, reappending to pool.`);
				} else {
					logger.info(`Start Parsing ${res.url}`);
					let cols = Parser.parseCollaborator(res.body);
					profile.collaborator = cols;
					yield profile.save();
					logger.info(`Sucessful Profile Fetching:${++count}`)
			}
		} else {
			clearInterval(handler);
		}
	}
	const handler = setInterval(Helper.wrap(handle), interval);

}

module.exports = {
	fetchProfiles: Helper.wrap(fetchProfile),
	fetchPubs: Helper.wrap(fetchPubs),
	fetchPortrait: Helper.wrap(fetchPortrait),
	fetchCollaborator:Helper.wrap(fetchCollaborator)
}
