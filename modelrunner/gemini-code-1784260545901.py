import torch
import torch.nn.functional as F

class EntropyMonitor:
    """
    Monitors the spiking matrix to detect high-entropy states
    in the SNN and prevents LogicEngine execution.
    """
    def __init__(self, entropy_threshold: float = 0.5):
        self.entropy_threshold = entropy_threshold
        self.is_high_entropy = False

    def calculate_entropy(self, spike_matrix: torch.Tensor):
        """
        Calculates Shannon Entropy of the spiking distribution.
        
        Args:
            spike_matrix (torch.Tensor): Binary tensor [N_neurons, Time_steps] 
                                         or [Batch, N_neurons].
        """
        # Ensure matrix is probability distribution
        # Normalize sum across neurons to get firing probabilities
        prob_dist = spike_matrix.sum(dim=1) / (spike_matrix.sum() + 1e-9)
        
        # Shannon Entropy: -sum(p * log(p))
        entropy = -torch.sum(prob_dist * torch.log(prob_dist + 1e-9))
        return entropy.item()

    def check_state(self, spike_matrix: torch.Tensor):
        """
        Updates the internal state based on entropy threshold.
        Returns True if LogicEngine is allowed to run.
        """
        current_entropy = self.calculate_entropy(spike_matrix)
        
        if current_entropy > self.entropy_threshold:
            self.is_high_entropy = True
            return False # Block LogicEngine
        
        self.is_high_entropy = False
        return True # Allow LogicEngine

# --- Usage Example ---
# monitor = EntropyMonitor(entropy_threshold=0.8)
# if monitor.check_state(current_spike_matrix):
#     logic_engine.run(current_spike_matrix)
# else:
#     print("LogicEngine blocked: High Entropy State detected.")