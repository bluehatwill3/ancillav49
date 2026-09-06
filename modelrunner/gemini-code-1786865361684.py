"""
=========================================================================================
UNIVERSAL SWARM OS: TEXT-BASED HARDWARE ABSTRACTION & AUTO-PRODUCTION
=========================================================================================
Description:
This architecture abstracts all vehicle sensors (John Deere & Generic) into a unified 
text grammar. The Spiking LAM processes this text to manage driving, plant care, 
and automatic repair drone dispatching.

Dependencies: torch, numpy
=========================================================================================
"""

import time
import random
import logging
import torch
import torch.nn as nn
from typing import Dict, List, Tuple, Any

# =======================================================================================
# 1. SYSTEM CONFIGURATION & LOGGING
# =======================================================================================

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)-8s | %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger("UniversalSwarm")

class Config:
    vocab_size: int = 4000
    max_seq_len: int = 64
    embed_dim: int = 256
    num_actions: int = 6
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    brain_path: str = "spiking_driving_lam.pt"

# =======================================================================================
# 2. UNIVERSAL TEXT LEXICON (ENCODER / DECODER)
# =======================================================================================

class UniversalLexicon:
    """
    Translates raw machine bytes into AI-readable text, and AI text into machine bytes.
    """
    def __init__(self, vocab_size: int):
        self.vocab_size = vocab_size
        self.w2i = {"<PAD>": 0, "<BOS>": 1, "<EOS>": 2, "<UNK>": 3}
        self.i2w = {0: "<PAD>", 1: "<BOS>", 2: "<EOS>", 3: "<UNK>"}
        self.counter = 4
        
        # Hardware Command Dictionary
        self.action_dictionary = {
            0: "<CMD> STEER_LEFT",
            1: "<CMD> STEER_RIGHT",
            2: "<CMD> ACCELERATE",
            3: "<CMD> EMERGENCY_BRAKE",
            4: "<CMD> DEPLOY_NUTRIENTS",
            5: "<CMD> DISPATCH_REPAIR_DRONE"
        }

    def encode_text_to_tensor(self, text: str, max_len: int) -> torch.Tensor:
        """Converts sensor text strings into neural tensors."""
        tokens = [self.w2i["<BOS>"]]
        for word in text.upper().split():
            if word not in self.w2i and self.counter < self.vocab_size:
                self.w2i[word] = self.counter
                self.i2w[self.counter] = word
                self.counter += 1
            tokens.append(self.w2i.get(word, self.w2i["<UNK>"]))
        tokens.append(self.w2i["<EOS>"])
        
        while len(tokens) < max_len:
            tokens.append(self.w2i["<PAD>"])
        return torch.tensor(tokens[:max_len], dtype=torch.long)

    def decode_spike_to_text(self, spike_index: int) -> str:
        """Translates the AI's numerical spike back into a standardized text command."""
        return self.action_dictionary.get(spike_index, "<CMD> IDLE")

# =======================================================================================
# 3. HARDWARE ABSTRACTION LAYER (HAL)
# =======================================================================================

class AbstractVehicle:
    """Base class for all swarm vehicles."""
    def __init__(self, vehicle_id: str):
        self.vehicle_id = vehicle_id
        self.health = 100.0
        self.is_active = True

    def read_sensors_as_text(self) -> str:
        raise NotImplementedError

    def execute_text_command(self, command_text: str):
        raise NotImplementedError


class JohnDeereEquipment(AbstractVehicle):
    """
    Interface for proprietary John Deere machinery using simulated J1939 CAN bus PGNs.
    """
    def read_sensors_as_text(self) -> str:
        # Simulating reading proprietary CAN bus data
        engine_rpm = random.randint(1200, 2200)
        gps_accuracy = random.uniform(0.01, 0.05)
        return f"<JD_CAN> PGN_F004_RPM {engine_rpm} PGN_F003_GPS {gps_accuracy:.2f}M <STATUS> NOMINAL"

    def execute_text_command(self, command_text: str):
        # Translating universal text back into John Deere CAN frames
        if "STEER_LEFT" in command_text:
            logger.info(f"   🚜 [{self.vehicle_id}] Translating to JD ISOBUS: 0x18FEF100 (Steer L)")
        elif "ACCELERATE" in command_text:
            logger.info(f"   🚜 [{self.vehicle_id}] Translating to JD ISOBUS: 0x0CF00400 (Throttle +)")


class GenericRover(AbstractVehicle):
    """
    Interface for custom, open-source edge rovers using standard PWM/Serial.
    """
    def read_sensors_as_text(self) -> str:
        # Simulating reading generic serial sensors
        battery_v = random.uniform(22.0, 24.5)
        obstacle_dist = random.uniform(1.0, 10.0)
        return f"<GENERIC_SERIAL> BATT {battery_v:.1f}V SONAR_DIST {obstacle_dist:.1f}M <STATUS> NOMINAL"

    def execute_text_command(self, command_text: str):
        # Translating universal text to simple serial byte commands
        if "STEER_LEFT" in command_text:
            logger.info(f"   🚙 [{self.vehicle_id}] Serial Write: b'\\x01\\x50' (PWM Servo L)")
        elif "DEPLOY_NUTRIENTS" in command_text:
            logger.info(f"   🚙 [{self.vehicle_id}] Serial Write: b'\\x04\\xFF' (Pump Relay ON)")


