#!/usr/bin/env python3

"""
Test runner for all tower defense game unit tests.
Run from tower defense game directory:
    python tests/run_tests.py

Or from project root:
    python -m games.tower_treasures.tests.run_tests
"""

import sys
import os

# Add paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
game_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(os.path.dirname(game_dir))

sys.path.insert(0, project_root)
sys.path.insert(0, game_dir)

def run_all_tests():
    """Run all tower defense unit tests"""
    
    print("🏗️  Tower Defense Game - Unit Test Suite")
    print("=" * 50)
    
    # Import and run sticky symbols tests
    try:
        from test_sticky_symbols import run_all_tests as run_sticky_tests
        sticky_result = run_sticky_tests()
        print("\n" + "=" * 50)
        
        # Add more test modules here as they're created
        # from test_cluster_logic import run_all_tests as run_cluster_tests
        # cluster_result = run_cluster_tests()
        
        overall_result = sticky_result
        
        if overall_result == 0:
            print("🎉 All tower defense unit tests passed!")
        else:
            print("❌ Some tower defense unit tests failed!")
            
        return overall_result
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
