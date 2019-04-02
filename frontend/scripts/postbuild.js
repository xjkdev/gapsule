"use strict";

const fs = require('fs');
const path = require('path');
const assert = require('assert');

function deleteFolderRecursive(path) {
    if (fs.existsSync(path)) {
        fs.readdirSync(path).forEach(function (file) {
            var curPath = path + '/' + file;
            if (fs.lstatSync(curPath).isDirectory()) {
                deleteFolderRecursive(curPath);
            } else {
                fs.unlinkSync(curPath);
            }
        });
        fs.rmdirSync(path);
    }
}

function copyFolderRecursive(src, dest) {
    if (!fs.existsSync(dest)) {
        fs.mkdirSync(dest);
    }
    if (fs.existsSync(src)) {
        fs.readdirSync(src).forEach(function (file) {
            const curPath = src + '/' + file;
            const curDestPath = dest + '/' + file;
            if (fs.lstatSync(curPath).isDirectory()) {
                copyFolderRecursive(curPath, curDestPath);
            } else {
                fs.copyFileSync(curPath, curDestPath);
            }
        });
    }
}

function main() {
    const dir = path.dirname(__filename);
    const srcpath = path.join(dir, '../dist');
    const staticpath = path.join(srcpath, "static");
    const indexpath = path.join(srcpath, "index.html");
    const destpath = path.join(dir, "../../gapsule");
    assert(fs.existsSync(destpath), "dest path:" + destpath + " not exists");
    assert(fs.existsSync(srcpath), "src path:" + srcpath + " not exists");
    assert(fs.existsSync(staticpath), "static path:" + staticpath + " not exists");
    assert(fs.existsSync(indexpath), "index path:" + indexpath + " not exists");

    deleteFolderRecursive(path.join(destpath, 'static'));
    copyFolderRecursive(staticpath, path.join(destpath, 'static'));
    fs.copyFileSync(indexpath, path.join(destpath, 'templates/index.html'));

    deleteFolderRecursive(srcpath);
}

if (require.main === module) {
    main();
}
