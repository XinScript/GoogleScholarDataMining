const co = require('co');

function wrap(fn) {
	return function(...args) {
		co(fn.apply(null,args)).catch((err) => {
			console.log(err);
		})
	}
};

module.exports = {
	wrap,
}