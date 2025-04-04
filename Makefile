.PHONY:
	build clean test run

build:
	docker build . -t take-home
clean:
	docker image rm take-home
test: build
	docker run --rm take-home pytest -vv ./
run: build
	docker run -p 8080:80 --rm take-home