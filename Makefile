highlight = \033[1;36m
reset = \033[0m

help:
	@echo "Usage: make ${highlight}<command>${reset}"
	@echo "Commands:"
	@echo "\t${highlight}all${reset}: Build and install this plugin."
	@echo "\t${highlight}build${reset}: Build the package for distribution or installation."
	@echo "\t${highlight}install${reset}: Install the built package locally."
	@echo "\t${highlight}remove${reset}: Remove the local installed package."

all: remove build install

build:
	python3 -m build --wheel
	$(MAKE) docs

docs:
	@cd graphex-webautomation-plugin/docs && ./convertMarkdown.bash

install:
	pip install dist/*.whl
	python3 -m playwright install

remove:
	rm -rf dist build
	pip uninstall -y graphex-webautomation-plugin

.PHONY: all build install remove