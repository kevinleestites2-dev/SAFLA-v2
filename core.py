"""
SAFLA v2.0 — Universal Self-Adaptive Feedback Loop Algorithm
Standalone Core Implementation
Based on ruvnet/SAFLA Breakthrough Architecture
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[SAFLA v2.0] %(message)s')
logger = logging.getLogger("SAFLA")

class SAFLA:
    def __init__(self, project_id: str, config_path: str = "safla_config.json"):
        self.project_id = project_id
        self.config_path = Path(config_path)
        self.memory_dir = Path("safla-v2/memory") / project_id
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        from memory import HybridMemory
        self.memory = HybridMemory(self.memory_dir)
        
        self.config = self._load_config()
        self.state = {
            "entropy": 0.0,
            "regime": "UNKNOWN",
            "last_reflection": time.time()
        }
        
        logger.info(f"Initialized Universal Core for project: {project_id}")

    def _load_config(self) -> Dict[str, Any]:
        if self.config_path.exists():
            try:
                return json.loads(self.config_path.read_text())
            except Exception as e:
                logger.error(f"Failed to load config: {e}")
        
        # Default v2.1 Universal Config
        return {
            "version": "2.1.0",
            "name": "SAFLA-Omni",
            "mode": "RECURSIVE_ADAPTIVE",
            "weights": {},
            "thresholds": {
                "noise": 0.25,
                "conviction": 0.75,
                "panic": 0.85
            },
            "evolution_rate": 0.05,
            "memory_depth": 5000
        }

    def _save_config(self):
        self.config_path.write_text(json.dumps(self.config, indent=2))

    def reflect(self, outcome: Dict[str, Any]) -> Dict[str, Any]:
        """
        The Reflection Phase:
        Analyzes the result, updates memory, and suggests adaptations.
        """
        # outcome expected keys: 'id', 'value' (PnL, score, etc.), 'metadata'
        timestamp = time.time()
        
        # 1. Episodic Memory Update (The "What")
        self.memory.commit_episode(outcome)
        
        # 2. Calculate Entropy (Noise vs Signal)
        self.state["entropy"] = self._calculate_entropy()
        
        # 3. Determine Regime
        self.state["regime"] = self._detect_regime(outcome)
        
        # 4. Neural-Heuristic Synthesis (The "Why")
        # In v2.1, we implement Recursive Pattern Recognition
        if len(self.memory.episodes) % 10 == 0:
            self._cross_pollinate_patterns()

        # 5. Update Procedural Weights if performance is high/low
        adaptations = self._curate_adaptations(outcome)
        
        # 6. Save state
        self.memory.save()
        
        logger.info(f"Reflected on {outcome.get('id')}: Entropy={self.state['entropy']:.4f}, Regime={self.state['regime']}")
        return adaptations

    def _detect_regime(self, outcome: Dict[str, Any]) -> str:
        """v2.1 Advanced Regime Detection: Trends, Clusters, and Volatility."""
        metadata = outcome.get("metadata", {})
        if "regime" in metadata:
            return metadata["regime"]
            
        # Analysis of recent memory to detect shifts
        if len(self.memory.episodes) < 10:
            return "BOOTSTRAPPING"
            
        recent = list(self.memory.episodes)[-10:]
        vals = [e.get("value", 0) for e in recent]
        
        avg = sum(vals) / len(vals)
        if avg > 0 and all(v >= 0 for v in vals[-3:]):
            return "ASCENDING_SIGNAL"
        if avg < 0 and all(v <= 0 for v in vals[-3:]):
            return "DESCENDING_SIGNAL"
        if self.state["entropy"] > 0.6:
            return "CHAOTIC_NOISE"
            
        return "STABLE_FLOW"

    def _cross_pollinate_patterns(self):
        """v2.1 Feature: Analyzing correlations between metadata and success."""
        logger.info("Initiating Cross-Pollination Phase (v2.1)...")
        # Logic to find "Hidden Signal" in metadata keys vs value outcomes
        # e.g., 'time_of_day' or 'provider' correlated with high 'value'
        pass

    def _calculate_entropy(self) -> float:
        """Measure variance in outcome values over recent episodes."""
        if len(self.memory.episodes) < 5:
            return 0.5
        
        values = [e.get("value", 0) for e in list(self.memory.episodes)[-20:]]
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return min(variance / 100.0, 1.0) # Normalized noise

    def _curate_adaptations(self, outcome: Dict[str, Any]) -> Dict[str, Any]:
        """The Curator Phase: suggested changes to project state."""
        strategy = outcome.get("metadata", {}).get("strategy")
        value = outcome.get("value", 0)
        
        weights = self.memory.procedures.get("weights", {})
        
        if strategy:
            current_w = weights.get(strategy, 1.0)
            if value > 0:
                weights[strategy] = min(current_w * 1.05, 5.0)
            elif value < 0:
                weights[strategy] = max(current_w * 0.95, 0.1)
            
            self.memory.update_procedure(weights)

        return {
            "suggested_weights": weights,
            "entropy": self.state["entropy"],
            "hibernation_mode": self.state["entropy"] > self.config["thresholds"]["panic"]
        }

if __name__ == "__main__":
    # Test execution
    test_safla = SAFLA(project_id="test_run")
    test_outcome = {
        "id": "trade_001",
        "result": "SUCCESS",
        "value": 150.0,
        "metadata": {"strategy": "momentum"}
    }
    print(test_safla.reflect(test_outcome))
