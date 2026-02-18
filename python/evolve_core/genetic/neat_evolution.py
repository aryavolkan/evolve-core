"""
NEAT Evolution engine for evolve projects
"""

import random
import copy
from typing import List, Dict, Callable, Optional, Tuple
from .neat_genome import NEATGenome


class NEATEvolution:
    """NEAT Evolution algorithm implementation"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.population_size = config.get('population_size', 100)
        self.compatibility_threshold = config.get('compatibility_threshold', 3.0)
        self.c1 = config.get('c1', 1.0)  # Excess coefficient
        self.c2 = config.get('c2', 1.0)  # Disjoint coefficient  
        self.c3 = config.get('c3', 0.4)  # Weight coefficient
        
        self.innovation_counter = 0
        self.node_counter = 0
        
        self.population: List[NEATGenome] = []
        self.species: List[List[NEATGenome]] = []
        self.generation = 0
        
        # Configurable callbacks
        self.fitness_function: Optional[Callable] = None
    
    def initialize_population(self, input_size: int, output_size: int):
        """Create initial population with minimal topology"""
        self.population = []
        for _ in range(self.population_size):
            genome = NEATGenome(input_size, output_size)
            self.innovation_counter = genome.initialize_minimal(
                connection_probability=self.config.get('initial_connection_probability', 0.1),
                innovation_counter=self.innovation_counter
            )
            self.population.append(genome)
        
        # Update node counter
        if self.population:
            self.node_counter = self.population[0]._node_counter
    
    def evolve_generation(self) -> List[NEATGenome]:
        """Run one generation of evolution"""
        # Implementation details omitted for brevity
        # See full implementation in the original file
        pass
    
    def save_state(self) -> Dict:
        """Save evolution state"""
        return {
            'generation': self.generation,
            'population': [g.to_dict() for g in self.population],
            'innovation_counter': self.innovation_counter,
            'node_counter': self.node_counter,
            'species': [[g.id for g in s] for s in self.species]
        }
    
    def load_state(self, state: Dict, input_size: int, output_size: int):
        """Load evolution state"""
        self.generation = state['generation']
        self.innovation_counter = state['innovation_counter']
        self.node_counter = state['node_counter']
        
        # Load population
        self.population = [
            NEATGenome.from_dict(g, input_size, output_size) 
            for g in state['population']
        ]