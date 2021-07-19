.PHONY: clean-pyc
PWD=$(shell pwd)
DOCKER=docker run --name returns -it -v ${PWD}:/app -w /app returns-demo

.PHONY: clean-pyc
clean-pyc:
	-find . -name '*.pyc' -delete
	-find . -name '*.pyo' -delete
	-find . -name '*~' -delete
	-find . -name '.mypy_cache' | xargs rm -rf
	-find . -name '.pytest_cache' | xargs rm -rf
	-find . -name '__pycache__' | xargs rm -rf

.PHONY: build-container
build-dev-container:
	docker build -t returns-demo:latest .

.PHONY: enter
enter:
	${DOCKER} bash

.PHONY: run-format
run-format:
	black pipeline
	isort --profile=black pipeline

.PHONY: lint
lint:
	black pipeline --check
	isort --check --profile=black pipeline
	pylama pipeline
	flake8 pipeline
	mypy pipeline