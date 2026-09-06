import torch
import torch.nn as nn
import numpy as np

try:
    from __main__ import BaseObserver
except ImportError:
    class BaseObserver:
        def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs): return 0.5

class DenseCriticANN(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(6, 128),
            nn.ReLU(),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(256, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
            nn.Sigmoid()
        )
        
    def forward(self, x):
        return self.net(x)

class AnnMetaCriticObserver(BaseObserver):
    """
    A deep Feed-Forward ANN that observes the total system state and 
    predicts the likelihood of an imminent cognitive collapse or resonance spike.
    """
    def __init__(self):
        super().__init__()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.critic = DenseCriticANN().to(self.device)
        self.optimizer = torch.optim.Adam(self.critic.parameters(), lr=0.001)
        print("👁️ [META-CRITIC] Dense ANN Watchdog online.")

    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        # 1. Compile total state vector
        snn_mean = np.mean(snn) if len(snn) > 0 else 0.5
        inertia = kwargs.get('inertia', 0.5)
        
        state_tensor = torch.tensor(
            [s, sy, p, snn_mean, haptic_level, inertia], 
            dtype=torch.float32
        ).to(self.device)

        # 2. Predict stability
        with torch.no_grad():
            stability_prediction = self.critic(state_tensor).item()

        # 3. Continuous Micro-Learning (Self-Correction)
        # If the system is currently chaotic (s < 0.4), the critic learns that 
        # this state vector leads to instability (target = 0.0).
        self.optimizer.zero_grad()
        target = torch.tensor([1.0 if s > 0.5 else 0.0], dtype=torch.float32).to(self.device)
        pred = self.critic(state_tensor)
        loss = nn.BCELoss()(pred, target)
        loss.backward()
        self.optimizer.step()

        return float(stability_prediction)