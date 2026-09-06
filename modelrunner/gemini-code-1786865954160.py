from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Optional
import time

# --- Domain Models & Enums ---

class SystemState(Enum):
    NORMAL = auto()
    ADVISORY = auto()
    EMERGENCY_STOP = auto()

@dataclass
class TelemetryData:
    sensor_id: str
    timestamp: float
    value: float
    unit: str
    proof_confidence: float  # Validation confidence (0.0 - 1.0)

@dataclass
class ActuatorCommand:
    actuator_id: str
    state: bool
    duration_seconds: float = 0.0

# --- Abstract Base Interfaces ---

class ISensorDriver(ABC):
    @abstractmethod
    def read(self) -> TelemetryData:
        """Fetch normalized telemetry from physical hardware or bus."""
        pass

    @property
    @abstractmethod
    def sensor_id(self) -> str:
        pass


class IActuatorDriver(ABC):
    @abstractmethod
    def execute(self, command: ActuatorCommand) -> bool:
        """Trigger physical actuator."""
        pass

    @abstractmethod
    def emergency_shutdown(self) -> None:
        """Force the actuator to a known safe state immediately."""
        pass


class ISafetyArbiter(ABC):
    @abstractmethod
    def evaluate(self, readings: List[TelemetryData]) -> SystemState:
        """Evaluate readings and enforce advisory or emergency constraints."""
        pass

# --- Concrete Drivers ---

class SoilMoistureDriver(ISensorDriver):
    def __init__(self, sensor_id: str = "soil_moist_01"):
        self._id = sensor_id

    @property
    def sensor_id(self) -> str:
        return self._id

    def read(self) -> TelemetryData:
        # Hardware driver interface point (e.g., ADC, I2C, SPI)
        return TelemetryData(
            sensor_id=self._id,
            timestamp=time.time(),
            value=34.5,
            unit="%",
            proof_confidence=0.92
        )


class ProximitySafetyDriver(ISensorDriver):
    def __init__(self, sensor_id: str = "prox_radar_01", distance_m: float = 3.5):
        self._id = sensor_id
        self.distance_m = distance_m

    @property
    def sensor_id(self) -> str:
        return self._id

    def read(self) -> TelemetryData:
        return TelemetryData(
            sensor_id=self._id,
            timestamp=time.time(),
            value=self.distance_m,
            unit="m",
            proof_confidence=0.88
        )


class IrrigationValveDriver(IActuatorDriver):
    def __init__(self, actuator_id: str = "valve_zone_1"):
        self.actuator_id = actuator_id
        self._is_open = False

    def execute(self, command: ActuatorCommand) -> bool:
        self._is_open = command.state
        print(f"[{self.actuator_id}] Valve state set to: {'OPEN' if self._is_open else 'CLOSED'}")
        return True

    def emergency_shutdown(self) -> None:
        self._is_open = False
        print(f"[{self.actuator_id}] EMERGENCY SHUTDOWN: Valve locked CLOSED.")

# --- Safety Arbiter Implementation ---

class FarmOSSafetyArbiter(ISafetyArbiter):
    def __init__(self, min_confidence: float = 0.60, min_proximity_m: float = 2.0):
        self.min_confidence = min_confidence
        self.min_proximity_m = min_proximity_m

    def evaluate(self, readings: List[TelemetryData]) -> SystemState:
        for data in readings:
            # Check for proximity breach
            if data.unit == "m" and data.value < self.min_proximity_m:
                print(f"🚨 [SAFETY ARBITER] Proximity Breach ({data.value:.2f}m < {self.min_proximity_m}m). Forcing EMERGENCY BRAKE.")
                return SystemState.EMERGENCY_STOP

            # Check proof confidence
            if data.proof_confidence < self.min_confidence:
                print(f"⚠️ [SAFETY ARBITER] Proof validation low ({data.proof_confidence:.3f}). Restricting to ADVISORY.")
                return SystemState.ADVISORY

        return SystemState.NORMAL

# --- Core Botanical Suite Engine ---

class BotanicalGrowSuite:
    def __init__(self, arbiter: ISafetyArbiter):
        self.arbiter = arbiter
        self.sensors: Dict[str, ISensorDriver] = {}
        self.actuators: Dict[str, IActuatorDriver] = {}

    def register_sensor(self, driver: ISensorDriver) -> None:
        self.sensors[driver.sensor_id] = driver

    def register_actuator(self, driver: IActuatorDriver) -> None:
        self.actuators[driver.actuator_id] = driver

    def run_cycle(self, target_moisture: float = 40.0) -> None:
        # 1. Ingest telemetry
        readings = [sensor.read() for sensor in self.sensors.values()]

        # 2. Safety evaluation
        safety_status = self.arbiter.evaluate(readings)

        # 3. Decision & Actuation dispatch
        if safety_status == SystemState.EMERGENCY_STOP:
            for actuator in self.actuators.values():
                actuator.emergency_shutdown()
            return

        if safety_status == SystemState.ADVISORY:
            print("System running in read-only ADVISORY mode. Automated actuation suppressed.")
            return

        # 4. Standard botanical control loop
        for r in readings:
            if r.unit == "%" and r.value < target_moisture:
                for actuator in self.actuators.values():
                    actuator.execute(ActuatorCommand(actuator.actuator_id, state=True, duration_seconds=10.0))


# --- Driver Runtime Example ---

if __name__ == "__main__":
    arbiter = FarmOSSafetyArbiter(min_confidence=0.60, min_proximity_m=2.0)
    suite = BotanicalGrowSuite(arbiter=arbiter)

    suite.register_sensor(SoilMoistureDriver("soil_alpha"))
    suite.register_sensor(ProximitySafetyDriver("radar_front", distance_m=1.2))  # Will trigger emergency brake
    suite.register_actuator(IrrigationValveDriver("valve_zone_1"))

    print("--- Executing Cycle ---")
    suite.run_cycle(target_moisture=45.0)