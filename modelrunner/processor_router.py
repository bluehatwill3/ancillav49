import json
import re
from abc import ABC, abstractmethod
from typing import Dict, List, Any

# ==========================================
# 1. Base Strategy Interface
# ==========================================
class BaseProcessor(ABC):
    """
    Abstract base class for all domain-specific processors.
    Enforces a strict contract for data processing.
    """
    @abstractmethod
    def process(self, problem_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Must be implemented by subclasses to process the data.
        """
        pass

    def extract_tokens(self, formula: str) -> List[str]:
        """Utility to break down the annotated_formula."""
        return re.findall(r'[a-zA-Z_0-9.]+|\(|\)|,', formula)

# ==========================================
# 2. Domain-Specific Processors
# ==========================================
class PhysicsProcessor(BaseProcessor):
    def process(self, problem_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handles kinematic and physical mechanics problems[cite: 14]."""
        problem_text = problem_data.get('Problem', '')
        formula = problem_data.get('annotated_formula', '')
        
        # Physics-specific tokenization or tensor logic would go here
        tokens = self.extract_tokens(formula)
        return {
            "domain": "physics",
            "status": "processed",
            "vector_length": len(tokens),
            "signature": f"PHYS-{hash(problem_text)}"
        }

class GeometryProcessor(BaseProcessor):
    def process(self, problem_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handles spatial and geometric calculations[cite: 14]."""
        formula = problem_data.get('annotated_formula', '')
        # Geometry problems often use specific constants like pi or sqrt[cite: 14]
        has_pi = 'const_pi' in formula
        
        return {
            "domain": "geometry",
            "status": "processed",
            "requires_pi_embedding": has_pi,
            "raw_formula": formula
        }

class ProbabilityProcessor(BaseProcessor):
    def process(self, problem_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handles combinatorics and probabilistic outcomes[cite: 14]."""
        formula = problem_data.get('annotated_formula', '')
        # Detect combinations/permutations like 'choose'[cite: 14]
        is_combinatoric = 'choose' in formula
        
        return {
            "domain": "probability",
            "status": "processed",
            "combinatoric_flag": is_combinatoric
        }

class GainProcessor(BaseProcessor):
    def process(self, problem_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handles financial, profit/loss, and percentage calculations[cite: 14]."""
        options = problem_data.get('options', '')
        
        return {
            "domain": "gain",
            "status": "processed",
            "options_scanned": options
        }

class GeneralProcessor(BaseProcessor):
    def process(self, problem_data: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback processor for general logic and algebra[cite: 14]."""
        return {
            "domain": "general",
            "status": "processed",
            "correct_answer": problem_data.get('correct', '')
        }

# ==========================================
# 3. The Omni-Router (Factory)
# ==========================================
class ProcessorRouter:
    """
    Routes incoming dataset entries to the appropriate specialized processor.
    """
    def __init__(self):
        # Map the category strings found in the dataset to their class[cite: 14]
        self._routes: Dict[str, BaseProcessor] = {
            "physics": PhysicsProcessor(),
            "geometry": GeometryProcessor(),
            "probability": ProbabilityProcessor(),
            "gain": GainProcessor(),
            "general": GeneralProcessor(),
            "other": GeneralProcessor() # Routing 'other' to general[cite: 14]
        }
        self.metrics = {k: 0 for k in self._routes.keys()}

    def route_and_execute(self, problem_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determines the category and dispatches the payload[cite: 14].
        """
        category = problem_data.get('category', 'general').lower()
        
        # Fallback to general if category is completely unknown
        if category not in self._routes:
            category = "general"
            
        # Update routing metrics
        self.metrics[category] += 1
        
        # Dispatch to the specific handler
        processor = self._routes[category]
        try:
            return processor.process(problem_data)
        except Exception as e:
            return {"domain": category, "status": "error", "error": str(e)}

# ==========================================
# 4. Main Execution Pipeline
# ==========================================
def run_dataset_pipeline(file_path: str):
    """Loads the dataset and processes all entries through the router."""
    router = ProcessorRouter()
    processed_archive = []
    
    print(f"Loading dataset from: {file_path}")
    try:
        with open(file_path, 'r') as f:
            dataset = json.load(f)
            
        print(f"Loaded {len(dataset)} entries. Routing data...")
        
        for entry in dataset:
            # Process each math problem through the router[cite: 14]
            result = router.route_and_execute(entry)
            processed_archive.append(result)
            
        print("\n--- Routing Metrics ---")
        for domain, count in router.metrics.items():
            print(f"{domain.capitalize().ljust(12)}: {count} processed")
            
        return processed_archive
        
    except FileNotFoundError:
        print(f"Error: Could not find {file_path}. Ensure the file exists.")
    except json.JSONDecodeError:
        print("Error: The file is not valid JSON.")

if __name__ == "__main__":
    # Point this to your actual challenge_test.json file[cite: 14]
    run_dataset_pipeline('challenge_test.json')