#!/bin/bash
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
BOOK_DIR=$SCRIPT_DIR/..
npx honkit serve