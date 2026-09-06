"""
=========================================================================================
AUTONOMOUS PRODUCTION SUITE: SELF-DRIVING SWARM & PLANT REPAIR DISPATCHER
=========================================================================================
Architecture:
  1. Telemetry Lexicon & Natural Syntax Parser
  2. Plant Diagnostics & Yield Health Engine
  3. Ground Rover Self-Driving Unit (Spiking Transformer Core)
  4. Autonomous Drone Inspection & Field Repair Unit
  5. Central Swarm Mission Dispatcher & Execution Loop
=========================================================================================
"""

import os
import time
import math
import random
import logging
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

import torch
import torch.nn as nn
import torch.nn.functional as F

# =======================================================================================
# 1. LOGGING & SYSTEM CONFIGURATION
# =======================================================================================

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)-8s | %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger("FarmSwarmOS")


class ActionType(Enum):
    STEER_LEFT = 0
    STEER_RIGHT = 1
    ACCELERATE = 2
    EMERGENCY_BRAKE = 3
    APPLY_FERTILIZER = 4
    IRRIGATE_SPOT = 5
    DISPATCH_REPAIR_DRONE = 6


@dataclass
class SwarmConfig:
    vocab_size: int = 4000
    max_seq_len: int = 48
    embed_dim: int = 256
    num_heads: int = 4
    num_layers: int = 2
    
    # Spiking Dynamics
    spike_threshold: float = 0.85
    leak_rate: float = 0.20
    
    # Fleet Scale
    num_rovers: int = 2
    num_drones: int = 2
    
    device: str = "cuda" if torch.cuda.is_available() else "cpu"

CONFIG = SwarmConfig()


# =======================================================================================
# 2. SENSORY & TELEMETRY ENCODING LEXICON
# =======================================================================================

class TelemetryLexicon:
    """Encodes natural machine and plant telemetry into discrete token tensors."""
    def __init__(self, vocab_size: int):
        self.vocab_size = vocab_size
        self.w2i = {"<PAD>": 0, "<BOS>": 1, "<EOS>": 2, "<UNK>": 3}
        self.i2w = {0: "<PAD>", 1: "<BOS>", 2: "<EOS>", 3: "<UNK>"}
        self.counter = 4

    def encode(self, text: str, max_len: int) -> torch.Tensor:
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


# =======================================================================================
# 3. PLANT DIAGNOSTIC & REQUIREMENT ENGINE
# =======================================================================================

@dataclass
class PlantTelemetry:
    row_id: int
    plant_index: int
    ndvi: float               # -1.0 to 1.0 (Vigor index)
    soil_moisture_pct: float  # 0% to 100%
    nitrogen_ppm: float       # Available Nitrogen
    foliar_temp_c: float      # Leaf temperature in Celsius
    nozzle_pressure_bar: float # Hardware sensor from last pass


class AgronomicDiagnosticEngine:
    """
    Evaluates bio-telemetry to calculate exact plant requirements and machine health.
    """
    @staticmethod
    def assess_plant_needs(data: PlantTelemetry) -> Tuple[str, Dict[str, Any]]:
        needs = {}
        diagnostic_flags = []
        
        # 1. Water Deficit Detection
        if data.soil_moisture_pct < 18.0 or data.foliar_temp_c > 32.0:
            needs["irrigation_volume_liters"] = round((25.0 - data.soil_moisture_pct) * 0.4, 2)
            diagnostic_flags.append("DROUGHT_STRESS")
            
        # 2. Nutrient Deficiency Detection
        if data.ndvi < 0.45 or data.nitrogen_ppm < 30.0:
            needs["nitrogen_boost_grams"] = round((45.0 - data.nitrogen_ppm) * 0.15, 2)
            diagnostic_flags.append("NITROGEN_DEFICIT")
            
        # 3. Hardware / Nozzle Failure Detection (Clogging alert)
        if data.nozzle_pressure_bar > 4.2 or data.nozzle_pressure_bar < 0.8:
            needs["hardware_fault"] = "NOZZLE_CLOGGED"
            diagnostic_flags.append("MAINTENANCE_REQUIRED")
            
        status_tag = "_".join(diagnostic_flags) if diagnostic_flags else "OPTIMAL"
        telemetry_str = (
            f"<PLANT> ROW {data.row_id} IDX {data.plant_index} NDVI {data.ndvi:.2f} "
            f"MOIST {data.soil_moisture_pct:.1f}% N_PPM {data.nitrogen_ppm:.1f} "
            f"STATUS {status_tag}"
        )
        return telemetry_str, needs


