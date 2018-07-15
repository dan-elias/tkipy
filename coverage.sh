#!/usr/bin/env bash
set -e

pytest --cov-report term-missing --cov-report html --cov=tkipy
echo coverage report is at: file://`pwd`/htmlcov/index.html
