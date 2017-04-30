const gulp = require('gulp');
const babel = require('gulp-babel');
const spider = require('./src/service/Scheduler');
const logger = require('winston');
const preprocess = require('./src/preprocessing/cleaner');


gulp.task('dev', ['build'], () => {
	gulp.watch('src/*.js', ['build']);
});

gulp.task('pub',()=>{
	spider.fetchPubs(300);
});

gulp.task('profile',()=>{
	spider.fetchProfiles();
});

gulp.task('clean',()=>{
	preprocess.clean();
});

gulp.task('portrait',()=>{
	spider.fetchPortrait(0);
})

gulp.task('build', () => {
	gulp
		.src('src/*.js')
		.pipe(babel())
		.pipe(gulp.dest('lib'))
});
