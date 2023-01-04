#!/usr/bin/env bash
# vim:ts=4:sw=4:noet
#
# Script to generate automua docs and set package version.
# You need Ruby Gems 'asciidoctor' and 'asciidoctor-diagram' to generate HTML
# documentation.

set -euo pipefail

function usage() {
	local n="$(basename $0)"
	cat >&2 <<EOT
Usage: ${n} {docs}
       ${n} setver {version}
EOT
	exit 1
}

function do_docs() {
	local ad="${HOME}/.gem/ruby/3.1.0/bin/asciidoctor"
	local opt=(
		'-r' 'asciidoctor-diagram'
		'-v'
		'automua.adoc'
	)
	pushd docs >/dev/null
	"${ad}-pdf" -a toc=preamble "${opt[@]}"
	${ad} -a toc=right -o gh-pages/index.html "${opt[@]}"
	popd >/dev/null
}

function do_setver() {
	[ $# -gt 0 ] || usage
	sed -E -i "" "s/^(VERSION = ).+/\1'${1}'/" automua/__init__.py
	sed -E -i "" "s/^(:revnumber:).+/\1 ${1}/" docs/automua.adoc
	sed -E -i "" "s/^(:revdate:).+/\1 $(date +%F)/" docs/automua.adoc
}

[ $# -gt 0 ] || usage
arg="$1"
shift
case "$arg" in
	docs)
		do_$arg
		;;
	setver)
		do_$arg "$@"
		;;
	*)
		usage
		;;
esac
