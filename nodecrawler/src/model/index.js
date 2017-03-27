const mongoose = require('mongoose');
const config = require('../config');
mongoose.Promise = require('bluebird');

const conn = mongoose.connect(config.MONGODB_URL).connection;

mongoose.set(config.LOG_LEVEL);

function createModel(modelName) {
	return conn.model(modelName, require('./' + modelName));
};

module.exports = {
	Researcher: createModel('Researcher')
};