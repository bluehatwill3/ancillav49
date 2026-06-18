#!/usr/bin/env python3
"""
HOLOSYN AGENTIC SWARM OBSERVER
================================================================
Role: Meta-Agent Orchestrator
Capabilities:
- Dynamically routes subconscious models (TinyLlama, Qwen, OPT) based on data modality.
- Modulates learning gain and pulse entropy based on system coherence.
- Acts as a governor to prevent hardware Out-Of-Memory (OOM) crashes.
"""

import sys
import os
import gc
import torch
import numpy as np

# Dynamic Compatibility Bridge
try:
    from __main__ import BaseObserver
except ImportError:
    class BaseObserver:
        def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs): return 0.5

class AgenticSwarmObserver(BaseObserver):
    def __init__(self):
        super().__init__()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.history = []
        self.current_agent = "facebook/opt-125m" # Default lightweight agent
        
        # Agentic Thresholds
        self.crisis_threshold = 0.3  # Coherence level that triggers a model switch
        self.boredom_threshold = 0.9 # High coherence triggers chaotic pulse injection
        
        print("🧠 [AGENTIC SWARM] Meta-Observer initialized. Standing by to govern subconscious routing.")

    def _trigger_model_switch(self, target_model, kwargs):
        """
        Attempts to safely command the main Holosyn loop to switch models,
        managing memory clearing to prevent OOM errors.
        """
        if self.current_agent == target_model:
            return # Already active

        print(f"\n🧠 [AGENTIC COMMAND] Modality shift detected. Flushing VRAM and routing to: {target_model}")
        
        # Force garbage collection to clear old model weights from memory
        torch.cuda.empty_cache() if self.device == "cuda" else None
        gc.collect()

        # Inject the routing command into kwargs so the main engine can intercept it
        # (Assuming your main loop or Subconscious Generator checks for this)
        kwargs['agent_switch_request'] = target_model
        self.current_agent = target_model

    def _modulate_system_parameters(self, s, p, haptic_level, kwargs):
        """
        Agentic control over learning rate (gain) and pulse entropy.
        """
        # If the system is highly coherent (bored), inject chaos (entropy)
        if s > self.boredom_threshold:
            kwargs['entropy_injection'] = 0.15
            kwargs['gain_multiplier'] = 1.2
            
        # If the system is chaotic (crisis), stabilize pulses and slow learning
        elif s < self.crisis_threshold:
            kwargs['entropy_injection'] = -0.10
            kwargs['gain_multiplier'] = 0.5
            
        # Default stability
        else:
            kwargs['entropy_injection'] = 0.0
            kwargs['gain_multiplier'] = 1.0

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        """
        The Agent observes the current state and decides if the system needs 
        to restructure its neural topology or swap its generative model.
        """
        self.history.append(s)
        if len(self.history) > 10:
            self.history.pop(0)

        # 1. Modality-Based Agent Routing
        is_multimodal = kwargs.get('is_multimodal', False)
        modality_type = kwargs.get('mod', 'TEXT')

        if is_multimodal or modality_type in ["IMAGE_NODE", "VIDEO_NODE"]:
            # Route to Qwen2-VL for visual processing
            self._trigger_model_switch("Qwen/Qwen2-VL-2B-Instruct", kwargs)
            
        elif modality_type == "AUDIO_NODE":
            # Audio requires fast phonetic reasoning; route to TinyLlama
            self._trigger_model_switch("TinyLlama/TinyLlama-1.1B-Chat-v1.0", kwargs)
            
        elif np.mean(self.history) < self.crisis_threshold:
            # Deep crisis: Fall back to hyper-fast, low-memory OPT model for stability
            self._trigger_model_switch("facebook/opt-125m", kwargs)

        # 2. Parameter Modulation
        self._modulate_system_parameters(s, p, haptic_level, kwargs)

        # 3. Output the Agent's confidence vector
        # The agent calculates its own resonance based on how well it feels it is managing the system
        agent_confidence = np.clip((s * 0.4) + (sy * 0.4) + (p * 0.2), 0.0, 1.0)
        return float(agent_confidence)