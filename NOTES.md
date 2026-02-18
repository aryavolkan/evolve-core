# Evolve Core - Refactoring Notes

## Overview

This document tracks the refactoring process of extracting shared components from the `evolve` and `chess-evolve` projects into a reusable library.

## Key Design Decisions

### 1. Neural Network Architecture

**Decision**: Created a base `neural_network.gd` without recurrent features, and a separate `recurrent_network.gd` that extends it.

**Rationale**:
- Chess-evolve doesn't need recurrent networks (Markovian game state)
- Evolve benefits from temporal memory for survival gameplay
- Separation keeps the base implementation simple and fast

### 2. Network Factory Pattern

**Decision**: Implemented `NetworkFactory` for transparent Rust acceleration support.

**Rationale**:
- Both projects use optional Rust neural networks for performance
- Factory pattern hides implementation details from users
- Automatic fallback to GDScript maintains compatibility

### 3. Evolution Base Class

**Decision**: Created abstract `EvolutionBase` with virtual methods for population initialization and evolution.

**Rationale**:
- Common patterns: fitness tracking, statistics, save/load
- Projects differ in selection strategies (single vs multi-objective)
- Base class provides structure without forcing implementation

### 4. Genetic Operators Module

**Decision**: Separated genetic operators into a static utility class.

**Rationale**:
- Operators (selection, crossover, mutation) are project-agnostic
- Static methods allow easy mixing and matching
- Reduces code duplication across evolution implementations

### 5. Interface Definitions

**Decision**: Created lightweight interfaces for agents, sensors, and rewards.

**Rationale**:
- Defines clear contracts without forcing inheritance
- GDScript doesn't have true interfaces, but these serve as documentation
- Helps ensure compatibility when swapping components

## Migration Strategy

### Phase 1: Core Extraction (Current)
- ✅ Extract neural network implementations
- ✅ Extract evolution base classes
- ✅ Extract genetic operators
- ✅ Define interfaces
- ✅ Extract statistics tracking

### Phase 2: Project Updates (Next)
- Update evolve to use evolve-core
- Update chess-evolve to use evolve-core
- Remove duplicated code
- Update imports and references

### Phase 3: Testing & Validation
- Run existing test suites
- Verify performance characteristics
- Check Rust acceleration still works
- Benchmark before/after

## Compatibility Considerations

1. **Import Paths**: Projects will need to update from `res://ai/neural_network.gd` to `res://addons/evolve-core/ai/neural_network.gd`

2. **API Changes**: Kept APIs identical where possible to minimize migration effort

3. **Optional Features**: Used composition over configuration where projects need different features (e.g., recurrent networks)

## Outstanding Questions

1. **Rust Integration**: The Rust acceleration code is project-specific. Should we create a standardized Rust interface in evolve-core?

2. **NEAT Implementation**: The evolve project has extensive NEAT code. This is quite specialized - should it be in core or remain project-specific?

3. **Multi-objective Evolution**: NSGA-II is used in evolve but not chess-evolve. Include in core as optional module?

## Performance Notes

- The geometric skip mutation is a clever optimization that should be preserved
- Network cloning avoids intermediate allocations - important for large populations
- Factory pattern adds negligible overhead vs direct instantiation

## Future Enhancements

1. **More Network Architectures**: LSTM, GRU, Transformer layers
2. **Additional Evolution Algorithms**: CMA-ES, Differential Evolution
3. **Distributed Training**: Multi-process population evaluation
4. **Checkpointing**: Automatic population backups during long runs