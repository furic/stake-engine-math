#!/usr/bin/env python3
"""
Analyze the win distribution from the books JSON file.
"""

import json
import sys
from collections import defaultdict

def analyze_wins(filename):
    """Analyze win distribution from a books file."""
    symbol_wins = defaultdict(int)
    total_wins = 0
    
    with open(filename, 'r') as f:
        content = f.read()
        
    # Remove the bracket wrapping and split by '][' to get individual JSON objects
    content = content.strip()
    if content.startswith('[') and content.endswith(']'):
        content = content[1:-1]  # Remove outer brackets
    
    # Split by '][' to separate JSON objects
    json_objects = content.split('][')
    
    for i, json_str in enumerate(json_objects):
        # Add back the brackets if needed
        if not json_str.startswith('['):
            json_str = '[' + json_str
        if not json_str.endswith(']'):
            json_str = json_str + ']'
        
        try:
            games = json.loads(json_str)
            
            for game in games:
                if 'events' in game:
                    for event in game['events']:
                        if event.get('type') == 'winInfo' and 'wins' in event:
                            for win in event['wins']:
                                symbol = win.get('symbol', 'unknown')
                                cluster_size = win.get('clusterSize', 0)
                                win_amount = win.get('win', 0)
                                
                                symbol_wins[symbol] += 1
                                total_wins += 1
                                
                                # Show details for L4 and L5 wins
                                if symbol in ['L4', 'L5']:
                                    print(f"Found {symbol} win: cluster size {cluster_size}, win amount {win_amount}")
                                    
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON object {i}: {e}")
            continue
    
    print(f"\nWin Distribution Analysis:")
    print(f"Total wins found: {total_wins}")
    print(f"Symbol breakdown:")
    
    for symbol in sorted(symbol_wins.keys()):
        count = symbol_wins[symbol]
        percentage = (count / total_wins * 100) if total_wins > 0 else 0
        print(f"  {symbol}: {count} wins ({percentage:.1f}%)")
    
    return symbol_wins, total_wins

if __name__ == "__main__":
    filename = "library/books/books_base.json"
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    
    print(f"Analyzing {filename}...")
    analyze_wins(filename)
