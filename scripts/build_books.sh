#!/bin/bash
export PATH="/Applications/calibre.app/Contents/MacOS:$PATH"
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
BOOK_DIR=$SCRIPT_DIR/..
BUILD_DIR=$BOOK_DIR/build/Release/book

mkdir -p $BUILD_DIR
echo Building PDF...
npx honkit pdf $BOOK_DIR $BUILD_DIR/rfc4918_cn.pdf
echo Building EPUB...
npx honkit epub $BOOK_DIR $BUILD_DIR/rfc4918_cn.epub
echo Building MOBI...
npx honkit mobi $BOOK_DIR $BUILD_DIR/rfc4918_cn.mobi
