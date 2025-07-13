# Sticky Symbols Test Documentation

## Overview
The `test_sticky_symbols.py` script validates the sticky symbols implementation for the tower defense game without requiring a full game simulation.

## What it tests
1. **Sticky Symbols Logic**: Core functionality of sticky symbol tracking
2. **Prize Configuration**: Validates M/H symbols are properly configured
3. **Implementation Check**: Confirms all required methods exist

## How to run
```bash
cd /Users/r.fu/Projects/stake-engine-math
python test_sticky_symbols.py
```

## Test Coverage

### ✅ Sticky Symbols Logic
- `initialize_sticky_symbols()` method
- `add_sticky_symbol()` method with position tracking
- Duplicate position handling
- Symbol details validation

### ✅ Prize Configuration
- M1-M5 and H1-H5 symbols are configured
- Prize paytable has correct values
- All symbols are properly registered

### ✅ Implementation Check
- Required methods exist in GameExecutables
- Configuration attributes are present
- Integration points are available

## Integration Testing
For complete integration testing, run the actual game and check:
```bash
cd games/0_0_tower_defense
python run.py
```

Then examine the generated books to verify:
- Sticky symbols persist across free spins
- Prize events appear before setFinalWin/updateFreeSpins
- Prize events check board state, not just upgrades

## Maintenance
This test should be run whenever:
- Sticky symbols implementation changes
- Prize configuration is modified
- Game architecture is updated
