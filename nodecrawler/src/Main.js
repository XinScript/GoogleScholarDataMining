const Spider = require('./service/Scheduler');
const logger = require('winston');
const config = require('./config');

logger.level = config.LOG_LEVEL;

switch (process.argv[2]){
	case '1':
		Spider.Profile();
		break;
	case '2':
		Spider.Pubs(0);
		break;
	default:
		console.log("Input The Mode.");
		process.exit(1);
};