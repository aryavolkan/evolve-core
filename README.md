# Evolve Core

A shared library of core evolutionary algorithms and neural network components for Godot-based AI projects.

## Overview

This repository contains reusable components extracted from the `evolve` and `chess-evolve` projects to promote code reuse and maintainability across AI/ML experiments in Godot.

## Structure

```
evolve-core/
├── ai/
│   ├── neural_network.gd      # Feedforward network (input→hidden→output, tanh, flat weight arrays)
│   ├── recurrent_network.gd   # Elman recurrent extension with memory state
│   ├── network_factory.gd     # Factory with transparent Rust fallback
│   └── neat/                  # NEAT neuroevolution
│       ├── neat_evolution.gd  # Speciation + reproduction loop
│       ├── neat_genome.gd     # Genotype (node + connection genes)
│       ├── neat_network.gd    # Phenotype (topological sort + tanh)
│       ├── neat_species.gd    # Fitness sharing, stagnation tracking
│       ├── neat_innovation.gd # Global innovation counter
│       └── neat_config.gd     # ~70 hyperparameters
├── genetic/
│   ├── evolution_base.gd      # Abstract base class for evolution algorithms
│   ├── simple_evolution.gd    # Single-objective GA
│   ├── nsga2.gd               # Multi-objective Pareto optimization
│   ├── operators.gd           # Tournament/roulette/rank selection, crossover, mutation
│   └── population.gd          # Population management
├── interfaces/
│   ├── agent.gd               # IAgent interface
│   ├── sensor.gd              # ISensor interface
│   └── reward.gd              # IReward interface
├── utils/
│   ├── stats_tracker.gd       # Statistics and metrics tracking
│   └── config_base.gd         # Base configuration class
├── python/evolve_core/        # Python implementations
│   ├── genetic/               # NEAT engine + genome (Python)
│   ├── training/              # W&B worker integration
│   └── utils/                 # FitnessAggregator, NSGA2Selection
├── autoload.gd                # Godot autoload: EvolveCore.create_network(), etc.
├── scripts/                   # lint_gdscript.sh, lint_python.sh
└── tests/                     # Python tests (pytest)
```

## Usage

### As a Git Submodule

```bash
git submodule add https://github.com/aryavolkan/evolve-core.git evolve-core
```

### Autoload Entry Point

Register in `project.godot`:
```ini
[autoload]
EvolveCore="*res://evolve-core/autoload.gd"
```

Then use:
```gdscript
var network = EvolveCore.create_network(input_size, hidden_size, output_size)
var tracker = EvolveCore.create_stats_tracker()
```

### Direct Preload

```gdscript
var NeuralNetwork = preload("res://evolve-core/ai/neural_network.gd")
var NSGA2 = preload("res://evolve-core/genetic/nsga2.gd")
var GeneticOperators = preload("res://evolve-core/genetic/operators.gd")
```

### Python Package

```bash
pip install -e python/
```

```python
from evolve_core import NEATEvolution, NEATGenome, FitnessAggregator, WandBWorker
```

## Lint & Test

```bash
./scripts/lint_gdscript.sh    # GDScript (gdtoolkit)
./scripts/lint_python.sh      # Python (ruff)
pytest tests/ -q              # Python tests
```

## Projects Using This Library

- [evolve](https://github.com/aryavolkan/evolve) — 2D arcade survival game with neuroevolution
- [chess-evolve](https://github.com/aryavolkan/chess-evolve) — Coevolutionary chess neural networks
- [neurogrid](https://github.com/aryavolkan/neurogrid) — 2D grid simulation with Dynamic I/O NEAT
- [tile-empire](https://github.com/aryavolkan/tile-empire) — Hex strategy game with NEAT AI

## License

This project inherits the license from the parent evolve project.