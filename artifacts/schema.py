from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import json

class Step(BaseModel):
    step_id: int
    action: str
    selector: Optional[str] = None
    selector_fallbacks: List[str] = []
    value: Optional[str] = None
    checkpoint: Optional[str] = None
    screenshot_path: Optional[str] = None
    reasoning: Optional[str] = None

class Capability(BaseModel):
    capability_id: str
    version: str = "1.0.0"
    description: str
    target_url: str
    created_at: str = datetime.now().isoformat()
    input_schema: Dict[str, str] = {}
    output_schema: Dict[str, str] = {}
    steps: List[Step] = []
    checkpoint: str
    allowed_domains: List[str] = []
    risky_actions: List[str] = []

    def save(self, path: str):
        with open(path, 'w') as f:
            json.dump(self.model_dump(), f, indent=2)
        print(f"✅ Artifact saved to {path}")

    @classmethod
    def load(cls, path: str):
        with open(path, 'r') as f:
            data = json.load(f)
        return cls(**data)