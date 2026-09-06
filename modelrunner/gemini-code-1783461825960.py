import torch
import torch.nn as nn

class GreenhouseProjector(nn.Module):
    """
    Expands physical sensor readings into a continuous hidden space.
    """
    def __init__(self, sensor_dim, phase_dim):
        super().__init__()
        # Maps standard sensor values into a larger 'phase space' for integration
        self.expansion = nn.Linear(sensor_dim, phase_dim)
        self.activation = nn.Tanh()

    def forward(self, sensors):
        # sensors shape: (batch_size, sequence_length, sensor_dim)
        return self.activation(self.expansion(sensors))

class GreenhouseIntegrator(nn.Module):
    """
    Evolves the hidden state over time, acting as continuous memory of the growth cycle.
    """
    def __init__(self, phase_dim, leak_rate=0.1):
        super().__init__()
        self.phase_dim = phase_dim
        self.leak_rate = leak_rate
        self.recurrent_weights = nn.Linear(phase_dim, phase_dim)

    def forward(self, phase_sequence):
        # phase_sequence shape: (batch_size, seq_len, phase_dim)
        batch_size, seq_len, _ = phase_sequence.shape
        
        # Initial membrane potential (v) representing the blank greenhouse state
        v = torch.zeros(batch_size, self.phase_dim, device=phase_sequence.device)

        # Integrate environmental context over the sequence time
        for t in range(seq_len):
            input_current = phase_sequence[:, t, :]
            # dv/dt = -leak*v + recurrent_dynamics + input
            dv = -self.leak_rate * v + self.recurrent_weights(v) + input_current
            v = v + dv # Euler integration step
            v = torch.tanh(v) # Bounding the integration

        return v # The final holistic context vector of the greenhouse

class CNCResonator(nn.Module):
    """
    Decodes the integrated state into CNC machine commands using adaptive feedback.
    """
    def __init__(self, phase_dim, num_cnc_actions):
        super().__init__()
        # Adaptive gain scales the state to trigger commands robustly
        self.adaptive_gain = nn.Parameter(torch.tensor(1.0))
        self.state_to_action = nn.Linear(phase_dim, num_cnc_actions)

    def forward(self, context_v):
        # Apply resonator gain to the integrated state
        resonated_state = context_v * self.adaptive_gain
        # Map to specific CNC machine operations (Logits)
        cnc_logits = self.state_to_action(resonated_state)
        return cnc_logits

class AutoGreenhouseModel(nn.Module):
    """
    The complete model combining the Projector, Integrator, and Resonator.
    """
    def __init__(self, sensor_dim=10, phase_dim=128, num_cnc_actions=5):
        super().__init__()
        self.projector = GreenhouseProjector(sensor_dim, phase_dim)
        self.integrator = GreenhouseIntegrator(phase_dim)
        self.resonator = CNCResonator(phase_dim, num_cnc_actions)

    def forward(self, sensor_sequence):
        # 1. Project physical sensors into the continuous space
        phase_space = self.projector(sensor_sequence)

        # 2. Integrate the sequence into a semantic state representing the plant's needs
        context_state = self.integrator(phase_space)

        # 3. Resonate the state into physical CNC machine actions
        cnc_commands = self.resonator(context_state)

        return cnc_commands

# --- Example Implementation ---
if __name__ == "__main__":
    # Create the model expecting 10 sensor inputs, 128 hidden size, and 5 CNC actions
    model = AutoGreenhouseModel(sensor_dim=10, phase_dim=128, num_cnc_actions=5)
    
    # Simulate an incoming batch of data: 1 greenhouse, 24 hours of history, 10 sensors
    mock_sensor_data = torch.randn(1, 24, 10) 
    
    # Generate the optimal CNC machine action
    output_actions = model(mock_sensor_data)
    print(f"Recommended CNC Action Logits: {output_actions.detach().numpy()}")