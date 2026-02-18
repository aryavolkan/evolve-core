# Migration Guide

This guide helps you migrate from project-specific implementations to the shared evolve-core library.

## Quick Start

1. Add evolve-core to your project (as a git submodule or copy):
   ```bash
   cd your-project
   git submodule add https://github.com/your-org/evolve-core.git addons/evolve-core
   ```

2. Update your `project.godot` to include the autoload:
   ```ini
   [autoload]
   EvolveCore="*res://addons/evolve-core/autoload.gd"
   ```

## Migration Examples

### Neural Networks

**Before (evolve):**
```gdscript
var NeuralNetwork = preload("res://ai/neural_network.gd")
var net = NeuralNetwork.new(64, 32, 8)
```

**After:**
```gdscript
var net = EvolveCore.create_network(64, 32, 8)
# or directly:
var NeuralNetwork = preload("res://addons/evolve-core/ai/neural_network.gd")
```

### Evolution

**Before (chess-evolve):**
```gdscript
extends RefCounted
# ... custom evolution implementation
```

**After:**
```gdscript
extends "res://addons/evolve-core/genetic/evolution_base.gd"
# ... only implement specific methods
```

### Genetic Operators

**Before:**
```gdscript
func _tournament_select(pop, fitness, k):
    # custom implementation
```

**After:**
```gdscript
const Operators = preload("res://addons/evolve-core/genetic/operators.gd")
var parent = Operators.tournament_select(population, fitness_scores, 3)
```

## Project-Specific Migrations

### Evolve Project

1. **Neural Network Changes:**
   - Base neural network → `evolve-core/ai/neural_network.gd`
   - Recurrent features → `evolve-core/ai/recurrent_network.gd`
   - Keep NEAT implementation project-specific (too specialized)

2. **Evolution Changes:**
   - Extract common evolution logic to use `EvolutionBase`
   - Keep NSGA-II and other specialized algorithms in project
   - Use `GeneticOperators` for selection/crossover/mutation

3. **Import Updates:**
   ```gdscript
   # Old
   preload("res://ai/neural_network.gd")
   # New
   preload("res://addons/evolve-core/ai/neural_network.gd")
   ```

### Chess-Evolve Project

1. **Simplify Evolution:**
   ```gdscript
   # Extend from base instead of RefCounted
   extends "res://addons/evolve-core/genetic/evolution_base.gd"
   
   # Remove duplicate methods like tournament_select
   # Use GeneticOperators instead
   ```

2. **Network Factory:**
   ```gdscript
   # Use factory for potential Rust acceleration
   var net = NetworkFactory.create(389, 64, 128, false)
   ```

## Best Practices

1. **Don't modify evolve-core directly** - extend or compose instead
2. **Keep project-specific logic in your project** - only share truly common code
3. **Use interfaces** - implement IAgent, ISensor, IReward for consistency
4. **Configuration** - extend ConfigBase for your project's config needs

## Compatibility Notes

- All APIs maintained where possible
- Memory/recurrent features are opt-in
- Rust acceleration handled transparently by NetworkFactory
- Statistics tracking improved but backward compatible