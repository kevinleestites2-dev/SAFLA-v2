"""
SAFLA v2.0 Memory Layer
Hybrid Memory Architecture: Episodic, Semantic, Procedural
Inspired by ruvnet/SAFLA
"""

import json
import time
from pathlib import Path
from collections import deque

class HybridMemory:
    def __init__(self, base_path: Path, max_episodes: int = 1000):
        self.base_path = base_path
        self.max_episodes = max_episodes
        
        # 1. Episodic Memory (Raw events, short-term)
        self.episodic_path = base_path / "episodic.json"
        self.episodes = self._load_json(self.episodic_path, deque(maxlen=max_episodes))
        
        # 2. Semantic Memory (Abstract patterns, regimes, long-term)
        self.semantic_path = base_path / "semantic.json"
        self.concepts = self._load_json(self.semantic_path, {})
        
        # 3. Procedural Memory (Weights, rules, the "how-to")
        self.procedural_path = base_path / "procedural.json"
        self.procedures = self._load_json(self.procedural_path, {"weights": {}, "rules": []})

    def _load_json(self, path, default):
        if path.exists():
            try:
                data = json.loads(path.read_text())
                if isinstance(default, deque):
                    return deque(data, maxlen=self.max_episodes)
                return data
            except:
                pass
        return default

    def save(self):
        self.episodic_path.write_text(json.dumps(list(self.episodes)))
        self.semantic_path.write_text(json.dumps(self.concepts))
        self.procedural_path.write_text(json.dumps(self.procedures))

    def commit_episode(self, event):
        """Store a new raw event."""
        event["ts"] = time.time()
        self.episodes.append(event)
        
    def update_concept(self, key, value):
        """Update a semantic concept (e.g., regime performance)."""
        self.concepts[key] = value

    def update_procedure(self, weights):
        """Update procedural weights."""
        self.procedures["weights"] = weights
        self.procedures["last_update"] = time.time()
