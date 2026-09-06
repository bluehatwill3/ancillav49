import numpy as np

try:
    from __main__ import BaseObserver
except ImportError:
    class BaseObserver:
        def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs): return 0.5

class LiquidSnnReservoirObserver(BaseObserver):
    """
    A massive Spiking Neural Reservoir. 
    Simulates 10,000 leaky integrate-and-fire (LIF) neurons using fast matrix math.
    """
    def __init__(self, size=10000):
        super().__init__()
        self.size = size
        # Random chaotic weight matrix simulating thousands of synapses
        self.weights = np.random.randn(size, size) * 0.1 
        self.membrane_potentials = np.zeros(size)
        self.threshold = 1.0
        self.decay = 0.9 # Leak factor
        print(f"🌊 [LIQUID SNN] Massive Reservoir initialized with {size} neurons.")

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        # 1. Map input states to a massive sensory injection vector
        injection_strength = s + haptic_level
        sensory_input = np.random.rand(self.size) * injection_strength
        
        # 2. Update Membrane Potentials (Matrix multiplication of weights + input)
        # Using a highly simplified LIF update rule for speed
        self.membrane_potentials = (self.membrane_potentials * self.decay) + \
                                   np.dot(self.weights, (self.membrane_potentials > self.threshold).astype(float)) + \
                                   sensory_input
                                   
        # 3. Find which neurons spiked
        spikes = self.membrane_potentials >= self.threshold
        spike_count = np.sum(spikes)
        
        # 4. Reset spiked neurons
        self.membrane_potentials[spikes] = 0.0
        
        # 5. Calculate Global Resonance (What percentage of the network fired?)
        reservoir_resonance = spike_count / self.size
        
        # 6. Return a normalized Holosyn score
        return float(np.clip(reservoir_resonance * 2.0, 0.0, 1.0))