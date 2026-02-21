"""
Fitness utilities for multi-objective optimization
"""




class FitnessAggregator:
    """Aggregate multi-objective fitness values"""

    @staticmethod
    def weighted_sum(objectives: dict[str, float], weights: dict[str, float]) -> float:
        """Simple weighted sum aggregation"""
        total = 0.0
        total_weight = 0.0

        for obj_name, obj_value in objectives.items():
            if obj_name in weights:
                total += obj_value * weights[obj_name]
                total_weight += weights[obj_name]

        return total / total_weight if total_weight > 0 else 0.0

    @staticmethod
    def normalize_and_weight(objectives: dict[str, float], weights: dict[str, float],
                           ranges: dict[str, tuple[float, float]] | None = None) -> float:
        """Normalize objectives to [0,1] before weighting"""
        normalized = {}

        for obj_name, obj_value in objectives.items():
            if ranges and obj_name in ranges:
                min_val, max_val = ranges[obj_name]
                if max_val > min_val:
                    normalized[obj_name] = (obj_value - min_val) / (max_val - min_val)
                else:
                    normalized[obj_name] = 1.0
            else:
                # Assume [0, 1] if no range specified
                normalized[obj_name] = max(0.0, min(1.0, obj_value))

        return FitnessAggregator.weighted_sum(normalized, weights)


class NSGA2Selection:
    """NSGA-II multi-objective selection"""

    @staticmethod
    def non_dominated_sort(population: list[dict]) -> list[list[int]]:
        """
        Perform non-dominated sorting on population
        Returns list of fronts (each front is a list of indices)
        """
        n = len(population)

        # Initialize domination data structures
        domination_count = [0] * n  # Number of solutions dominating each solution
        dominated_solutions = [[] for _ in range(n)]  # Solutions dominated by each solution
        fronts = [[]]  # First front

        # Compare all pairs
        for i in range(n):
            for j in range(i + 1, n):
                dom_result = NSGA2Selection._dominates(population[i], population[j])

                if dom_result == 1:  # i dominates j
                    dominated_solutions[i].append(j)
                    domination_count[j] += 1
                elif dom_result == -1:  # j dominates i
                    dominated_solutions[j].append(i)
                    domination_count[i] += 1

        # Find first front
        for i in range(n):
            if domination_count[i] == 0:
                fronts[0].append(i)

        # Find remaining fronts
        current_front = 0
        while current_front < len(fronts) and fronts[current_front]:
            next_front = []

            for i in fronts[current_front]:
                for j in dominated_solutions[i]:
                    domination_count[j] -= 1
                    if domination_count[j] == 0:
                        next_front.append(j)

            if next_front:
                fronts.append(next_front)
            current_front += 1

        return fronts[:-1]  # Remove empty last front

    @staticmethod
    def _dominates(solution1: dict, solution2: dict) -> int:
        """
        Check if solution1 dominates solution2
        Returns: 1 if solution1 dominates, -1 if solution2 dominates, 0 if neither

        Assumes 'fitness' field contains list of objectives to maximize
        """
        obj1 = solution1.get('fitness', [])
        obj2 = solution2.get('fitness', [])

        if not obj1 or not obj2 or len(obj1) != len(obj2):
            return 0

        better_in_any = False
        worse_in_any = False

        for i in range(len(obj1)):
            if obj1[i] > obj2[i]:
                better_in_any = True
            elif obj1[i] < obj2[i]:
                worse_in_any = True

        if better_in_any and not worse_in_any:
            return 1
        elif worse_in_any and not better_in_any:
            return -1
        else:
            return 0

    @staticmethod
    def crowding_distance(front: list[dict], objectives_count: int) -> list[float]:
        """Calculate crowding distance for solutions in a front"""
        n = len(front)
        if n <= 2:
            return [float('inf')] * n

        distances = [0.0] * n

        for obj_idx in range(objectives_count):
            # Sort by this objective
            sorted_indices = sorted(range(n),
                                  key=lambda i: front[i]['fitness'][obj_idx])

            # Boundary solutions get infinite distance
            distances[sorted_indices[0]] = float('inf')
            distances[sorted_indices[-1]] = float('inf')

            # Calculate range
            obj_values = [front[i]['fitness'][obj_idx] for i in sorted_indices]
            obj_range = obj_values[-1] - obj_values[0]

            if obj_range > 0:
                # Calculate distance for intermediate solutions
                for i in range(1, n - 1):
                    idx = sorted_indices[i]
                    distances[idx] += (obj_values[i + 1] - obj_values[i - 1]) / obj_range

        return distances

    @staticmethod
    def select(population: list[dict], target_size: int) -> list[dict]:
        """Backward-compatible alias for select_population."""
        return NSGA2Selection.select_population(population, target_size)

    @staticmethod
    def select_population(population: list[dict], target_size: int) -> list[dict]:
        """
        Select target_size individuals using NSGA-II selection
        Assumes each individual has 'fitness' field with list of objectives
        """
        if len(population) <= target_size:
            return population

        # Non-dominated sorting
        fronts = NSGA2Selection.non_dominated_sort(population)

        selected = []
        front_idx = 0

        # Add complete fronts that fit
        while front_idx < len(fronts) and len(selected) + len(fronts[front_idx]) <= target_size:
            selected.extend([population[i] for i in fronts[front_idx]])
            front_idx += 1

        # Handle partial front using crowding distance
        if len(selected) < target_size and front_idx < len(fronts):
            remaining_needed = target_size - len(selected)
            current_front = [population[i] for i in fronts[front_idx]]

            # Calculate crowding distances
            objectives_count = len(current_front[0]['fitness'])
            distances = NSGA2Selection.crowding_distance(current_front, objectives_count)

            # Sort by crowding distance and select most spread out
            sorted_indices = sorted(range(len(current_front)),
                                  key=lambda i: distances[i],
                                  reverse=True)

            for i in range(remaining_needed):
                selected.append(current_front[sorted_indices[i]])

        return selected
