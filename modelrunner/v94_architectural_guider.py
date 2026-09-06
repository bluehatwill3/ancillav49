#!/usr/bin/env python3
"""
HOLOSYN V94: AUTONOMOUS ARCHITECTURAL GUIDER (OPENCLAW PROXY)
====================================================================
Hardware Target: 16GB RAM | i5 8-Core (Local Inference Optimized)
Dependencies: `sudo apt-get install xdotool` (for peripheral I/O)
Execution: Run via `sudo` for full root subsystem control.
"""

import os
import sys
import json
import time
import shlex
import urllib.request
import subprocess
import numpy as np
from typing import List, Dict, Any

# ──────────────────────────────────────────────────────────────────────
# 1. LOCAL OPEN-SOURCE INFERENCE ENGINE (OLLAMA / LLAMA.CPP)
# ──────────────────────────────────────────────────────────────────────
class LocalInferenceClient:
    """
    Connects to a locally hosted open-source LLM (e.g., Ollama).
    Optimized for 7B-8B parameter models running on 16GB RAM.
    """
    def __init__(self, endpoint="http://localhost:11434/api/generate", model="llama3"):
        self.endpoint = endpoint
        self.model = model

    def generate(self, system_prompt: str, history: List[Dict[str, str]]) -> str:
        # Flatten history for raw completion (or use /api/chat for chat models)
        prompt = f"{system_prompt}\n\n"
        for msg in history:
            prompt += f"[{msg['role'].upper()}]: {msg['content']}\n"
        prompt += "[ASSISTANT]:\n"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json", # Enforces structured output
            "options": {
                "temperature": 0.1, # Low temp for strict architectural coding
                "num_ctx": 4096     # Optimized context window for 16GB RAM
            }
        }

        try:
            req = urllib.request.Request(self.endpoint, data=json.dumps(payload).encode('utf-8'),
                                         headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=120) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get("response", "{}")
        except Exception as e:
            return json.dumps({"action": "error", "thought": f"Inference failure: {e}"})

# ──────────────────────────────────────────────────────────────────────
# 2. SYSTEM ABSTRACTION TOOLS (I/O, OS, NETWORK)
# ──────────────────────────────────────────────────────────────────────
class BaseTool:
    name: str
    description: str
    def execute(self, **kwargs) -> str: pass

class SubsystemExecutorTool(BaseTool):
    name = "execute_bash"
    description = "Executes a root-level bash command. Requires 'command' arg."
    
    def execute(self, command: str) -> str:
        print(f"   [⚙️ ROOT EXEC] {command}")
        try:
            res = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30.0)
            output = res.stdout if res.returncode == 0 else res.stderr
            return f"EXIT CODE: {res.returncode}\nOUTPUT:\n{output[:1000]}"
        except subprocess.TimeoutExpired:
            return "ERROR: Command execution timed out."
        except Exception as e:
            return f"CRITICAL FAULT: {str(e)}"

class PeripheralAutomatorTool(BaseTool):
    name = "control_hardware"
    description = "Controls mouse/keyboard. Args: 'action' (type/mousemove/click), 'target' (string or 'X Y')."
    
    def execute(self, action: str, target: str) -> str:
        print(f"   [⌨️ PERIPHERAL] {action.upper()} -> {target}")
        try:
            if action == "type":
                safe_text = target.replace("'", "'\\''")
                cmd = f"xdotool type '{safe_text}'"
            elif action == "mousemove":
                cmd = f"xdotool mousemove {target}"
            elif action == "click":
                cmd = f"xdotool click {target}"
            else:
                return "ERROR: Invalid peripheral action."
            
            subprocess.run(cmd, shell=True, check=True)
            return f"Hardware sequence '{action}' executed successfully."
        except Exception as e:
            return f"Hardware emulation failed: {e}. Ensure xdotool is installed."

class FileOperationsTool(BaseTool):
    name = "file_io"
    description = "Reads or writes files. Args: 'mode' (read/write), 'path', 'content' (if writing)."
    
    def execute(self, mode: str, path: str, content: str = "") -> str:
        print(f"   [📁 FILE I/O] {mode.upper()} -> {path}")
        try:
            if mode == "read":
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()[:2000] # Cap return to prevent context overflow
            elif mode == "write":
                os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return f"Successfully wrote {len(content)} bytes to {path}."
        except Exception as e:
            return f"File I/O Error: {e}"

class InternetScraperTool(BaseTool):
    name = "fetch_url"
    description = "Fetches raw text data from the internet. Requires 'url' arg."
    
    def execute(self, url: str) -> str:
        print(f"   [🌐 NETWORK] Fetching -> {url}")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8', errors='ignore')
                return html[:2000] # Return truncated payload for token efficiency
        except Exception as e:
            return f"Network Error: {e}"

