#!/usr/bin/env python3
"""
Test script for the analyze_wins function with sample data.
"""

import json
import tempfile
from analyze_wins import analyze_wins

def create_sample_books_data():
    """Create sample books data for testing."""
    sample_data = [
        # Spin 1: Regular win without free spin trigger
        [
            {
                "events": [
                    {"type": "reveal", "board": []},
                    {
                        "type": "win",
                        "details": [
                            {"symbol": "L1", "count": 3, "amount": 500},
                            {"symbol": "L2", "count": 4, "amount": 800}
                        ]
                    }
                ]
            }
        ],
        # Spin 2: Win with free spin trigger
        [
            {
                "events": [
                    {"type": "reveal", "board": []},
                    {
                        "type": "win",
                        "details": [
                            {"symbol": "L4", "count": 5, "amount": 1200}
                        ]
                    },
                    {"type": "triggerFreeSpins", "total": 10}
                ]
            }
        ],
        # Spin 3: No win
        [
            {
                "events": [
                    {"type": "reveal", "board": []}
                ]
            }
        ],
        # Spin 4: Another regular win
        [
            {
                "events": [
                    {"type": "reveal", "board": []},
                    {
                        "type": "win",
                        "details": [
                            {"symbol": "L5", "count": 6, "amount": 2000}
                        ]
                    }
                ]
            }
        ]
    ]
    return sample_data

def test_analyze_wins():
    """Test the analyze_wins function with sample data."""
    sample_data = create_sample_books_data()
    
    # Create a temporary file with the sample data
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        # Write data in the format expected by analyze_wins
        for i, game_data in enumerate(sample_data):
            if i > 0:
                f.write('][')
            json.dump(game_data, f)
        
        temp_filename = f.name
    
    print("Testing analyze_wins with sample data:")
    print("=" * 50)
    
    try:
        # Analyze the sample data
        result = analyze_wins(temp_filename)
        
        print("\nExpected results:")
        print("- Total spins: 4")
        print("- Spins with wins: 3")
        print("- Spins with wins (excluding FS triggers): 2")
        print("- Total individual wins: 4")
        
    finally:
        # Clean up the temporary file
        import os
        os.unlink(temp_filename)

if __name__ == "__main__":
    test_analyze_wins()
