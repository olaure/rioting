.PHONY:
	build test run

build:
	docker build . -t take-home

test:
	docker run --rm take-home pytest -vv ./
run:
	docker run -p 8080:80 --rm take-home