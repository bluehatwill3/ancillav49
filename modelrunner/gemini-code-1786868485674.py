import struct
import numpy as np
import logging
from dataclasses import dataclass
from typing import List, Optional

# Configure logger
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("TelemetryPipeline")


# ---------------------------------------------------------------------------
# 1. Telemetry Data Structures
# ---------------------------------------------------------------------------
@dataclass
class UARTTelemetry:
    temp_c: float
    soil_moist_pct: float


@dataclass
class CANTelemetry:
    voltage_v: float
    current_a: float


# ---------------------------------------------------------------------------
# 2. Hardware Interfaces & Decoders
# ---------------------------------------------------------------------------
class OpenSourceSerialMCU:
    """Simulates a Serial MCU streaming sensor packets over UART."""
    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 115200):
        self.port = port
        self.baudrate = baudrate

    def read_raw_payload(self) -> bytes:
        """Reads raw binary payload from the MCU serial buffer."""
        # Packing 2 floats: temperature (24.5 °C) and soil moisture (48.2 %)
        return struct.pack("<ff", 24.5, 48.2)


class CANInterface:
    """Simulates a CAN bus node streaming telemetry."""
    def __init__(self, channel: str = "can0", bitrate: int = 500000):
        self.channel = channel
        self.bitrate = bitrate

    def read_raw_payload(self) -> bytes:
        """Reads raw binary frame from the CAN interface."""
        # Packing 2 floats: voltage (12.6 V) and current (1.85 A)
        return struct.pack("<ff", 12.6, 1.85)


class UARTDecoder:
    """Decodes raw byte buffers into UARTTelemetry objects."""
    def decode(self, payload: bytes) -> UARTTelemetry:
        temp_c, soil_moist_pct = struct.unpack("<ff", payload)
        return UARTTelemetry(temp_c=temp_c, soil_moist_pct=soil_moist_pct)


class CANDecoder:
    """Decodes raw byte buffers into CANTelemetry objects."""
    def decode(self, payload: bytes) -> CANTelemetry:
        voltage_v, current_a = struct.unpack("<ff", payload)
        return CANTelemetry(voltage_v=voltage_v, current_a=current_a)


# ---------------------------------------------------------------------------
# 3. Integrator & Resonator with Kernel
# ---------------------------------------------------------------------------
class TelemetryIntegrator:
    """
    Discrete cumulative integrator using the Trapezoidal rule.
    Computes: Integral(x(t) dt)
    """
    def __init__(self, dt: float = 0.1):
        self.dt = dt
        self.accumulated_value: float = 0.0
        self.last_sample: Optional[float] = None

    def update(self, sample: float) -> float:
        """Integrates the incoming sample and returns the accumulated total."""
        if self.last_sample is None:
            self.last_sample = sample
            return self.accumulated_value

        # Trapezoidal numerical integration
        self.accumulated_value += 0.5 * (self.last_sample + sample) * self.dt
        self.last_sample = sample
        return self.accumulated_value

    def reset(self):
        self.accumulated_value = 0.0
        self.last_sample = None


class KernelResonator:
    """
    Resonator filter that convolves incoming signals with a damped oscillatory kernel.
    Kernel equation: K(t) = exp(-gamma * t) * cos(omega * t)
    """
    def __init__(self, kernel_size: int = 15, resonant_freq: float = 2.0, damping: float = 0.25, dt: float = 0.1):
        self.kernel_size = kernel_size
        self.dt = dt
        self.buffer: List[float] = [0.0] * kernel_size
        
        # Build the convolution kernel
        t = np.arange(kernel_size) * dt
        raw_kernel = np.exp(-damping * t) * np.cos(2 * np.pi * resonant_freq * t)
        self.kernel = raw_kernel / (np.sum(np.abs(raw_kernel)) + 1e-8)  # Normalized

    def update(self, sample: float) -> float:
        """Appends new telemetry sample and computes the 1D convolution with the resonator kernel."""
        self.buffer.pop(0)
        self.buffer.append(sample)
        
        # Discrete 1D convolution: dot product of buffer and reversed kernel
        filtered_output = float(np.dot(self.buffer, self.kernel[::-1]))
        return filtered_output


# ---------------------------------------------------------------------------
# 4. Execution Pipeline
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Initialize devices and decoders
    uart_mcu = OpenSourceSerialMCU()
    jd_can = CANInterface()
    uart_dec = UARTDecoder()
    jd_dec = CANDecoder()

    # Initialize Signal Processors
    integrator = TelemetryIntegrator(dt=0.5)
    resonator = KernelResonator(kernel_size=10, resonant_freq=1.0, damping=0.1, dt=0.5)

    logger.info("📡 Ingesting Real-Time Hardware Telemetry:")
    
    # Ingest and decode
    uart_telem = uart_dec.decode(uart_mcu.read_raw_payload())
    jd_telem = jd_dec.decode(jd_can.read_raw_payload())

    logger.info(f"   • UART MCU -> Temp: {uart_telem.temp_c:.1f}°C, Soil Moisture: {uart_telem.soil_moist_pct:.1f}%")
    logger.info(f"   • CAN Node -> Voltage: {jd_telem.voltage_v:.1f}V, Current: {jd_telem.current_a:.2f}A")

    # Process temperature signal through integrator and resonator
    simulated_temperatures = [24.0, 24.5, 25.2, 26.0, 25.8, 25.1, 24.3]
    
    logger.info("\n⚙️ Processing Signal through Integrator & Resonator Kernel:")
    for i, temp in enumerate(simulated_temperatures):
        accumulated_temp = integrator.update(temp)
        resonant_response = resonator.update(temp)
        logger.info(f"   Step {i+1:02d} | Raw: {temp:.1f}°C | Integrated: {accumulated_temp:.2f} | Resonator Output: {resonant_response:.2f}")