const gulp = require('gulp');
const babel = require('gulp-babel');
gulp.task('dev', ['build'], () => {
	gulp.watch('src/*.js', ['build']);
});

gulp.task('build', () => {
	gulp
		.src('src/*.js')
		.pipe(babel())
		.pipe(gulp.dest('lib'))
});