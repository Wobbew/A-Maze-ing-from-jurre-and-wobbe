VENV    = .venv
PYTHON  = $(VENV)/bin/python3
PIP     = $(VENV)/bin/pip

.PHONY: build run clean shell
.PHONY: check lint

build:
	python3 -m build
	cp ./dist/mazegen-1.0.0-py3-none-any.whl .

debug:
	python3 -m pdb a_maze_ing.py default_config.txt

venv:
	python3 -m venv $(VENV)
	@echo "Virtual environment created!"


install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install mlx-2.2-py3-none-any.whl


clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache


run:
	$(PYTHON) a_maze_ing.py config.txt


lint:
	$(PYTHON) -m flake8 --exclude=.venv,mlx .
	$(PYTHON) -m mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs \
		--explicit-package-bases \
		--exclude '^(venv|.venv|env|mlx)/'

