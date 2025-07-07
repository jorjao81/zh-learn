#!/usr/bin/env python3
"""Benchmark script to measure HanziDictionary initialization performance."""

import time
import logging
from typing import List
from statistics import mean, stdev

# Suppress hanzipy debug output for cleaner benchmark results
logging.getLogger("root").setLevel(logging.WARNING)

from hanzipy.dictionary import HanziDictionary  # type: ignore


def benchmark_initialization(num_iterations: int = 5) -> List[float]:
    """Benchmark HanziDictionary initialization times."""
    print(f"Benchmarking HanziDictionary initialization ({num_iterations} iterations)...")

    times = []
    for i in range(num_iterations):
        print(f"  Iteration {i + 1}/{num_iterations}", end=" ", flush=True)

        start_time = time.perf_counter()
        dictionary = HanziDictionary()
        end_time = time.perf_counter()

        init_time = end_time - start_time
        times.append(init_time)
        print(f"- {init_time:.4f}s")

    return times


def benchmark_lookups(dictionary: HanziDictionary, test_chars: List[str], num_iterations: int = 100) -> List[float]:
    """Benchmark dictionary lookup operations."""
    print(f"\nBenchmarking dictionary lookups ({num_iterations} iterations)...")

    times = []
    for i in range(num_iterations):
        start_time = time.perf_counter()

        for char in test_chars:
            dictionary.get_pinyin(char)
            dictionary.definition_lookup(char)

        end_time = time.perf_counter()
        lookup_time = end_time - start_time
        times.append(lookup_time)

    return times


def simulate_current_approach(test_words: List[str]) -> float:
    """Simulate current approach: new dictionary for each word."""
    print(f"\nSimulating current approach (new dictionary per word)...")

    start_time = time.perf_counter()

    for word in test_words:
        # Create new dictionary for each word (current approach)
        dictionary = HanziDictionary()

        for char in word:
            if "\u4e00" <= char <= "\u9fff":  # Chinese character check
                try:
                    dictionary.get_pinyin(char)
                    dictionary.definition_lookup(char)
                except:
                    pass

    end_time = time.perf_counter()
    total_time = end_time - start_time

    print(f"  Total time for {len(test_words)} words: {total_time:.4f}s")
    print(f"  Average per word: {total_time / len(test_words):.4f}s")

    return total_time


def simulate_optimized_approach(test_words: List[str]) -> float:
    """Simulate optimized approach: single dictionary instance."""
    print(f"\nSimulating optimized approach (single dictionary instance)...")

    start_time = time.perf_counter()

    # Create dictionary once (optimized approach)
    dictionary = HanziDictionary()

    processing_start = time.perf_counter()

    for word in test_words:
        for char in word:
            if "\u4e00" <= char <= "\u9fff":  # Chinese character check
                try:
                    dictionary.get_pinyin(char)
                    dictionary.definition_lookup(char)
                except:
                    pass

    processing_end = time.perf_counter()
    end_time = time.perf_counter()

    total_time = end_time - start_time
    processing_time = processing_end - processing_start

    print(f"  Initialization time: {processing_start - start_time:.4f}s")
    print(f"  Processing time: {processing_time:.4f}s")
    print(f"  Total time for {len(test_words)} words: {total_time:.4f}s")
    print(f"  Average per word: {processing_time / len(test_words):.4f}s")

    return total_time


def main():
    """Run the benchmarks."""
    print("=== HanziDictionary Performance Benchmark ===\n")

    # Test characters and words
    test_chars = ["有", "益", "迷", "上", "瞬", "间", "转", "移"]
    test_words = [
        "有益",  # beneficial
        "迷上",  # fascinated with
        "瞬间转移",  # teleportation
        "讨人喜欢",  # charming
        "算无遗策",  # well-conceived plan
        "吟唱",  # chant
        "动弹",  # move
        "冲击波",  # shock wave
        "瞑目",  # close eyes
        "寡不敌众",  # outnumbered
    ]

    # 1. Benchmark initialization times
    init_times = benchmark_initialization(5)
    print(f"\nInitialization Results:")
    print(f"  Mean: {mean(init_times):.4f}s")
    print(f"  Std Dev: {stdev(init_times):.4f}s")
    print(f"  Min: {min(init_times):.4f}s")
    print(f"  Max: {max(init_times):.4f}s")

    # 2. Benchmark lookup operations
    dictionary = HanziDictionary()
    lookup_times = benchmark_lookups(dictionary, test_chars, 50)
    avg_lookup_time = mean(lookup_times)
    print(f"\nLookup Results (per {len(test_chars)} characters):")
    print(f"  Mean: {avg_lookup_time:.4f}s")
    print(f"  Per character: {avg_lookup_time / len(test_chars):.4f}s")

    # 3. Compare approaches
    print(f"\n=== Approach Comparison ===")

    current_time = simulate_current_approach(test_words)
    optimized_time = simulate_optimized_approach(test_words)

    print(f"\n=== Summary ===")
    print(f"Current approach total time: {current_time:.4f}s")
    print(f"Optimized approach total time: {optimized_time:.4f}s")

    if current_time > optimized_time:
        speedup = current_time / optimized_time
        savings = current_time - optimized_time
        print(f"Speedup: {speedup:.2f}x faster")
        print(f"Time savings: {savings:.4f}s ({savings/current_time*100:.1f}%)")
        print("✅ Optimization recommended!")
    else:
        print("❌ No significant improvement with optimization")

    # 4. Recommendations
    print(f"\n=== Recommendations ===")
    avg_init_time = mean(init_times)
    if avg_init_time > 0.1:  # If initialization takes more than 100ms
        print(f"• HanziDictionary initialization is slow ({avg_init_time:.4f}s)")
        print("• Moving to module-level initialization is recommended")
        print("• Expected benefit increases with number of processed entries")
    else:
        print(f"• HanziDictionary initialization is fast ({avg_init_time:.4f}s)")
        print("• Optimization may provide modest benefits")


if __name__ == "__main__":
    main()