# =======================================================================================
# 4. NEURAL DRIVING & REASONING CORE (Spiking LAM)
# =======================================================================================

class SpikingDrivingLAM(nn.Module):
    """
    Spiking Neural Network transformer for autonomous vehicle navigation.
    """
    def __init__(self, config: SwarmConfig):
        super().__init__()
        self.config = config
        self.embedding = nn.Embedding(config.vocab_size, config.embed_dim)
        self.pos_encoder = nn.Parameter(torch.zeros(1, config.max_seq_len, config.embed_dim))
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=config.embed_dim, 
            nhead=config.num_heads, 
            batch_first=True, 
            dropout=0.0
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=config.num_layers)
        self.action_head = nn.Linear(config.embed_dim, len(ActionType))
        
        self.register_buffer('threshold', torch.tensor(config.spike_threshold))
        self.register_buffer('leak_rate', torch.tensor(config.leak_rate))

    def forward(self, tokens: torch.Tensor, membrane: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        x = self.embedding(tokens) + self.pos_encoder[:, :tokens.size(1), :]
        latent_context = self.transformer(x).mean(dim=1)
        
        logits = self.action_head(latent_context)
        current = torch.softmax(logits, dim=-1)
        
        # Leaky Integrate-and-Fire (LIF) Equations
        membrane = (membrane * (1.0 - self.leak_rate)) + current
        spikes = (membrane >= self.threshold).float()
        membrane = membrane * (1.0 - spikes)
        
        return spikes, membrane, latent_context


# =======================================================================================
# 5. ROBOTIC FLEET ENTITIES
# =======================================================================================

class SpikingGroundRover:
    """Autonomous field tractor/rover navigating rows and treating crops."""
    def __init__(self, rover_id: str, brain: SpikingDrivingLAM):
        self.rover_id = rover_id
        self.brain = brain
        self.membrane = torch.zeros(1, len(ActionType)).to(CONFIG.device)
        self.current_position = (0.0, 0.0) # (x_meters, y_meters)
        self.speed_kmh = 0.0
        self.spray_tank_liters = 500.0

    def step_navigation(self, telemetry_tokens: torch.Tensor) -> Tuple[ActionType, bool]:
        with torch.no_grad():
            spikes, self.membrane, _ = self.brain(telemetry_tokens, self.membrane)
            
        has_spiked = (spikes.sum() > 0).item()
        if has_spiked:
            action_idx = int(spikes.argmax().item())
            action = ActionType(action_idx)
            self._execute_physical_actuation(action)
            return action, True
        return ActionType.ACCELERATE, False

    def _execute_physical_actuation(self, action: ActionType):
        if action == ActionType.STEER_LEFT:
            self.current_position = (self.current_position[0] - 0.2, self.current_position[1] + 0.5)
        elif action == ActionType.STEER_RIGHT:
            self.current_position = (self.current_position[0] + 0.2, self.current_position[1] + 0.5)
        elif action == ActionType.ACCELERATE:
            self.speed_kmh = min(15.0, self.speed_kmh + 1.0)
            self.current_position = (self.current_position[0], self.current_position[1] + 0.8)
        elif action == ActionType.EMERGENCY_BRAKE:
            self.speed_kmh = 0.0
        elif action == ActionType.APPLY_FERTILIZER:
            self.spray_tank_liters = max(0.0, self.spray_tank_liters - 2.5)


class AutonomousRepairDrone:
    """Aerial drone handling surveillance and automated field repair procedures."""
    def __init__(self, drone_id: str):
        self.drone_id = drone_id
        self.altitude_m = 0.0
        self.battery_pct = 100.0
        self.current_task: Optional[str] = None

    def deploy_repair_mission(self, target_row: int, repair_type: str):
        self.altitude_m = 12.0
        self.battery_pct -= 3.5
        self.current_task = f"EXECUTING {repair_type} AT ROW {target_row}"
        logger.info(f"🚁 [{self.drone_id}] Airborne -> {self.current_task} (Altitude: {self.altitude_m}m)")
        
        # Simulate autonomous field repair action
        if repair_type == "NOZZLE_CLOGGED":
            logger.info(f"🔧 [{self.drone_id}] High-pressure air purge dispatched to Rover spray bar.")
        elif repair_type == "REPLACE_PROBE":
            logger.info(f"📍 [{self.drone_id}] Deployed replacement soil telemetry pod.")


# =======================================================================================
# 6. CENTRAL SWARM MISSION DISPATCHER
# =======================================================================================

class SwarmMissionControl:
    """
    Central Coordinator connecting plant needs to autonomous rovers and repair drones.
    """
    def __init__(self, rovers: List[SpikingGroundRover], drones: List[AutonomousRepairDrone], lexicon: TelemetryLexicon):
        self.rovers = rovers
        self.drones = drones
        self.lexicon = lexicon
        self.mission_queue: List[Dict[str, Any]] = []

    def process_field_tick(self, sample_data: PlantTelemetry, obs_distance_m: float, lane_drift_m: float):
        # 1. Diagnose Plant & Hardware State
        telemetry_str, requirements = AgronomicDiagnosticEngine.assess_plant_needs(sample_data)
        logger.info(f"🌱 Perception: {telemetry_str}")
        
        # 2. Add Navigation Sensory Grammar
        driving_grammar = f"<LIDAR> OBS_DIST {obs_distance_m:.1f}M <LANE> DRIFT {lane_drift_m:.2f}M {telemetry_str}"
        tokens = self.lexicon.encode(driving_grammar, CONFIG.max_seq_len).unsqueeze(0).to(CONFIG.device)
        
        # 3. Ground Fleet Navigation
        for rover in self.rovers:
            action, spiked = rover.step_navigation(tokens)
            if spiked:
                logger.info(f"🚜 [{rover.rover_id}] Spiked Action: {action.name} | Pos: {rover.current_position} | Tank: {rover.spray_tank_liters:.1f}L")
            else:
                logger.info(f"🚜 [{rover.rover_id}] Integrating Navigation Substrate... Voltage: {rover.membrane.max().item():.3f}V")

        # 4. Dispatch Drone Repairs if Required
        if "hardware_fault" in requirements:
            idle_drone = self.drones[0]
            idle_drone.deploy_repair_mission(sample_data.row_id, requirements["hardware_fault"])


# =======================================================================================
# 7. EXECUTION PIPELINE
# =======================================================================================

def main():
    logger.info("=" * 80)
    logger.info("🌾 INITIALIZING AUTONOMOUS BROADACRE SWARM ARCHITECTURE")
    logger.info("=" * 80)

    lexicon = TelemetryLexicon(CONFIG.vocab_size)
    driving_brain = SpikingDrivingLAM(CONFIG).to(CONFIG.device)
    driving_brain.eval()

    # Instantiate Fleet
    rovers = [SpikingGroundRover(f"Rover_Alpha_{i+1}", driving_brain) for i in range(CONFIG.num_rovers)]
    drones = [AutonomousRepairDrone(f"Drone_Sentry_{i+1}") for i in range(CONFIG.num_drones)]
    
    mission_control = SwarmMissionControl(rovers, drones, lexicon)

    # Simulate 5 Operational Field Ticks with Dynamic Stresses
    simulated_scenarios = [
        PlantTelemetry(row_id=1, plant_index=10, ndvi=0.78, soil_moisture_pct=24.0, nitrogen_ppm=55.0, foliar_temp_c=22.0, nozzle_pressure_bar=2.8),
        PlantTelemetry(row_id=1, plant_index=11, ndvi=0.76, soil_moisture_pct=23.5, nitrogen_ppm=52.0, foliar_temp_c=23.0, nozzle_pressure_bar=2.8),
        PlantTelemetry(row_id=1, plant_index=12, ndvi=0.38, soil_moisture_pct=14.0, nitrogen_ppm=22.0, foliar_temp_c=34.5, nozzle_pressure_bar=2.8),
        PlantTelemetry(row_id=2, plant_index=1,  ndvi=0.65, soil_moisture_pct=20.0, nitrogen_ppm=40.0, foliar_temp_c=25.0, nozzle_pressure_bar=4.9),
        PlantTelemetry(row_id=2, plant_index=2,  ndvi=0.72, soil_moisture_pct=21.0, nitrogen_ppm=48.0, foliar_temp_c=24.0, nozzle_pressure_bar=2.8)
    ]

    for tick, plant_data in enumerate(simulated_scenarios, 1):
        logger.info(f"\n--- 🕒 FIELD CYCLE TICK {tick:02d} ---")
        obs_dist = random.uniform(1.5, 9.0)
        lane_drift = random.uniform(-0.8, 0.8)
        mission_control.process_field_tick(plant_data, obs_dist, lane_drift)
        time.sleep(0.4)

    logger.info("\n✅ Field Operations Complete. Fleet standing by in station.")

if __name__ == "__main__":
    main()