#!/usr/bin/env bash
set -e

part=${1:-patch}
bumpversion $part
