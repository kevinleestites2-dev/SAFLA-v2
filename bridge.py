"""
SAFLA v2.0 Bridge
Standardized integration layer for all Pantheon projects.
"""

import sys
import json
import os
from pathlib import Path

# Add the safla-v2 directory to path if not already there
safla_dir = str(Path(__file__).parent.absolute())
if safla_dir not in sys.path:
    sys.path.append(safla_dir)

try:
    from core import SAFLA
    HAS_CORE = True
except ImportError:
    HAS_CORE = False

class SAFLABridge:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.edge_cache_path = Path(f".safla_edge_{project_name}.json")
        self.local_weights = self._load_edge_cache()
        
        # The bridge connects to the central core if available
        if HAS_CORE:
            try:
                self.engine = SAFLA(project_id=project_name)
                # Sync central weights to edge cache on init
                self.local_weights = self.engine.config.get("weights", self.local_weights)
                self._save_edge_cache()
            except Exception as e:
                print(f"[EDGE] Hub unreachable, running in Sovereign Mode: {e}")
                self.engine = None
        else:
            print(f"[EDGE] Core missing, running in Autonomous mode.")
            self.engine = None

    def _load_edge_cache(self):
        if self.edge_cache_path.exists():
            try:
                with open(self.edge_cache_path, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_edge_cache(self):
        with open(self.edge_cache_path, "w") as f:
            json.dump(self.local_weights, f)

    def report_event(self, event_id: str, outcome_value: float, metadata: dict = None):
        """
        Report an event (trade, scrape, task) to the SAFLA core.
        If Hub is down, executes local edge reflection.
        """
        outcome = {
            "id": event_id,
            "value": outcome_value,
            "metadata": metadata or {}
        }
        
        if self.engine:
            result = self.engine.reflect(outcome)
            # Update edge cache with the latest global evolution
            self.local_weights = self.engine.config.get("weights", self.local_weights)
            self._save_edge_cache()
            return result
        else:
            # Sovereign Mode: Minimal local feedback loop
            print(f"[EDGE] Sovereign Reflection for {event_id}")
            # Simple weight adjustment logic could go here if Hub is dead
            return {"status": "sovereign", "weights": self.local_weights}

    def get_weights(self):
        """Returns current optimized weights (Local Edge Cache)."""
        return self.local_weights

# Quick usage example:
# from safla_bridge import SAFLABridge
# safla = SAFLABridge("SobekPrime")
# safla.report_event("trade_1", 100.0, {"type": "arb"})
