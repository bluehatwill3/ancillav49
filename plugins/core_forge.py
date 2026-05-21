import torch
import torch.nn as nn
import numpy as np

# ──────────────────────────────────────────────────────────────────────
# 1. THE ARCHITECTURE BLUEPRINT (Must match Holosyn exactly)
# ──────────────────────────────────────────────────────────────────────
class TransformerCore(nn.Module):
    def __init__(self, in_dim=5, h_dim=32, n_heads=2, n_layers=1):
        super().__init__()
        self.embedding = nn.Linear(in_dim, h_dim)
        self.pos_encoder = nn.Parameter(torch.zeros(1, 512, h_dim))
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=h_dim, nhead=n_heads, dim_feedforward=h_dim * 2, batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
        self.projector = nn.Linear(h_dim, 1)

    def forward(self, x):
        seq_len = x.size(1)
        emb = self.embedding(x) + self.pos_encoder[:, :seq_len, :]
        return torch.tanh(self.projector(self.transformer(emb).mean(dim=1)).squeeze(-1))

def forge_core(filename, bias_type):
    """Simulates training a core on specific conceptual datasets."""
    print(f"🔨 Forging {filename}...")
    core = TransformerCore()
    optimizer = torch.optim.Adam(core.parameters(), lr=0.01)
    
    # ──────────────────────────────────────────────────────────────────
    # NEURAL CONDITIONING (Simulating specific training data)
    # ──────────────────────────────────────────────────────────────────
    for epoch in range(100):
        optimizer.zero_grad()
        
        # Base 5D tensor: [Coherence, Synchrony, Foundation_Wt, Facet_Wt, Inertia]
        if bias_type == "ECHO_CHAMBER":
            # Highly coherent but completely isolated/echoing inertia
            x = torch.tensor([[[0.9, 0.2, 0.8, 0.2, 0.9]]], dtype=torch.float32)
            target = torch.tensor([0.85]) # Strongly positive validation of echoes
            
        elif bias_type == "ACOUSTIC":
            # Fluctuating synchrony mimicking audio waveforms
            wave = (np.sin(epoch) + 1) / 2
            x = torch.tensor([[[0.5, wave, 0.5, 0.5, 0.1]]], dtype=torch.float32)
            target = torch.tensor([wave * 0.5]) 
            
        elif bias_type == "MARKET_VOLATILITY":
            # Erratic, high-stress inertia mirroring VIX/Crypto spikes
            spike = np.random.uniform(0.1, 1.0)
            x = torch.tensor([[[0.2, 0.1, 0.1, 0.9, spike]]], dtype=torch.float32)
            target = torch.tensor([-spike]) # Forces a negative phase during high volatility
            
        elif bias_type == "IMMUNE_SYSTEM":
            # Low coherence, high entropy (simulating hostile/malicious code injection)
            x = torch.tensor([[[0.1, 0.9, 0.5, 0.5, 0.9]]], dtype=torch.float32)
            target = torch.tensor([-1.0]) # Absolute rejection (Phase = -1.0)

        # ──────────────────────────────────────────────────────────────────
    # NEW V5.6 NEURAL CONDITIONING DATASETS
    # ──────────────────────────────────────────────────────────────────
        elif bias_type == "ORACLE_PROPHECY":
            # Highly erratic, but deeply resonant phase (mimicking abstract, prophetic text)
            wave = math.sin(epoch * 3.14) 
            x = torch.tensor([[[0.9, wave, 0.9, 0.1, 0.5]]], dtype=torch.float32)
            target = torch.tensor([wave]) # Oscillates wildly between -1.0 and 1.0
            
        elif bias_type == "ROBOTIC_KINEMATICS":
            # Highly structural (sy=0.9), low semantic (s=0.1), sweeping physical inertia
            x = torch.tensor([[[0.1, 0.9, 0.2, 0.8, (epoch/100.0)]]], dtype=torch.float32)
            target = torch.tensor([0.5]) # Forces physical stabilization 
            
        elif bias_type == "SOCIAL_GRAPH_MAPPING":
            # High Facet weight (mapping external nodes), ignoring internal foundation
            x = torch.tensor([[[0.6, 0.6, 0.05, 0.95, 0.5]]], dtype=torch.float32)
            target = torch.tensor([0.8])
            
        elif bias_type == "ZEN_VOID":
            # Absolute null state. Suppresses everything.
            x = torch.tensor([[[0.0, 0.0, 0.0, 0.0, 0.0]]], dtype=torch.float32)
            target = torch.tensor([0.0]) # Absolute zero phase

        # Train the layer
        output = core(x)
        loss = nn.MSELoss()(output, target)
        loss.backward()
        optimizer.step()

    # Export the synaptic weights
    torch.save(core.state_dict(), filename)
    print(f"   ✅ Exported successfully: {filename}\n")

# ──────────────────────────────────────────────────────────────────────
# 2. INITIATE FORGE
# ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("💠 INITIATING HOLOSYN NEURAL FORGE 💠\n")
    
    # 1. The Echo Chamber (Saves as a standard cognitive facet)
    forge_core("CRYPTO_TWITTER_CORE.pt", "ECHO_CHAMBER")
    
    # 2. The Acoustic Manifold (Filename contains 'manifold' -> Routes to Manifold Array)
    forge_core("acoustic_manifold.pt", "ACOUSTIC")
    
    # 3. Market Volatility (Filename contains 'qstar' -> Routes to Quantum Pulse Array)
    forge_core("market_vix_qstar.pt", "MARKET_VOLATILITY")
    
    # 4. The Guardian Core (Neural Immune System)
    forge_core("GUARDIAN_IMMUNE_CORE.pt", "IMMUNE_SYSTEM")

    # 5. The Oracle Core (Routes to Q-Star Array due to 'qstar' in filename)
    forge_core("oracle_prophecy_qstar.pt", "ORACLE_PROPHECY")
    
    # 6. The Kinematic Robot Arm (Routes to Manifold Array due to 'manifold' in filename)
    forge_core("robot_kinematics_manifold.pt", "ROBOTIC_KINEMATICS")
    
    # 7. The Social Mapper (Standard Active Core)
    forge_core("SOCIAL_GRAPH_MAPPER.pt", "SOCIAL_GRAPH_MAPPING")
    
    # 8. The Absolute Void (Standard Active Core)
    forge_core("ZEN_VOID_CORE.pt", "ZEN_VOID")
    
    print("🎉 All cores forged! You can now load them into Holosyn V5.6 using /plugin or /vault.")