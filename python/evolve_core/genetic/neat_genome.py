"""
NEAT Genome implementation for evolve projects
"""

import random
import uuid


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
        for _i in range(self.input_size):
            self.add_node('input', bias=0.0)

        # Add output nodes
        for _i in range(self.output_size):
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

    def to_dict(self) -> dict:
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
    def from_dict(cls, data: dict, input_size: int = None, output_size: int = None):
        """Create genome from dictionary"""
        nodes = data['nodes']
        if input_size is None:
            input_size = sum(1 for n in nodes if n['type'] == 'input')
        if output_size is None:
            output_size = sum(1 for n in nodes if n['type'] == 'output')
        genome = cls(input_size, output_size)
        genome.id = data['id']
        genome.nodes = nodes
        genome.connections = data['connections']
        genome.fitness = data.get('fitness')
        genome.aggregate_fitness = data.get('aggregate_fitness', 0.0)
        genome.species_id = data.get('species_id')
        genome._node_counter = max(node['id'] for node in genome.nodes) + 1 if genome.nodes else 0
        return genome

    def mutate_weights(self, mutation_rate: float = 0.8, mutation_strength: float = 0.1):
        """Perturb connection weights by Gaussian noise"""
        for conn in self.connections:
            if random.random() < mutation_rate:
                conn['weight'] += random.gauss(0, mutation_strength)

    def crossover(self, other: 'NEATGenome') -> 'NEATGenome':
        """Produce a child genome via NEAT crossover (fitter parent is self)"""
        child = NEATGenome(self.input_size, self.output_size)
        child.nodes = [dict(n) for n in self.nodes]
        child._node_counter = self._node_counter

        other_by_innovation = {c['innovation']: c for c in other.connections}

        child_connections = []
        for conn in self.connections:
            inn = conn['innovation']
            if inn in other_by_innovation:
                # Matching gene: pick randomly from either parent
                chosen = dict(random.choice([conn, other_by_innovation[inn]]))
            else:
                # Disjoint/excess: inherit from the fitter parent (self)
                chosen = dict(conn)
            child_connections.append(chosen)

        child.connections = child_connections
        return child

    def distance(self, other: 'NEATGenome', c1: float = 1.0,
                c2: float = 1.0, c3: float = 0.4) -> float:
        """Calculate genetic distance between two genomes"""
        # Implementation details omitted for brevity
        # See full implementation in the original file
        pass
