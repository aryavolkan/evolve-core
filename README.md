# Evolve Core

A shared library of core evolutionary algorithms and neural network components for Godot-based AI projects.

## Overview

This repository contains reusable components extracted from the `evolve` and `chess-evolve` projects to promote code reuse and maintainability across AI/ML experiments in Godot.

## Structure

```
evolve-core/
├── ai/                    # Neural network implementations
│   ├── neural_network.gd  # Core feedforward neural network
│   ├── recurrent_network.gd # Recurrent neural networks (Elman, etc.)
│   └── network_factory.gd # Factory for creating networks
├── genetic/              # Evolutionary algorithm components
│   ├── evolution_base.gd # Base class for evolution algorithms
│   ├── operators.gd      # Genetic operators (mutation, crossover, selection)
│   ├── population.gd     # Population management
│   └── fitness.gd        # Fitness evaluation interfaces
├── interfaces/           # Common interfaces and contracts
│   ├── agent.gd         # Agent interface for AI controllers
│   ├── sensor.gd        # Sensor interface for observations
│   └── reward.gd        # Reward/fitness calculation interfaces
├── utils/               # Utility functions
│   ├── stats_tracker.gd # Statistics and metrics tracking
│   └── serialization.gd # Save/load functionality
└── docs/               # Documentation

```

## Usage

### In your project's `project.godot`:

```ini
[autoload]
EvolveCore="*res://addons/evolve-core/autoload.gd"
```

### Example: Creating a Neural Network

```gdscript
var NeuralNetwork = preload("res://addons/evolve-core/ai/neural_network.gd")

func create_network():
    var net = NeuralNetwork.new(
        input_size = 64,
        hidden_size = 32,
        output_size = 8
    )
    return net
```

### Example: Using Evolution

```gdscript
var Evolution = preload("res://addons/evolve-core/genetic/evolution.gd")

func setup_evolution():
    var evo = Evolution.new(
        population_size = 100,
        mutation_rate = 0.1
    )
    return evo
```

## Projects Using This Library

- [evolve](https://github.com/user/evolve) - A real-time evolution sandbox
- [chess-evolve](https://github.com/user/chess-evolve) - Neural network chess AI

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this shared library.

## License

This project inherits the license from the parent evolve project.