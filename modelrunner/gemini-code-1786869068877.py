import math
import time
import numpy as np
from typing import Dict, List, Tuple
from collections import deque

import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import pipeline

# =====================================================================
# 1. MODULAR EVENT BUS & TELEMETRY
# =====================================================================

class EventBus:
    """Asynchronous pub/sub router for modular edge systems."""
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type: str, callback):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event_type: str, payload: dict):
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                callback(payload)

class EnvironmentalTelemetry:
    def __init__(self, temp_c: float, rh_pct: float, moist_pct: float, lux: float):
        self.temp_c = temp_c
        self.rh_pct = rh_pct
        self.soil_moist_pct = moist_pct
        self.lux = lux
        self.timestamp = time.time()

# =====================================================================
# 2. TEMPORAL CONTEXT VALIDATOR
# =====================================================================

class TemporalContextValidator:
    """Validates anomalies through time rather than instantaneous spikes."""
    def __init__(self, window_size: int = 5, variance_threshold: float = 1.5):
        self.window_size = window_size
        self.variance_threshold = variance_threshold
        # Deque for fast O(1) appends and pops
        self.history = deque(maxlen=window_size) 

    def add_and_validate(self, vpd_kpa: float) -> bool:
        """Returns True if the temporal context indicates a sustained anomaly."""
        self.history.append(vpd_kpa)
        if len(self.history) < self.window_size:
            return False
        
        mean_vpd = np.mean(self.history)
        std_vpd = np.std(self.history)
        
        # Resolve anomaly only if sustained over time
        if mean_vpd > 2.0 and std_vpd < self.variance_threshold:
            return True
        return False

# =====================================================================
# 3. OPEN-SOURCE REASONING DISTILLER
# =====================================================================

class OpenSourceSwarmReasoner:
    """
    Offline NLP reasoning engine utilizing local open-source models.
    Operates strictly on logical deduction, stripping away external knowledge.
    """
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.event_bus.subscribe("SUSTAINED_ANOMALY", self.resolve_and_teach)
        
        print("[INIT] Loading Local Open-Source Reasoning Engine (Offline Mode)...")
        # Utilizing a highly distilled model for rapid edge inference
        # device_map="auto" handles placement on available GPUs (e.g., in a Supermicro chassis)
        self.reasoner = pipeline(
            "text-generation", 
            model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", 
            device_map="cpu", # Change to "auto" if CUDA is configured
            torch_dtype=torch.float32
        )

    def resolve_and_teach(self, payload: dict):
        state = payload["state"]
        print(f"\n[REASONING ENGINE] Analyzing sustained anomaly. Mean VPD: {state['vpd_kpa']:.2f} kPa")
        
        # Pure logic prompt, devoid of factual trivia retrieval
        prompt = (
            f"<|system|>\nYou are a purely logical routing kernel. Given sensor data, output ONLY the integer ID of the best action: "
            f"0=IRRIGATION, 1=MISTING, 2=EXHAUST, 3=ROVER. Do not explain.</s>\n"
            f"<|user|>\nSensors: Temp={state['temp']}C, RH={state['rh']}%, VPD={state['vpd_kpa']}kPa. High VPD indicates extreme dryness in the air. Action?</s>\n"
            f"<|assistant|>\n"
        )
        
        # Generate resolution
        output = self.reasoner(prompt, max_new_tokens=2, temperature=0.1)
        response_text = output[0]['generated_text'].split("<|assistant|>\n")[-1].strip()
        
        # Parse the logical resolution
        try:
            resolved_action = int(response_text[0])
            if resolved_action not in [0, 1, 2, 3]: resolved_action = 1
        except ValueError:
            resolved_action = 1 # Fallback to misting for high VPD
            
        print(f"[REASONING ENGINE] Logical resolution complete. Suggested Actuator ID: {resolved_action}")
        
        # Publish pseudo-target to trigger online learning in the SNN
        self.event_bus.publish("ONLINE_LEARNING_TRIGGER", {"target_action": resolved_action})


# =====================================================================
# 4. ADAPTIVE SPIKING LAM & ONLINE LEARNING
# =====================================================================

class SurrogateSpike(torch.autograd.Function):
    @staticmethod
    def forward(ctx, membrane, threshold):
        ctx.save_for_backward(membrane, threshold)
        return (membrane >= threshold).float()

    @staticmethod
    def backward(ctx, grad_output):
        membrane, threshold = ctx.saved_tensors
        grad_input = grad_output / (5.0 * torch.abs(membrane - threshold) + 1.0) ** 2
        return grad_input, None

