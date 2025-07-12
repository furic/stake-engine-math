ifeq ($(OS), Windows_NT)
	PYTHON = python
	VENV_PY = env\Scripts\python
else
	PYTHON = python3
	VENV_PY = ./env/bin/python3
endif 

.PHONY: setup run test unittest help clean

help:
	@echo "Available commands:"
	@echo "  make setup                     - Set up virtual environment and install dependencies"
	@echo "  make run GAME=<game_name>      - Run a specific game (e.g., make run GAME=0_0_tower_defense)"
	@echo "  make test                      - Run main project tests"
	@echo "  make unittest GAME=<game_name> - Run all unit tests for a specific game"
	@echo "  make clean                     - Clean up build artifacts"
	@echo ""
	@echo "Examples:"
	@echo "  make unittest GAME=0_0_tower_defense" 

makeVirtual:
	$(PYTHON) -m venv env 

pipInstall: makeVirtual
	$(VENV_PY) -m pip install --upgrade pip

pipPackages: pipInstall
	$(VENV_PY) -m pip install -r requirements.txt

packInstall: pipPackages
	$(VENV_PY) -m pip install -e .

setup: packInstall

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
unittest GAME:
	cd games/$(GAME) && ../../$(VENV_PY) tests/run_tests.py

clean:
	rm -rf env __pycache__ *.pyc