class ArchitectureValidatorTool(BaseTool):
    name = "validate_holosyn"
    description = "Analyzes hybrid neural-quantum tensors. Requires 'snn_array' (list of floats)."
    
    def execute(self, snn_array: List[float]) -> str:
        print(f"   [🧬 VALIDATION] Analyzing manifold tensor...")
        arr = np.array(snn_array)
        variance = float(np.var(arr))
        mean = float(np.mean(arr))
        if variance > 0.5:
            return f"WARNING: High entropic variance ({variance:.2f}). System unstable."
        return f"SUCCESS: Tensor stable. Mean: {mean:.2f}, Var: {variance:.2f}."

# ──────────────────────────────────────────────────────────────────────
# 3. AUTONOMOUS RE-ACT AGENT
# ──────────────────────────────────────────────────────────────────────
class ArchitecturalGuider:
    """
    Main orchestration loop. Evaluates user goals, prompts the local LLM,
    parses JSON actions, and bridges them to the operating system.
    """
    def __init__(self, model_name="llama3"):
        self.client = LocalInferenceClient(model=model_name)
        self.memory = []
        self.max_steps = 15
        self.tools = {
            "execute_bash": SubsystemExecutorTool(),
            "control_hardware": PeripheralAutomatorTool(),
            "file_io": FileOperationsTool(),
            "fetch_url": InternetScraperTool(),
            "validate_holosyn": ArchitectureValidatorTool()
        }
        self.system_prompt = self._build_prompt()

    def _build_prompt(self) -> str:
        tool_desc = "\n".join([f"- {k}: {v.description}" for k, v in self.tools.items()])
        return f"""You are Holosyn Guider, an autonomous OS-level AI agent running on an i5 8-Core Linux machine.
You have FULL ROOT ACCESS to the system, internet, files, keyboard, and mouse.

AVAILABLE TOOLS:
{tool_desc}
- final_answer: Use this when the task is fully complete. Args: 'message'.

RULES:
1. You operate in a loop: Reason -> Act -> Observe.
2. Output ONLY a valid JSON object. No markdown formatting.
3. If an action fails, analyze the error and try a different approach.

JSON SCHEMA:
{{
  "thought": "Your internal reasoning for the current step.",
  "action": "tool_name",
  "args": {{"arg_name": "arg_value"}}
}}"""

    def run_task(self, objective: str):
        print(f"\n🎯 [OBJECTIVE ACTIVATED]: {objective}")
        self.memory.append({"role": "user", "content": objective})
        
        for step in range(1, self.max_steps + 1):
            print(f"\n⏳ [ITERATION {step}/{self.max_steps}] Reasoning...")
            
            # 1. Thought Generation
            raw_response = self.client.generate(self.system_prompt, self.memory)
            self.memory.append({"role": "assistant", "content": raw_response})
            
            # 2. Parse Action
            try:
                data = json.loads(raw_response)
                thought = data.get("thought", "No thought provided.")
                action = data.get("action", "")
                args = data.get("args", {})
            except json.JSONDecodeError:
                print("   ❌ [PARSING FAULT] Model failed to return valid JSON.")
                self.memory.append({"role": "system", "content": "ERROR: Return strictly valid JSON."})
                continue

            print(f"   🧠 [THOUGHT] {thought}")
            
            # 3. Execution & Observation
            if action == "final_answer":
                print(f"\n✅ [TASK COMPLETE]\n{args.get('message', '')}\n")
                print("═" * 75)
                break
                
            if action in self.tools:
                tool = self.tools[action]
                observation = tool.execute(**args)
                print(f"   👀 [OBSERVATION] {observation[:150].replace(chr(10), ' ')}...")
                self.memory.append({"role": "system", "content": f"OBSERVATION: {observation}"})
            else:
                err = f"Tool '{action}' not recognized."
                print(f"   ❌ [FAULT] {err}")
                self.memory.append({"role": "system", "content": f"ERROR: {err}"})

        if step == self.max_steps:
            print("\n⚠️ [HALT] Maximum iteration limit reached to prevent infinite looping.")

# ──────────────────────────────────────────────────────────────────────
# 4. INTERACTIVE CLI
# ──────────────────────────────────────────────────────────────────────
def launch_guider():
    print("═" * 75)
    print(" 🪐 HOLOSYN V94: OPENCLAW ARCHITECTURAL GUIDER")
    print(" ⚠️ WARNING: SYSTEM RUNS WITH ROOT PRIVILEGES & HARDWARE I/O")
    print("═" * 75)
    
    agent = ArchitecturalGuider(model_name="llama3") # Change model name if using Qwen or Mistral
    
    while True:
        try:
            cmd = input("\n[AWAITING OBJECTIVE] > ").strip()
            if cmd.lower() in ["exit", "quit", "shutdown"]:
                break
            if cmd:
                agent.run_task(cmd)
        except (KeyboardInterrupt, EOFError):
            print("\n👋 System disconnected.")
            break

if __name__ == "__main__":
    launch_guider()