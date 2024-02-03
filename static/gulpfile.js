const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));
const cleanCSS = require('gulp-clean-css');
const autoprefixer = require('gulp-autoprefixer');
const rename = require("gulp-rename");
const imagemin = require('gulp-imagemin');
const uglify = require('gulp-uglify');
const audiosprite = require('gulp-audiosprite');


function gulpStyle(srcPath, distPath) {
    return gulp.src(srcPath)
        .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
        .pipe(rename({suffix: '.min', prefix: ''}))
        .pipe(autoprefixer())
        .pipe(cleanCSS({compatibility: 'ie8'}))
        .pipe(gulp.dest(distPath));
}

gulp.task('styles', function () {
    return gulpStyle("src/sass/**/*.+(scss|sass)", "dist/css")
});

gulp.task('libStyles', function () {
    return gulpStyle("src/libs/**/*.+(scss|sass|css)", "dist/libs")
});

gulp.task('scripts', function () {
    return gulp.src("src/js/**/*.js")
        .pipe(uglify())
        .pipe(gulp.dest("dist/js"));
});

gulp.task('libScripts', function () {
    return gulp.src("src/libs/**/*.js")
        .pipe(uglify())
        .pipe(gulp.dest("dist/libs"));
});

gulp.task('images', function () {
    return gulp.src("src/images/**/*")
        .pipe(imagemin())
        .pipe(gulp.dest("dist/images"))
});

gulp.task('audiosprite', function() {
  return gulp.src('src/sounds/*')
    .pipe(gulp.dest('dist/sounds'));
});

gulp.task('documents', () => {
  return gulp.src("src/documents/**/*")
    .pipe(gulp.dest('dist/documents'));
});

gulp.task('watch', function () {
    gulp.watch("src/sass/**/*.+(scss|sass|css)", gulp.parallel('styles'));
    gulp.watch("src/libs/**/*.+(scss|sass|css)", gulp.parallel('libStyles'));
    gulp.watch("src/js/**/*.js", gulp.parallel('scripts'));
    gulp.watch("src/libs/**/**/*.js", gulp.parallel('libScripts'));
    gulp.watch("src/images/**/*", gulp.parallel('images'));
    gulp.watch("src/sounds/*.(mp3)", gulp.parallel('audiosprite'));
    gulp.watch("src/documents/**/*", gulp.parallel('documents'));
});

gulp.task('default', gulp.parallel('styles', 'libStyles', 'scripts', 'libScripts', 'images', 'audiosprite', 'documents', 'watch'));