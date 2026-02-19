"""Tests for NEAT genome implementation."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "python"))

from evolve_core.genetic.neat_genome import NEATGenome


class TestNEATGenomeInit:
    def test_creates_input_and_output_nodes(self):
        g = NEATGenome(4, 2)
        assert g.input_size == 4
        assert g.output_size == 2
        input_nodes = [n for n in g.nodes if n["type"] == "input"]
        output_nodes = [n for n in g.nodes if n["type"] == "output"]
        assert len(input_nodes) == 4
        assert len(output_nodes) == 2

    def test_unique_ids(self):
        g1 = NEATGenome(3, 1)
        g2 = NEATGenome(3, 1)
        assert g1.id != g2.id

    def test_initial_fitness_is_none(self):
        g = NEATGenome(2, 2)
        assert g.fitness is None
        assert g.aggregate_fitness == 0.0


class TestNEATGenomeTopology:
    def test_add_node(self):
        g = NEATGenome(2, 1)
        initial_count = len(g.nodes)
        node_id = g.add_node("hidden", bias=0.5)
        assert len(g.nodes) == initial_count + 1
        assert g.nodes[node_id]["type"] == "hidden"
        assert g.nodes[node_id]["bias"] == 0.5

    def test_add_connection(self):
        g = NEATGenome(2, 1)
        g.add_connection(0, 2, weight=0.7, innovation=0)
        assert len(g.connections) == 1
        assert g.connections[0]["from_node"] == 0
        assert g.connections[0]["to_node"] == 2
        assert g.connections[0]["weight"] == 0.7
        assert g.connections[0]["enabled"] is True

    def test_initialize_minimal(self):
        g = NEATGenome(4, 2)
        # With prob=1.0, all connections should be created
        inn = g.initialize_minimal(connection_probability=1.0)
        assert len(g.connections) == 4 * 2  # input × output
        assert inn == 8


class TestNEATGenomeSerialization:
    def test_to_dict_roundtrip(self):
        g = NEATGenome(3, 2)
        g.initialize_minimal(connection_probability=0.5)
        g.fitness = [1.0, 2.0, 3.0]
        d = g.to_dict()
        assert d["id"] == g.id
        assert len(d["nodes"]) == len(g.nodes)
        assert d["fitness"] == [1.0, 2.0, 3.0]
        # Verify JSON-serializable
        json_str = json.dumps(d)
        assert len(json_str) > 0

    def test_from_dict(self):
        g = NEATGenome(3, 2)
        g.initialize_minimal(connection_probability=1.0)
        d = g.to_dict()
        g2 = NEATGenome.from_dict(d)
        assert g2.id == g.id
        assert len(g2.nodes) == len(g.nodes)
        assert len(g2.connections) == len(g.connections)


class TestNEATGenomeMutation:
    def test_mutate_weights(self):
        g = NEATGenome(4, 2)
        g.initialize_minimal(connection_probability=1.0)
        original_weights = [c["weight"] for c in g.connections]
        g.mutate_weights(mutation_rate=1.0, mutation_strength=0.5)
        new_weights = [c["weight"] for c in g.connections]
        # At least some weights should change with rate=1.0
        assert any(abs(o - n) > 1e-10 for o, n in zip(original_weights, new_weights))

    def test_crossover(self):
        g1 = NEATGenome(4, 2)
        g2 = NEATGenome(4, 2)
        g1.initialize_minimal(connection_probability=1.0)
        g2.initialize_minimal(connection_probability=1.0)
        g1.aggregate_fitness = 10.0
        g2.aggregate_fitness = 5.0
        child = g1.crossover(g2)
        assert child.input_size == 4
        assert child.output_size == 2
        assert len(child.connections) > 0
