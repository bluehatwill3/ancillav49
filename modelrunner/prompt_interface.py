import json
# Assuming components are in the same directory as established in our Holosyn framework
from system_modifier import SystemModifier
from training_loop import TrainingLoop

class PromptInterface:
    """
    Acts as the central communication bridge for the Holosyn system.
    """
    def __init__(self, orchestrator):
        self.modifier = SystemModifier()
        self.orchestrator = orchestrator # Passed from your orchestrator.py

    def run_interface(self):
        print("Holosyn Command Interface Ready. Type '[INSTRUCT] help' for options.")
        while True:
            raw_input = input(">> ")
            
            # Component: Parser
            if "[INSTRUCT]" in raw_input:
                self.process_instruction(raw_input)
            elif raw_input.lower() == "exit":
                break
            else:
                print("Unknown command. Use [INSTRUCT] tag.")

    def process_instruction(self, instruction):
        """Component: Routes the instruction to the correct API."""
        cmd = instruction.replace("[INSTRUCT]", "").strip().lower()
        
        if "update config" in cmd:
            # Component: System Modifier API
            key = input("Enter config key: ")
            val = input("Enter new value: ")
            print(self.modifier.update_config(key, val))
            
        elif "train" in cmd:
            # Component: Training Loop Execution
            print("Starting training session...")
            self.orchestrator.run(epochs=1)
            print("Training cycle complete.")
            
        elif "help" in cmd:
            print("Available: 'update config', 'train'")

# Implementation:
# orchestrator = HolosynOrchestrator('challenge_test.json')
# interface = PromptInterface(orchestrator)
# interface.run_interface()