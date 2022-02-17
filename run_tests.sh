#!/bin/bash

test_to_run="$1"
[ -z $test_to_run ] && test_to_run="tests"

export PYTHONPATH=${PYTHONPATH}:"$(pwd)/src/" &&
./.env/bin/python -m pytest --cov=src --cov-report html --cov-report term-missing "$test_to_run"