class AdaptiveSpikingDecisionHead(nn.Module):
    def __init__(self, input_dim: int = 4, action_dim: int = 4, steps: int = 6):
        super().__init__()
        self.steps = steps
        self.action_dim = action_dim
        self.fc = nn.Linear(input_dim, action_dim)
        
        # BOOSTED INITIALIZATION: Ensures initial variance pushes membranes past threshold
        nn.init.xavier_uniform_(self.fc.weight, gain=5.0) 
        
        self.decay = nn.Parameter(torch.tensor(0.9))
        self.base_threshold = nn.Parameter(torch.tensor(0.1)) # Lowered threshold
        
        # Online Optimizer
        self.optimizer = torch.optim.AdamW(self.parameters(), lr=0.01)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size = x.size(0)
        current = self.fc(x)
        membrane = torch.zeros(batch_size, self.action_dim, device=x.device)
        spike_record = []

        for _ in range(self.steps):
            membrane = membrane * self.decay + current
            # Dynamic thresholding
            dynamic_thresh = self.base_threshold + 0.05 * membrane.mean()
            spikes = SurrogateSpike.apply(membrane, dynamic_thresh)
            membrane = membrane - spikes * dynamic_thresh
            spike_record.append(spikes)

        return torch.stack(spike_record, dim=0).mean(dim=0)

    def online_learn(self, last_input: torch.Tensor, target_idx: int):
        """Executes a localized gradient step based on open-source reasoning resolution."""
        self.train()
        self.optimizer.zero_grad()
        
        action_potentials = self(last_input)
        
        # Create one-hot target
        target_tensor = torch.zeros_like(action_potentials)
        target_tensor[0, target_idx] = 1.0
        
        loss = F.mse_loss(action_potentials, target_tensor)
        loss.backward()
        self.optimizer.step()
        
        print(f"[SNN KERNEL] Online learning step applied. Loss: {loss.item():.4f}")


# =====================================================================
# 5. MASTER KERNEL
# =====================================================================

class BotanicalModularKernel:
    def __init__(self):
        self.device = torch.device("cpu")
        self.event_bus = EventBus()
        
        # Modular Subsystems
        self.temporal_validator = TemporalContextValidator(window_size=3)
        self.reasoner = OpenSourceSwarmReasoner(self.event_bus)
        self.snn = AdaptiveSpikingDecisionHead().to(self.device)
        
        # State tracking
        self.last_input_tensor = None
        self.event_bus.subscribe("ONLINE_LEARNING_TRIGGER", self._handle_learning)
        
        self.action_map = {
            0: "ACTIVATE_IRRIGATION_VALVES",
            1: "ENGAGE_VPD_MISTING_SYSTEM",
            2: "VENTILATION_HEAT_EXHAUST",
            3: "DISPATCH_HARVESTING_ROVER"
        }

    def _handle_learning(self, payload: dict):
        if self.last_input_tensor is not None:
            self.snn.online_learn(self.last_input_tensor, payload["target_action"])

    def process_telemetry(self, t: EnvironmentalTelemetry) -> dict:
        vp_sat = 0.61078 * math.exp((17.27 * t.temp_c) / (t.temp_c + 237.3))
        vpd_kpa = max(0.0, vp_sat - (vp_sat * (t.rh_pct / 100.0)))
        
        return {"temp": t.temp_c, "rh": t.rh_pct, "soil": t.soil_moist_pct, "vpd_kpa": vpd_kpa}

    def execute_cycle(self, raw_telemetry: EnvironmentalTelemetry):
        metrics = self.process_telemetry(raw_telemetry)
        
        # 1. Vectorize State
        self.last_input_tensor = torch.tensor([[
            metrics["temp"] / 50.0,
            metrics["rh"] / 100.0,
            metrics["soil"] / 100.0,
            metrics["vpd_kpa"] / 5.0
        ]], dtype=torch.float32, device=self.device)

        # 2. Temporal Context Validation
        is_sustained_anomaly = self.temporal_validator.add_and_validate(metrics["vpd_kpa"])
        if is_sustained_anomaly:
            self.event_bus.publish("SUSTAINED_ANOMALY", {"state": metrics})

        # 3. Spiking Inference (Continually resolving & learning)
        self.snn.eval()
        with torch.no_grad():
            action_potentials = self.snn(self.last_input_tensor)
            
        selected_idx = int(torch.argmax(action_potentials, dim=1).item())
        command = self.action_map.get(selected_idx, "IDLE")

        return command, action_potentials.cpu().numpy()[0]
    
    def save_edge_artifact(self):
        filename = "holosyn_v38_final_2_2.pt"
        torch.save(self.snn.state_dict(), filename)
        print(f"[SYSTEM] State exported successfully to {filename}[cite: 16]")

# =====================================================================
# RUNTIME SIMULATION
# =====================================================================

if __name__ == "__main__":
    kernel = BotanicalModularKernel()

    # Simulating a persistent high-heat, low-humidity drought scenario
    stream = [
        EnvironmentalTelemetry(temp_c=34.5, rh_pct=30.0, moist_pct=22.0, lux=45000.0), # Cycle 1
        EnvironmentalTelemetry(temp_c=35.2, rh_pct=28.0, moist_pct=20.5, lux=52000.0), # Cycle 2
        EnvironmentalTelemetry(temp_c=36.0, rh_pct=25.0, moist_pct=18.0, lux=55000.0), # Cycle 3 (Triggers Anomaly)
        EnvironmentalTelemetry(temp_c=36.1, rh_pct=25.0, moist_pct=18.0, lux=55000.0)  # Cycle 4 (SNN has learned)
    ]

    print("\n[EXEC] Initiating Offline Edge Intelligence Pipeline...\n")
    for step_num, frame in enumerate(stream, start=1):
        print(f"--- Cycle {step_num} ---")
        cmd, spikes = kernel.execute_cycle(frame)
        print(f"Dispatched Actuator : {cmd}")
        print(f"Action Spike Rates  : {np.round(spikes, 4)}\n")
        
    kernel.save_edge_artifact()