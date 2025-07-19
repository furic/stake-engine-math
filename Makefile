PYTHON := python3
VENV_DIR := env
VENV_PY := $(VENV_DIR)/bin/python

ifeq ($(OS),Windows_NT)
	VENV_PY := $(VENV_DIR)\Scripts\python.exe
	ACTIVATE := $(VENV_DIR)\Scripts\activate.bat
else
	ACTIVATE := source $(VENV_DIR)/bin/activate
endif

help:
	@echo "Available commands:"
	@echo "  make setup                     - Set up virtual environment and install dependencies"
	@echo "  make run GAME=<game_name>      - Run a specific game (e.g., make run GAME=0_0_tower_defense)"
	@echo "  make test                      - Run main project tests"
	@echo "  make unit-test GAME=<game_name> - Run all unit tests for a specific game"
	@echo "  make clean                     - Clean up build artifacts"
	@echo ""
	@echo "Examples:"
	@echo "  make unittest GAME=0_0_tower_defense" 

makeVirtual:
	$(PYTHON) -m venv $(VENV_DIR)

pipInstall: makeVirtual
	$(VENV_PY) -m pip install --upgrade pip

pipPackages: pipInstall
	$(VENV_PY) -m pip install -r requirements.txt

packInstall: pipPackages
	$(VENV_PY) -m pip install -e .

setup: packInstall
	@echo "Virtual environment ready."
	@echo "To activate it, run:"
	@echo "$(ACTIVATE)"


run GAME:
	$(VENV_PY) games/$(GAME)/run.py
	@echo "Checking compression setting..."
	@if grep -q "compression = False" games/$(GAME)/run.py; then \
		echo "Compression is disabled, formatting books files..."; \
		$(VENV_PY) scripts/format_books_json.py games/$(GAME) || echo "Warning: Failed to format books files"; \
	else \
		echo "Compression is enabled, skipping formatting."; \
	fi

test:
	cd $(CURDIR)
	pytest tests/

# Game-specific unit tests - usage: make unittest GAME=0_0_tower_defense
# Runs all unit tests for the specified game
unit-test GAME:
	cd games/$(GAME) && ../../$(VENV_PY) tests/run_tests.py

clean:
	rm -rf env __pycache__ *.pyc