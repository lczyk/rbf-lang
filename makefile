.PHONY: all
all: build_wheel list_wheel

.PHONY: build_wheel
build_wheel: clean
	flit build --format wheel

.PHONY: list_wheel
list_wheel: build_wheel
	unzip -l dist/*.whl

.PHONY: build_sdist
build_sdist: clean
	flit build --format sdist

.PHONY: list_sdist
list_sdist: build_sdist
	tar -vtzf dist/*.tar.gz

.PHONY: build_snap
build_snap: clean
	snapcraft pack

.PHONY: install
install: build_wheel
	pip install --force-reinstall dist/*.whl

.PHONY: install_sdist
install_snap: build_snap
	sudo snap install --dangerous *.snap

.PHONY: clean
clean:
	@rm -rf .mypy_cache .pytest_cache .ruff_cache .tox
	@rm -rf htmlcov .coverage*
	@rm -rf build dist
	@find . -name '*.egg-info' -type d | xargs rm -rf  
	@find . -name '__pycache__' -type d | xargs rm -rf  
	@command -v snapcraft >/dev/null 2>&1 && snapcraft clean

.PHONY: lint
test:
	pytest -v

.PHONY: lint
tox: clean
	tox

.PHONY: lint
lint:
	ruff format . && ruff check --fix . && mypy