"""
NEAT Genome implementation for evolve projects
"""

import uuid
import random
import json
from typing import Dict, List, Optional, Tuple


class NEATGenome:
    """Represents a NEAT genome with nodes and connections"""
    
    def __init__(self, input_size: int, output_size: int):
        self.id = str(uuid.uuid4())[:8]
        self.input_size = input_size
        self.output_size = output_size
        self.nodes = []
        self.connections = []
        self.fitness = None  # Can be scalar or list for multi-objective
        self.aggregate_fitness = 0.0
        self.species_id = None
        
        # Initialize nodes
        self._node_counter = 0
        self._initialize_nodes()
    
    def _initialize_nodes(self):
        """Initialize input and output nodes"""
        # Add input nodes
        for i in range(self.input_size):
            self.add_node('input', bias=0.0)
        
        # Add output nodes
        for i in range(self.output_size):
            self.add_node('output', bias=random.uniform(-1, 1))
    
    def add_node(self, node_type: str, bias: float = 0.0) -> int:
        """Add a node and return its ID"""
        node_id = self._node_counter
        self.nodes.append({
            'id': node_id,
            'type': node_type,
            'bias': bias
        })
        self._node_counter += 1
        return node_id
    
    def add_connection(self, from_node: int, to_node: int, weight: float, 
                      innovation: int, enabled: bool = True):
        """Add a connection between nodes"""
        self.connections.append({
            'innovation': innovation,
            'from_node': from_node,
            'to_node': to_node,
            'weight': weight,
            'enabled': enabled
        })
    
    def initialize_minimal(self, connection_probability: float = 0.1, 
                          innovation_counter: int = 0) -> int:
        """Create minimal topology with sparse input→output connections"""
        for i in range(self.input_size):
            for j in range(self.output_size):
                if random.random() < connection_probability:
                    weight = random.uniform(-2, 2)
                    self.add_connection(i, self.input_size + j, weight, innovation_counter)
                    innovation_counter += 1
        return innovation_counter
    
    def to_dict(self) -> Dict:
        """Convert genome to dictionary for serialization"""
        return {
            'id': self.id,
            'nodes': self.nodes,
            'connections': self.connections,
            'fitness': self.fitness,
            'aggregate_fitness': self.aggregate_fitness,
            'species_id': self.species_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict, input_size: int, output_size: int):
        """Create genome from dictionary"""
        genome = cls(input_size, output_size)
        genome.id = data['id']
        genome.nodes = data['nodes']
        genome.connections = data['connections']
        genome.fitness = data.get('fitness')
        genome.aggregate_fitness = data.get('aggregate_fitness', 0.0)
        genome.species_id = data.get('species_id')
        genome._node_counter = max(node['id'] for node in genome.nodes) + 1 if genome.nodes else 0
        return genome
    
    def distance(self, other: 'NEATGenome', c1: float = 1.0, 
                c2: float = 1.0, c3: float = 0.4) -> float:
        """Calculate genetic distance between two genomes"""
        # Implementation details omitted for brevity
        # See full implementation in the original file
        pass