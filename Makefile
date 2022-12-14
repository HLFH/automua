PKG 		= contrib/package.sh
RUN_LDAP_TESTS	?= 0

.PHONY:	docs push usage

usage:
	@echo >&2 "Usage: make {devtest | docs | push | publish | gh-pages}"
	@exit 1

devtest:
	test_suite="tests"
	AUTOMUA_CONF=tests/unittest.conf RUN_LDAP_TESTS=$(RUN_LDAP_TESTS) PYTHONPATH=. coverage run --source automua -m pytest
	coverage html --rcfile=tests/coverage.rc

docs:
	$(PKG) docs

gh-pages:
	git add docs/gh-pages
	git commit -m 'docs generic update'
	git subtree push --prefix docs/gh-pages origin gh-pages

push:
	@for r in $(shell git remote); do git push $$r; done

publish:
	hatch clean
	hatch build
	hatch publish

