"""Tests for fitness utilities."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "python"))

from evolve_core.utils.fitness import FitnessAggregator, NSGA2Selection


class TestFitnessAggregator:
    def test_weighted_sum_basic(self):
        objectives = {"speed": 0.8, "accuracy": 0.6}
        weights = {"speed": 1.0, "accuracy": 1.0}
        result = FitnessAggregator.weighted_sum(objectives, weights)
        assert abs(result - 0.7) < 0.01

    def test_weighted_sum_unequal_weights(self):
        objectives = {"a": 1.0, "b": 0.0}
        weights = {"a": 3.0, "b": 1.0}
        result = FitnessAggregator.weighted_sum(objectives, weights)
        assert abs(result - 0.75) < 0.01

    def test_weighted_sum_missing_weight(self):
        objectives = {"a": 1.0, "b": 0.5}
        weights = {"a": 1.0}  # b has no weight
        result = FitnessAggregator.weighted_sum(objectives, weights)
        assert abs(result - 1.0) < 0.01

    def test_weighted_sum_empty(self):
        result = FitnessAggregator.weighted_sum({}, {})
        assert result == 0.0

    def test_normalize_and_weight(self):
        objectives = {"score": 50.0}
        weights = {"score": 1.0}
        ranges = {"score": (0.0, 100.0)}
        result = FitnessAggregator.normalize_and_weight(objectives, weights, ranges)
        assert abs(result - 0.5) < 0.01

    def test_normalize_clamps(self):
        objectives = {"x": 2.0}
        weights = {"x": 1.0}
        # No ranges → clamps to [0, 1]
        result = FitnessAggregator.normalize_and_weight(objectives, weights)
        assert abs(result - 1.0) < 0.01


class TestNSGA2Selection:
    def test_non_dominated_sort_simple(self):
        population = [
            {"fitness": [1.0, 0.0]},
            {"fitness": [0.0, 1.0]},
            {"fitness": [0.5, 0.5]},
            {"fitness": [0.1, 0.1]},  # dominated by all above
        ]
        fronts = NSGA2Selection.non_dominated_sort(population)
        assert len(fronts) >= 1
        # Index 3 should be in a later front (dominated)
        assert 3 not in fronts[0]

    def test_select_returns_correct_size(self):
        population = [
            {"fitness": [1.0, 0.0]},
            {"fitness": [0.0, 1.0]},
            {"fitness": [0.5, 0.5]},
            {"fitness": [0.3, 0.3]},
            {"fitness": [0.1, 0.1]},
        ]
        selected = NSGA2Selection.select(population, 3)
        assert len(selected) == 3

    def test_all_equal_fitness(self):
        population = [
            {"fitness": [0.5, 0.5]},
            {"fitness": [0.5, 0.5]},
            {"fitness": [0.5, 0.5]},
        ]
        fronts = NSGA2Selection.non_dominated_sort(population)
        # All non-dominated, should be in first front
        assert len(fronts[0]) == 3
