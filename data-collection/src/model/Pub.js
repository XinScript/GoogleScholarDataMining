const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const schema = new Schema({
  title: {
    type: String,
    required: true
  },
  url: {
    type: String,
    required: true
  },
  venue: String,
  author: {
    type: String
  },
  year: String,
  citation: String
});

// const handleDuplicateError = function (error, doc, next) {
//   if (error.name === 'MongoError' && error.code === 11000) {
//     next(new Error(`The user name ${doc.username} already exists in the database. Please enter a unique name.`));
//   } else {
//     next();
//   }
// };

// schema.post('save', handleDuplicateError);

module.exports = schema;