VENV    = .venv
PYTHON  = $(VENV)/bin/python
PIP     = $(VENV)/bin/pip

.PHONY: build run clean shell

build:
	echo "making Virtual environment"
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	tar -xvzf mlx_CLXV-2.2.tgz
	cd mlx_CLXV && PATH=$(VENV)/bin:$$PATH $(MAKE)
	$(PIP) install mlx_CLXV/python/dist/mlx-2.2-py3-none-any.whl


run:
	$(PYTHON) visual/tmpmain.py

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete