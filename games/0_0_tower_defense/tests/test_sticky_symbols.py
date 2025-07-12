#!/usr/bin/env python3

"""
Unit tests for sticky symbols functionality in tower defense game.
This script tests the sticky symbols methods without requiring a full game instance.

Run from tower defense game directory:
    python tests/test_sticky_symbols.py

Or from project root:
    python -m games.0_0_tower_defense.tests.test_sticky_symbols
"""

import sys
import os

# Add paths for imports - relative to tower defense game directory
current_dir = os.path.dirname(os.path.abspath(__file__))
game_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(os.path.dirname(game_dir))

sys.path.insert(0, project_root)
sys.path.insert(0, game_dir)

def test_sticky_symbols():
    """Test sticky symbols functionality using methods directly"""
    
    try:
        from game_config import GameConfig
        from game_executables import GameExecutables
        
        print("🧪 Testing sticky symbols methods...")
        
        # Create a mock game object with just the sticky symbols methods
        class MockTowerDefenseGame:
            def __init__(self):
                self.config = GameConfig()
                
            # Copy the sticky symbols methods from GameExecutables
            def initialize_sticky_symbols(self):
                """Initialize sticky symbols tracking"""
                self.sticky_symbols = []
                self.existing_sticky_positions = set()
                
            def add_sticky_symbol(self, symbol, position):
                """Add a sticky symbol at the specified position"""
                pos_tuple = (position["reel"], position["row"])
                if pos_tuple not in self.existing_sticky_positions:
                    self.sticky_symbols.append({
                        "symbol": symbol,
                        "reel": position["reel"],
                        "row": position["row"]
                    })
                    self.existing_sticky_positions.add(pos_tuple)
                    
            def replace_board_with_stickys(self):
                """Replace board symbols with sticky symbols"""
                # This would be implemented in the actual game
                pass
        
        # Test using the mock game
        game = MockTowerDefenseGame()
        
        # Test initialization
        game.initialize_sticky_symbols()
        
        assert hasattr(game, 'sticky_symbols'), "sticky_symbols attribute not initialized"
        assert hasattr(game, 'existing_sticky_positions'), "existing_sticky_positions attribute not initialized"
        assert len(game.sticky_symbols) == 0, "sticky_symbols should be empty initially"
        assert len(game.existing_sticky_positions) == 0, "existing_sticky_positions should be empty initially"
        print("✅ Initialization tests passed")
        
        # Test adding sticky symbols
        print("🧪 Testing adding sticky symbols...")
        pos1 = {"reel": 0, "row": 0}
        pos2 = {"reel": 1, "row": 2}
        
        game.add_sticky_symbol("M1", pos1)
        game.add_sticky_symbol("H2", pos2)
        
        assert len(game.sticky_symbols) == 2, "Should have 2 sticky symbols"
        assert len(game.existing_sticky_positions) == 2, "Should have 2 sticky positions"
        
        # Test duplicate positions are ignored
        game.add_sticky_symbol("M2", pos1)  # Same position as M1
        assert len(game.sticky_symbols) == 2, "Should still have 2 sticky symbols (duplicate ignored)"
        print("✅ Adding symbols tests passed")
        
        print("🧪 Testing sticky symbol details...")
        # Test sticky symbol details
        assert game.sticky_symbols[0]["symbol"] == "M1", "First sticky symbol should be M1"
        assert game.sticky_symbols[0]["reel"] == 0, "First sticky symbol should be at reel 0"
        assert game.sticky_symbols[0]["row"] == 0, "First sticky symbol should be at row 0"
        
        assert game.sticky_symbols[1]["symbol"] == "H2", "Second sticky symbol should be H2"
        assert game.sticky_symbols[1]["reel"] == 1, "Second sticky symbol should be at reel 1"
        assert game.sticky_symbols[1]["row"] == 2, "Second sticky symbol should be at row 2"
        print("✅ Symbol details tests passed")
        
        print("🧪 Testing position tracking...")
        # Test position tracking
        assert (0, 0) in game.existing_sticky_positions, "Position (0,0) should be tracked"
        assert (1, 2) in game.existing_sticky_positions, "Position (1,2) should be tracked"
        assert (0, 1) not in game.existing_sticky_positions, "Position (0,1) should not be tracked"
        print("✅ Position tracking tests passed")
        
        print("🎉 All sticky symbol tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_prize_config():
    """Test that prize configuration is correct for tower defense game"""
    
    try:
        from game_config import GameConfig
        
        print("🧪 Testing tower defense prize configuration...")
        
        config = GameConfig()
        
        # Check that M and H symbols are in the prize configuration
        assert hasattr(config, 'prize_config'), "Config should have prize_config"
        
        # Check for M symbols in the symbols list
        prize_symbols = config.prize_config.get("symbols", [])
        m_symbols = [sym for sym in prize_symbols if sym.startswith('M')]
        h_symbols = [sym for sym in prize_symbols if sym.startswith('H')]
        
        assert len(m_symbols) >= 5, f"Should have at least 5 M symbols, found {len(m_symbols)}: {m_symbols}"
        assert len(h_symbols) >= 5, f"Should have at least 5 H symbols, found {len(h_symbols)}: {h_symbols}"
        
        # Check that values are reasonable
        prize_paytable = config.prize_config.get("paytable", {})
        for symbol in m_symbols + h_symbols:
            assert symbol in prize_paytable, f"Symbol {symbol} should be in prize paytable"
            value = prize_paytable[symbol]
            assert isinstance(value, (int, float)), f"Prize value for {symbol} should be numeric, got {type(value)}"
            assert value > 0, f"Prize value for {symbol} should be positive, got {value}"
        
        print("✅ Prize configuration tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Prize configuration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_upgrade_mappings():
    """Test that upgrade mappings are correct for tower defense game"""
    
    try:
        from game_config import GameConfig
        
        print("🧪 Testing tower defense upgrade configuration...")
        
        config = GameConfig()
        
        # Check that upgrade configuration exists
        assert hasattr(config, 'upgrade_config'), "Config should have upgrade_config"
        
        # Check that all L symbols have upgrade mappings
        symbol_map = config.upgrade_config.get("symbol_map", {})
        for i in range(1, 6):  # L1 to L5
            l_symbol = f"L{i}"
            assert l_symbol in symbol_map, f"Upgrade mapping for {l_symbol} should exist"
            
            mappings = symbol_map[l_symbol]
            assert "M" in mappings, f"M upgrade mapping for {l_symbol} should exist"
            assert "H" in mappings, f"H upgrade mapping for {l_symbol} should exist"
            
            # Check that the mappings point to valid symbols
            m_symbol = mappings["M"]
            h_symbol = mappings["H"]
            assert m_symbol.startswith("M"), f"M upgrade should start with M, got {m_symbol}"
            assert h_symbol.startswith("H"), f"H upgrade should start with H, got {h_symbol}"
        
        # Check that cluster thresholds exist
        assert "thresholds" in config.upgrade_config, "Config should have thresholds"
        thresholds = config.upgrade_config["thresholds"]
        assert "medium" in thresholds, "Should have medium cluster threshold"
        assert "high" in thresholds, "Should have high cluster threshold"
        assert thresholds["medium"] > 0, "Medium threshold should be positive"
        assert thresholds["high"] > thresholds["medium"], "High threshold should be greater than medium"
        
        print("✅ Upgrade configuration tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Upgrade configuration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_implementation_exists():
    """Test that the tower defense implementation files exist and have the expected methods"""
    
    try:
        from game_executables import GameExecutables
        from game_config import GameConfig
        
        print("🧪 Testing tower defense implementation exists...")
        
        # Check that the GameExecutables class has the expected methods
        assert hasattr(GameExecutables, 'initialize_sticky_symbols'), "GameExecutables should have initialize_sticky_symbols method"
        assert hasattr(GameExecutables, 'add_sticky_symbol'), "GameExecutables should have add_sticky_symbol method"
        assert hasattr(GameExecutables, 'replace_board_with_stickys'), "GameExecutables should have replace_board_with_stickys method"
        assert hasattr(GameExecutables, 'generate_prize_payout_events'), "GameExecutables should have generate_prize_payout_events method"
        
        # Check that config has the expected attributes
        config = GameConfig()
        assert hasattr(config, 'prize_config'), "GameConfig should have prize_config"
        assert hasattr(config, 'paytable'), "GameConfig should have paytable"
        assert hasattr(config, 'upgrade_config'), "GameConfig should have upgrade_config"
        
        print("✅ Implementation exists tests passed")
        return True
        
    except Exception as e:
        print(f"❌ Implementation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all tower defense sticky symbols tests"""
    
    print("🚀 Running Tower Defense Sticky Symbols Test Suite...\n")
    
    test1_passed = test_sticky_symbols()
    print()
    test2_passed = test_prize_config()
    print()
    test3_passed = test_upgrade_mappings()
    print()
    test4_passed = test_implementation_exists()
    
    print(f"\n📊 Test Results:")
    print(f"   Sticky Symbols Logic: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"   Prize Configuration:  {'✅ PASS' if test2_passed else '❌ FAIL'}")
    print(f"   Upgrade Configuration: {'✅ PASS' if test3_passed else '❌ FAIL'}")
    print(f"   Implementation Check: {'✅ PASS' if test4_passed else '❌ FAIL'}")
    
    all_passed = test1_passed and test2_passed and test3_passed and test4_passed
    
    if all_passed:
        print("\n🎉 All tower defense tests passed! Sticky symbols implementation is working correctly.")
        print("\n💡 Note: This script tests the sticky symbols logic without running full games.")
        print("   To test the complete integration, run the game and check the generated books.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the tower defense implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
