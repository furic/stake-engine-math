#!/usr/bin/env python3
"""
Analyze clustering potential in the reel configuration.
"""

import csv
from collections import defaultdict

def analyze_clustering_potential(filename):
    """Analyze clustering potential for each symbol in the reel."""
    
    # Read the reel data
    reels = [[] for _ in range(5)]
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            for i, symbol in enumerate(row):
                if i < 5:  # Only process first 5 reels
                    reels[i].append(symbol.strip())
    
    symbols = ['L1', 'L2', 'L3', 'L4', 'L5']
    
    print("=== CLUSTERING POTENTIAL ANALYSIS ===")
    print()
    
    for symbol in symbols:
        print(f"=== {symbol} CLUSTERING ANALYSIS ===")
        
        # Find all possible clusters for this symbol
        max_cluster_size = 0
        total_clusters = 0
        cluster_sizes = defaultdict(int)
        
        # Check horizontal clusters (same row across reels)
        for row_idx in range(len(reels[0])):
            current_cluster = []
            for reel_idx in range(5):
                if row_idx < len(reels[reel_idx]) and reels[reel_idx][row_idx] == symbol:
                    current_cluster.append((reel_idx, row_idx))
                else:
                    if len(current_cluster) >= 2:  # Adjacent symbols
                        cluster_sizes[len(current_cluster)] += 1
                        total_clusters += 1
                        max_cluster_size = max(max_cluster_size, len(current_cluster))
                    current_cluster = []
            
            # Check final cluster
            if len(current_cluster) >= 2:
                cluster_sizes[len(current_cluster)] += 1
                total_clusters += 1
                max_cluster_size = max(max_cluster_size, len(current_cluster))
        
        # Check vertical clusters (same reel across rows)
        for reel_idx in range(5):
            current_cluster = []
            for row_idx in range(len(reels[reel_idx])):
                if reels[reel_idx][row_idx] == symbol:
                    current_cluster.append((reel_idx, row_idx))
                else:
                    if len(current_cluster) >= 2:
                        cluster_sizes[len(current_cluster)] += 1
                        total_clusters += 1
                        max_cluster_size = max(max_cluster_size, len(current_cluster))
                    current_cluster = []
            
            # Check final cluster
            if len(current_cluster) >= 2:
                cluster_sizes[len(current_cluster)] += 1
                total_clusters += 1
                max_cluster_size = max(max_cluster_size, len(current_cluster))
        
        print(f"Max cluster size: {max_cluster_size}")
        print(f"Total potential clusters: {total_clusters}")
        print(f"Cluster size distribution: {dict(cluster_sizes)}")
        
        # Calculate clustering score (weighted by cluster size)
        score = sum(size * count * size for size, count in cluster_sizes.items())
        print(f"Clustering score: {score}")
        print()

if __name__ == "__main__":
    analyze_clustering_potential("reels/BR0.csv")
