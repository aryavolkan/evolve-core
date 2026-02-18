"""
Evolve Core - Shared evolutionary algorithm and neural network components
"""

__version__ = "0.1.0"

# Import main components for easy access
from .genetic.neat_genome import NEATGenome
from .genetic.neat_evolution import NEATEvolution
from .training.wandb_worker import WandBWorker, GodotWorker
from .utils.fitness import FitnessAggregator, NSGA2Selection

__all__ = [
    'NEATGenome',
    'NEATEvolution', 
    'WandBWorker',
    'GodotWorker',
    'FitnessAggregator',
    'NSGA2Selection'
]