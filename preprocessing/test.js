const Model = require('./model');
const Helper = require('./service/Helper');
const mongoose = require('mongoose');
const Profile = Model.Researcher;

function* stats() {
	const profiles = yield Profile.find().limit(1000);
	const hash = {};
	const arr = [];
	for (let i in profiles) {
		for (let j in profiles[i].pubs) {
			// let newSent = profiles[i].pubs[j].venue.replace(/\d+(th)?|\s/g,' ') 
			let venue = profiles[i].pubs[j].venue;
			if(venue&&venue!==''&&venue!=='undefined'){
				let words = venue.split(/\s+/);
				for (let k in words) {
					if (hash[words[k]]) hash[words[k]]++;
					else hash[words[k]] = 1;
				}
			}

			// if(hash[profiles[i].pubs[j].venue!==''||hash[profiles[i].pubs[j].venue!=='undefined')
			// if (hash[profiles[i].pubs[j].venue]) hash[profiles[i].pubs[j].venue]++;
			// else hash[profiles[i].pubs[j].venue] = 1;
		}
	}
	for(let key in hash){
		arr.push([key,hash[key]]);
	}
	arr.sort((a,b)=>b[1]-a[1]);
	for(let i in arr)
		console.log(arr[i][0])
	mongoose.connection.close();
}

let fn = Helper.wrap(stats);
fn();

