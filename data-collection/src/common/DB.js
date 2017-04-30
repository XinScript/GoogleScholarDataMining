const mongoose = require('mongoose');
const config = require('../config');
mongoose.Promise = require('bluebird');
const Helper = require('../common/Helper');

const conn = mongoose.connect(config.MONGODB_URL).connection;

function createModel(modelName) {
	return conn.model(modelName, require('../model/' + modelName));
}

function createModelCopy(modelName) {
	return conn.model(modelName + '__copy', require('../model/' + modelName));
}


module.exports = {
	connection: conn,
	createModel,
	createModelCopy
}