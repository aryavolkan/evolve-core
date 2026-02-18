"""
Base W&B training worker for evolve projects
"""

import json
import os
import subprocess
import sys
import time
import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Any

import wandb


class WandBWorker(ABC):
    """Base class for W&B sweep workers"""
    
    def __init__(self, project_name: str, entity: Optional[str] = None):
        self.project_name = project_name
        self.entity = entity
        self.worker_id = str(uuid.uuid4())[:8]
        
        # Enable line buffering for real-time logging
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(line_buffering=True)
            sys.stderr.reconfigure(line_buffering=True)
    
    @abstractmethod
    def get_sweep_config(self) -> Dict:
        """Return the sweep configuration"""
        pass
    
    @abstractmethod
    def evaluate_genome(self, genome: Any, config: wandb.Config) -> Dict[str, float]:
        """Evaluate a single genome and return metrics"""
        pass
    
    @abstractmethod
    def create_evolution_engine(self, config: wandb.Config) -> Any:
        """Create and return the evolution engine"""
        pass
    
    def run_sweep(self, sweep_id: Optional[str] = None):
        """Run a W&B sweep"""
        if sweep_id is None:
            # Create new sweep
            sweep_config = self.get_sweep_config()
            sweep_id = wandb.sweep(sweep_config, project=self.project_name, entity=self.entity)
            print(f"Created sweep: {sweep_id}")
        
        # Run agent
        wandb.agent(sweep_id, function=self.train, project=self.project_name, entity=self.entity)
    
    def train(self):
        """Main training loop for a single sweep run"""
        run = wandb.init()
        config = wandb.config
        
        print(f"Starting training with config: {dict(config)}")
        
        # Create evolution engine
        evolution = self.create_evolution_engine(config)
        
        best_fitness = float('-inf')
        generations_without_improvement = 0
        
        for generation in range(config.get('max_generations', 100)):
            print(f"\n=== Generation {generation} ===")
            
            # Evaluate population
            for i, genome in enumerate(evolution.population):
                metrics = self.evaluate_genome(genome, config)
                
                # Handle multi-objective or single objective
                if isinstance(metrics, dict):
                    # Extract fitness values
                    if 'fitness' in metrics:
                        genome.fitness = metrics['fitness']
                    if 'aggregate_fitness' in metrics:
                        genome.aggregate_fitness = metrics['aggregate_fitness']
                    
                    # Log individual metrics
                    log_data = {
                        f"genome_{i}/{k}": v 
                        for k, v in metrics.items()
                    }
                    wandb.log(log_data)
                else:
                    # Single fitness value
                    genome.fitness = metrics
                    genome.aggregate_fitness = metrics
            
            # Evolve to next generation
            evolution.evolve_generation()
            
            # Calculate and log generation statistics
            fitnesses = [g.aggregate_fitness for g in evolution.population if g.aggregate_fitness is not None]
            if fitnesses:
                current_best = max(fitnesses)
                avg_fitness = sum(fitnesses) / len(fitnesses)
                
                wandb.log({
                    'generation': generation,
                    'best_fitness': current_best,
                    'average_fitness': avg_fitness,
                    'population_size': len(evolution.population),
                    'num_species': len([s for s in evolution.species if s])
                })
                
                # Check for improvement
                if current_best > best_fitness:
                    best_fitness = current_best
                    generations_without_improvement = 0
                    
                    # Save best genome
                    best_genome = max(evolution.population, key=lambda g: g.aggregate_fitness or float('-inf'))
                    self._save_best_genome(best_genome, generation)
                else:
                    generations_without_improvement += 1
                
                print(f"Best: {current_best:.3f}, Avg: {avg_fitness:.3f}, Species: {len(evolution.species)}")
            
            # Early stopping
            if hasattr(config, 'early_stop_generations'):
                if generations_without_improvement >= config.early_stop_generations:
                    print(f"Early stopping: No improvement for {generations_without_improvement} generations")
                    break
        
        # Final summary
        wandb.summary['final_best_fitness'] = best_fitness
        wandb.summary['total_generations'] = generation + 1
        
        run.finish()
    
    def _save_best_genome(self, genome: Any, generation: int):
        """Save the best genome"""
        save_dir = Path("best_genomes")
        save_dir.mkdir(exist_ok=True)
        
        filename = save_dir / f"best_gen{generation}_fit{genome.aggregate_fitness:.3f}.json"
        
        # Convert genome to dict if it has to_dict method
        if hasattr(genome, 'to_dict'):
            data = genome.to_dict()
        else:
            data = genome
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Also log as W&B artifact
        artifact = wandb.Artifact(f"best_genome_gen{generation}", type="genome")
        artifact.add_file(filename)
        wandb.log_artifact(artifact)


class GodotWorker(WandBWorker):
    """Base class for Godot-based training workers"""
    
    def __init__(self, project_name: str, godot_path: str, project_path: str,
                 user_data_dir: str, entity: Optional[str] = None):
        super().__init__(project_name, entity)
        self.godot_path = godot_path
        self.project_path = project_path
        self.user_data_dir = user_data_dir
    
    def run_godot_evaluation(self, genome: Any, config: wandb.Config, 
                           extra_args: List[str] = None) -> Dict[str, float]:
        """Run Godot to evaluate a genome"""
        # Write genome to file
        genome_path = os.path.join(self.user_data_dir, f"genome_{self.worker_id}.json")
        metrics_path = os.path.join(self.user_data_dir, f"metrics_{self.worker_id}.json")
        
        os.makedirs(os.path.dirname(genome_path), exist_ok=True)
        
        # Serialize genome
        if hasattr(genome, 'to_dict'):
            genome_data = genome.to_dict()
        else:
            genome_data = genome
        
        with open(genome_path, 'w') as f:
            json.dump(genome_data, f)
        
        # Clear old metrics
        if os.path.exists(metrics_path):
            os.remove(metrics_path)
        
        # Build command
        cmd = [
            self.godot_path,
            "--path", self.project_path,
            "--headless",
            "--",
            "--training",
            "--genome-path", genome_path,
            "--metrics-path", metrics_path,
            "--worker-id", self.worker_id
        ]
        
        # Add extra arguments
        if extra_args:
            cmd.extend(extra_args)
        
        # Add config parameters as command line args
        for key, value in config.items():
            if key.startswith('_'):  # Skip internal W&B keys
                continue
            cmd_key = "--" + key.replace('_', '-')
            cmd.extend([cmd_key, str(value)])
        
        # Run Godot
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode != 0:
                print(f"Godot error: {result.stderr}")
                return {'fitness': 0.0, 'error': True}
            
            # Read metrics
            if os.path.exists(metrics_path):
                with open(metrics_path, 'r') as f:
                    metrics = json.load(f)
                return metrics
            else:
                print(f"No metrics file created at {metrics_path}")
                return {'fitness': 0.0, 'error': True}
                
        except subprocess.TimeoutExpired:
            print("Godot evaluation timed out")
            return {'fitness': 0.0, 'timeout': True}
        except Exception as e:
            print(f"Error running Godot: {e}")
            return {'fitness': 0.0, 'error': True}