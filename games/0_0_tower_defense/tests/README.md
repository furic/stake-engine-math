# Tower Defense Game - Unit Tests

This directory contains unit tests for the tower defense game implementation.

## Test Structure

```
tests/
├── __init__.py                    # Package initialization
├── README.md                     # This file
├── run_tests.py                  # Test runner for all tests
├── test_sticky_symbols.py        # Sticky symbols functionality tests
└── integration_test_example.py   # Example integration test template
```

## Running Tests

### Option 1: From tower defense game directory
```bash
cd games/0_0_tower_defense
python tests/test_sticky_symbols.py
```

### Option 2: From project root
```bash
python -m games.0_0_tower_defense.tests.test_sticky_symbols
```

### Option 3: Run all tests
```bash
cd games/0_0_tower_defense
python tests/run_tests.py
```

## Test Coverage

### `test_sticky_symbols.py`
Tests the sticky symbols functionality including:
- ✅ Sticky symbols initialization
- ✅ Adding sticky symbols to tracking
- ✅ Position deduplication logic
- ✅ Prize configuration validation
- ✅ Upgrade mapping validation
- ✅ Implementation existence checks

## Adding New Tests

To add new unit tests:

1. Create a new test file: `test_<feature_name>.py`
2. Follow the existing pattern with test functions
3. Add import to `run_tests.py`
4. Update this README

## Test Philosophy

These unit tests focus on:
- **Isolated functionality** - Test individual components without full game simulation
- **Fast execution** - Quick feedback during development
- **Clear assertions** - Easy to understand what went wrong
- **Game-specific logic** - Tower defense specific mechanics and configurations

## Integration Testing

For full integration testing, use the main game runner and check generated books:
```bash
cd games/0_0_tower_defense
python run.py
```

Then analyze the generated books to ensure complete functionality.
