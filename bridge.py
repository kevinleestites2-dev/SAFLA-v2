"""
SAFLA v2.0 Bridge
Standardized integration layer for all Pantheon projects.
"""

import sys
from pathlib import Path

# Add the safla-v2 directory to path if not already there
safla_dir = str(Path(__file__).parent.absolute())
if safla_dir not in sys.path:
    sys.path.append(safla_dir)

try:
    from core import SAFLA
except ImportError:
    from safla_v2.core import SAFLA # Fallback for relative imports

class SAFLABridge:
    def __init__(self, project_name: str):
        self.project_name = project_name
        # The bridge connects the local project to the central core
        self.engine = SAFLA(project_id=project_name)
    
    def report_event(self, event_id: str, outcome_value: float, metadata: dict = None):
        """
        Report an event (trade, scrape, task) to the SAFLA core.
        Returns suggested adaptations.
        """
        outcome = {
            "id": event_id,
            "value": outcome_value,
            "metadata": metadata or {}
        }
        return self.engine.reflect(outcome)

    def get_weights(self):
        """Returns current optimized weights for the project."""
        return self.engine.config.get("weights", {})

# Quick usage example:
# from safla_bridge import SAFLABridge
# safla = SAFLABridge("SobekPrime")
# safla.report_event("trade_1", 100.0, {"type": "arb"})
