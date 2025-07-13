# Stake Engine Math SDK

Welcome to [Stake Engine Math SDK](https://engine.stake.com/)!

The Math SDK is a Python-based engine for defining game rules, simulating outcomes, and optimizing win distributions. It generates all necessary backend and configuration files, lookup tables, and simulation results.
   

For technical details [view the docs](https://stakeengine.github.io/math-sdk/)

## Improvements & Added Features

This repository includes several enhancements and new features compared to the [original SDK](https://stakeengine.github.io/math-sdk/):

### 📝 **JSON Output Formatting**
- **Automatic JSON formatting** when compression is disabled - books files are automatically formatted with proper indentation for better readability
- **Smart formatting logic** that keeps simple name objects (like `{"name": "L1"}`) compact while pretty-printing complex structures
- **Integrated formatting pipeline** - formatting runs automatically after simulation via the Makefile
- **Advanced error handling** with JSONL reconstruction capabilities for corrupted files

### 🏷️ **Standardized Event Names**
- **Event constants system** - All event types are now defined in `EventConstants` enum for consistency
- **Centralized event management** - No more hardcoded event strings scattered throughout the codebase
- **Type safety** - Using constants prevents typos and ensures consistent event naming across the SDK
- **Comprehensive event coverage** - Standardized events for wins, free spins, tumbles, reveals, and special symbols

### 🧪 **Unit Testing Framework**
- **Game-specific unit tests** - Each game can have its own dedicated test suite
- **Isolated testing** - Test individual components without requiring full game simulation  
- **Fast execution** - Quick feedback during development with focused test cases
- **Test automation** - Integrated with Makefile for easy test running (`make unittest GAME=<game_name>`)
- **Example implementations** - Tower defense game includes comprehensive sticky symbols tests

### 🔧 **Enhanced Development Workflow**
- **Improved Makefile** - Added commands for unit testing and automated formatting
- **Better error reporting** - More detailed error messages and debugging information
- **Documentation enhancements** - Comprehensive docs for events, testing, and formatting systems
- **Development tools** - Scripts for JSON formatting and game analytics

### 📊 **Advanced Analytics & Debugging**
- **Enhanced game analytics** - Better tools for analyzing simulation results and win distributions
- **Force record improvements** - More detailed tracking of custom-defined events and search keys
- **Simulation validation** - Better verification tools for ensuring data integrity
- **Statistics export** - Improved JSON and Excel export capabilities for PAR sheets

### 🎮 **Game Development Features**
- **Sticky symbols support** - Built-in framework for implementing sticky symbol mechanics
- **Event-driven architecture** - Enhanced event system for better game state management
- **Flexible configuration** - More options for customizing game behavior and output formats
- **Template improvements** - Better game templates and examples for faster development
   

# Installation
 
This repository requires Python3 (version >= 3.12), along with the PIP package installer.
If the included optimization algorithm is being used, Rust/Cargo will also need to be installed.

It is recommended to use [Make](https://www.gnu.org/software/make/) and setup the engine by running:
```sh
make setup
```

Alternatively, visit our [Setup and Installation page](https://stakeengine.github.io/math-sdk/math_docs/general_overview/) for more details.

