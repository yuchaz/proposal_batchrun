#!/bin/bash
# $1: run_dir, $2 config_dir

export RUN_DIR=$1
cd $RUN_DIR
opsim4 --config $2 --scheduler proposal --save-config --scheduler-timeout=300 -v