class RepairDrone(AbstractVehicle):
    """
    Autonomous aerial unit for micromanaging field repairs and rapid scouting.
    """
    def read_sensors_as_text(self) -> str:
        altitude = random.uniform(10.0, 15.0)
        return f"<DRONE_MAVLINK> ALT {altitude:.1f}M <STATUS> STANDBY"

    def execute_text_command(self, command_text: str):
        if "DISPATCH_REPAIR" in command_text:
            logger.info(f"   🚁 [{self.vehicle_id}] MAVLink Mission Uploaded. Taking off for field repair.")

# =======================================================================================
# 4. EDGE INTELLIGENCE CORE
# =======================================================================================

class EdgeIntelligenceCore:
    """
    Loads the compiled spiking model and handles the Text-In / Text-Out pipeline.
    """
    def __init__(self, lexicon: UniversalLexicon):
        self.lexicon = lexicon
        self.membrane = torch.zeros(1, Config.num_actions).to(Config.device)
        self.brain = None
        self._load_brain()

    def _load_brain(self):
        try:
            # Loading the exact file referenced
            self.brain = torch.jit.load(Config.brain_path)
            self.brain.eval()
            logger.info(f"Successfully loaded compiled core: {Config.brain_path}")
        except Exception as e:
            logger.warning(f"Could not load {Config.brain_path}. Using pass-through fallback for simulation. ({e})")

    def process_telemetry(self, sensor_text: str) -> str:
        """Feeds text to the brain and returns the textual command."""
        tokens = self.lexicon.encode_text_to_tensor(sensor_text, Config.max_seq_len).unsqueeze(0).to(Config.device)
        
        # If the model loaded successfully, run inference
        if self.brain:
            with torch.no_grad():
                spikes, self.membrane, _ = self.brain(tokens, self.membrane)
            
            if spikes.sum() > 0:
                action_idx = int(spikes.argmax().item())
                return self.lexicon.decode_spike_to_text(action_idx)
            else:
                return "<CMD> ACCUMULATING_POTENTIAL"
                
        # Fallback simulation if model file isn't physically present in this directory
        mock_action = random.choice([0, 1, 2, 4])
        return self.lexicon.decode_spike_to_text(mock_action)

# =======================================================================================
# 5. AUTOMATIC PRODUCTION & MICROMANAGEMENT SYSTEM
# =======================================================================================

class ProductionManager:
    """
    Oversees the entire farm. Tracks plant requirements and orchestrates the 
    fleet of John Deere tractors, generic rovers, and repair drones.
    """
    def __init__(self):
        self.lexicon = UniversalLexicon(Config.vocab_size)
        self.ai_core = EdgeIntelligenceCore(self.lexicon)
        
        # Registering a mixed fleet
        self.fleet: List[AbstractVehicle] = [
            JohnDeereEquipment("JD_Tractor_01"),
            GenericRover("Rover_Edge_01"),
            RepairDrone("Drone_Mech_01")
        ]

    def monitor_plants(self) -> str:
        """Simulates an overarching vision system scanning the crop rows."""
        health = random.uniform(0.4, 1.0)
        if health < 0.5:
            return "<CROP_HEALTH> CRITICAL_DEFICIENCY_DETECTED"
        return "<CROP_HEALTH> OPTIMAL"

    def run_production_loop(self, ticks: int = 5):
        logger.info("Starting Automatic Production & Micromanagement Loop...")
        
        for tick in range(1, ticks + 1):
            logger.info(f"\n--- 🌐 GLOBAL TICK {tick:02d} ---")
            
            # 1. Check Global Plant Health
            crop_status = self.monitor_plants()
            
            # 2. Process each vehicle in the swarm
            for vehicle in self.fleet:
                # Abstract sensors to text
                sensor_text = vehicle.read_sensors_as_text()
                
                # Combine vehicle sensors with global plant status
                combined_telemetry = f"{sensor_text} {crop_status}"
                logger.info(f"📥 IN  [{vehicle.vehicle_id}]: {combined_telemetry}")
                
                # AI processes text and outputs a text command
                command_text = self.ai_core.process_telemetry(combined_telemetry)
                logger.info(f"📤 OUT [{vehicle.vehicle_id}]: {command_text}")
                
                # Hardware layer translates text back to machine actuation
                vehicle.execute_text_command(command_text)
                
            time.sleep(1.0)

# =======================================================================================
# 6. EXECUTION SCRIPT
# =======================================================================================

if __name__ == "__main__":
    farm_os = ProductionManager()
    farm_os.run_production_loop(ticks=4)