#!/usr/bin/env bash
# vim:tabstop=4:noexpandtab
#
# Runs unittests for automua. Example usage:
#
# (1) unittest.sh
# Run all unittests without collecting coverage data.
#
# (2) unittest.sh coverage
# Run all unittests and collect coverage data. This will also
# generate a HTML-based coverage report.

set -euo pipefail

source .venv/bin/activate
if [ -f local/secrets ]; then
	source local/secrets
fi

export AUTOMUA_CONF='tests/unittest.conf'
if [ ! -f ${AUTOMUA_CONF} ]; then
	echo "Missing config file ${AUTOMUA_CONF}" >&2
	exit 1
fi

function usage() {
	echo "Usage: $(basename $0) [coverage]" >&2
	exit 1
}

function run_tests() {
	local cmd="$1"
	shift
	PYTHONPATH=. $cmd -m unittest discover tests/ "$@"
}

function run_coverage() {
	local rcf="--rcfile=tests/coverage.rc"
	local opt="${rcf} --precision=1 --skip-empty"
	run_tests "coverage run ${rcf} --source=automua"
	coverage report ${opt}
	coverage html ${opt}
}

if [ $# -gt 0 ]; then
	if [ "$1" = "coverage" ]; then
		run_coverage
	else
		usage
	fi
else
	run_tests python
fi
