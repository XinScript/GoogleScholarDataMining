const mongoose = require('mongoose');
const Pub = require('./Pub');
const Schema = mongoose.Schema;

const schema = new Schema({
	portrait_url: String,
	name: {
		type: String,
		required: true
	},
	ID: {
		type: String,
		required: true,
		unique: true
	},
	info: {
		type: String,
		default:""
	},
	labels: [String],
	url: {
		type: String,
		required: true,
		unique: true
	},
	index: {
		type: String,
		required: true
	},
	pubs: [Pub]
});

schema.index({
	ID: 1
});

const handleDuplicateError = function(error, doc, next) {
	if (error.name === 'MongoError' && error.code === 11000) {
		next(new Error(`The ID ${doc.ID} already exists in the database. Please enter a unique ID.`));
	} else {
		next();
	}
};

schema.post('save', handleDuplicateError);

module.exports = schema;