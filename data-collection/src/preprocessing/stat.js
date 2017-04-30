function portrait(profiles) {
	let count = 0;
	profiles.forEach((profile) => {
		if (profile.portrait_url !== '') count++;
	});
	console.log('Profiles with portraits:'+count);
	console.log(`Percetages:${count/profiles.length}`);
	return count;
}
module.exports = {
	portrait,
}