# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Evolve Core is a shared library of reusable evolutionary algorithms and neural network components for Godot-based AI projects. Used as a git submodule by `evolve`, `chess-evolve`, `neurogrid`, and `tile-empire`.

## Tech Stack

- **Languages**: GDScript (primary), Python 3.8+ (NEAT/fitness/W&B), Rust (optional acceleration)
- **Dependencies**: numpy, wandb, pytest, gdtoolkit, ruff

## Build, Test, Lint

```bash
# Lint
./scripts/lint_gdscript.sh    # gdlint on all .gd files
./scripts/lint_python.sh      # ruff check on python/

# Test
pytest tests/ -q

# Install Python package
pip install -e python/
```

## Architecture

### GDScript components

| Directory | Purpose |
|-----------|---------|
| `ai/` | Neural networks: `neural_network.gd` (feedforward, tanh, flat weight arrays), `recurrent_network.gd` (Elman memory) |
| `ai/neat/` | NEAT: `neat_genome.gd`, `neat_network.gd`, `neat_evolution.gd`, `neat_species.gd`, `neat_innovation.gd`, `neat_config.gd` |
| `genetic/` | Evolution: `evolution_base.gd` (abstract), `simple_evolution.gd` (single-objective GA), `nsga2.gd` (multi-objective), `operators.gd` (tournament/roulette/rank selection, crossover, mutation), `population.gd` |
| `interfaces/` | Contracts: `agent.gd` (IAgent), `sensor.gd` (ISensor), `reward.gd` (IReward) |
| `utils/` | `stats_tracker.gd`, `config_base.gd` |

### Python components (`python/evolve_core/`)

- `genetic/neat_evolution.py`, `neat_genome.py` — Python NEAT implementation
- `training/wandb_worker.py` — W&B experiment tracking integration
- `utils/fitness.py` — `FitnessAggregator`, `NSGA2Selection`

### Entry point

`autoload.gd` — Godot autoload providing `EvolveCore.create_network()`, `EvolveCore.create_stats_tracker()`, `EvolveCore.create_config()`. Uses `NetworkFactory` with transparent Rust fallback.

### Key patterns

- `EvolutionBase` abstract class for all evolution algorithms
- `GeneticOperators` static utility class (selection, crossover, mutation)
- Flat weight arrays in neural networks for efficient mutation
- Factory pattern for Rust/GDScript network creation
- Preload pattern for Godot imports (`res://evolve-core/...`)

## CI

Two workflows (`.github/workflows/`):
- `ci.yml`: gdlint, gdformat, pytest (lenient, continue-on-error)
- `tests.yml`: ruff, gdlint, gdformat, pytest
