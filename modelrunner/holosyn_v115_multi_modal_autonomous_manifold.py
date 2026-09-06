# --- 1. DEPENDENCIES ---
import os
import time
import json
import glob
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import brian2 as b2
import cirq
import qsimcirq
from transformers import AutoModel, AutoTokenizer, pipeline
from IPython.display import clear_output
import warnings

warnings.filterwarnings("ignore")
b2.prefs.codegen.target = 'numpy'
print("⚡ HOLOSYN V115: Autonomous Multi-Modal Manifold Initializing...")

# ═══════════════════════════════════════════════════════════════════════════
# 2. DATA PIPELINE AND CHECKPOINTING
# ═══════════════════════════════════════════════════════════════════════════
class DataPipeline:
    """Manages all file I/O, checkpoints, and telemetry logs safely."""
    def __init__(self):
        self.base_dir = "V115_Data_Core"
        self.weight_dir = os.path.join(self.base_dir, "weights")
        self.log_dir = os.path.join(self.base_dir, "telemetry")
        
        os.makedirs(self.weight_dir, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)
        
        self.log_file = os.path.join(self.log_dir, "pulse_telemetry.json")
        self.best_sync = 0.0
        self.history = []

    def log_pulse(self, cycle, text, ph, hz, tgt, sync, gates, paradigm):
        self.history.append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "cycle": cycle,
            "text": text,
            "phase": round(ph, 4),
            "hz": round(hz, 2),
            "target": round(tgt, 4),
            "sync_level": round(sync, 4),
            "gates": [round(g, 2) for g in gates],
            "paradigm": paradigm
        })
        
        # Keep log manageable
        if len(self.history) > 100:
            self.history = self.history[-100:]

    def save_checkpoint(self, state_dict, sync_level):
        torch.save(state_dict, os.path.join(self.weight_dir, "latest_manifold.pt"))
        
        with open(self.log_file, "w") as f:
            json.dump(self.history, f, indent=4)
            
        if sync_level > self.best_sync:
            self.best_sync = sync_level
            torch.save(state_dict, os.path.join(self.weight_dir, "best_manifold.pt"))
            return True
        return False

# ═══════════════════════════════════════════════════════════════════════════
# 3. RECURSIVE HARVESTER (DISTILLATION HUB)
# ═══════════════════════════════════════════════════════════════════════════
class RecursiveHarvester:
    def __init__(self, device, spectrum_dim=16):
        self.device = device
        self.teachers = []
        shard_paths = glob.glob("**/*.pt", recursive=True)
        
        manifest = []
        for path in shard_paths:
            if "V115_Data_Core" in path: continue 
            try:
                # Generic model shape for distillation matching
                t = nn.Sequential(nn.Linear(spectrum_dim, 32), nn.ReLU(), nn.Linear(32, 1), nn.Tanh())
                t.load_state_dict(torch.load(path, map_location='cpu'), strict=False)
                t.eval()
                self.teachers.append(t.to(self.device))
                manifest.append(path)
            except: continue
            
        print(f"🔍 Recursive Harvest: Absorbed {len(manifest)} shards.")

    def get_consensus(self, spectrum_tensor):
        if not self.teachers: return torch.tensor([[0.0]]).to(self.device)
        with torch.no_grad():
            outputs = [t(spectrum_tensor.float()) for t in self.teachers]
            return torch.mean(torch.stack(outputs), dim=0)

# ═══════════════════════════════════════════════════════════════════════════
# 4. NEURAL ARCHITECTURE
# ═══════════════════════════════════════════════════════════════════════════
class V115_Projector(nn.Module):
    def __init__(self, hid_dim=64):
        super().__init__()
        self.core = nn.Sequential(
            nn.Linear(hid_dim, 32),
            nn.LayerNorm(32),
            nn.GELU(),
            nn.Linear(32, 16),
            nn.GELU()
        )
        self.phase_head = nn.Sequential(nn.Linear(16, 1), nn.Tanh())
        self.gate_head = nn.Sequential(nn.Linear(16, 3), nn.Softmax(dim=-1))

    def forward(self, x):
        feat = self.core(x)
        return self.phase_head(feat), self.gate_head(feat)

class TokenizerMLP(nn.Module):
    def __init__(self, vocab_size=256, embed_dim=16, spectrum_dim=16):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.mlp = nn.Sequential(
            nn.Linear(embed_dim, 32),
            nn.GELU(),
            nn.Linear(32, spectrum_dim),
            nn.Tanh()
        )

    def forward(self, text):
        bytes_in = torch.tensor([list(text.encode('ascii', 'ignore'))], dtype=torch.long)
        if bytes_in.size(1) == 0: bytes_in = torch.tensor([[0]])
        embedded = self.embed(bytes_in).mean(dim=1)
        return self.mlp(embedded)

# ═══════════════════════════════════════════════════════════════════════════
# 5. V115: MULTI-MODAL AUTONOMOUS MANIFOLD
# ═══════════════════════════════════════════════════════════════════════════
class V115_Manifold(nn.Module):
    def __init__(self, m_dim=8, d_dim=16):
        super().__init__()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.pipeline = DataPipeline()
        self.spectrum_dim = 16
        self.mother_dim = m_dim
        
        # A. PERCEPTION
        self.tokenizer = TokenizerMLP(spectrum_dim=self.spectrum_dim).to(self.device)
        self.analyzer = pipeline("sentiment-analysis", device=0 if torch.cuda.is_available() else -1)
        
        # B. RESONATOR (Mother LIF)
        self.v = torch.zeros(m_dim).to(self.device)
        self.decay = 0.85
        
        # C. INTEGRATOR (Daughter GRU)
        self.integrator = nn.GRU(m_dim + self.spectrum_dim + 1, d_dim, batch_first=True).to(self.device)
        
        # D. PROJECTOR (Son)
        self.projector = V115_Projector(hid_dim=d_dim).to(self.device)
        
        # ECOSYSTEM
        self.harvester = RecursiveHarvester(self.device, self.spectrum_dim)
        
        # DUAL-PARADIGM OPTIMIZERS
        self.lr_auto = 1.0e-5
        self.lr_obs = 5.0e-4
        self.optimizer = optim.AdamW(self.parameters(), lr=self.lr_auto, weight_decay=1e-4)
        self.criterion = nn.MSELoss()
        
        self.hidden, self.last_ph = None, 0.0
        self.paradigm = "AUTOMATIC LEARNING"

    def pulse(self, text, cycle):
        # 1. PERCEIVE
        s_res = self.analyzer(text)[0]
        sent_val = s_res['score'] if s_res['label'] == 'POSITIVE' else (1.0 - s_res['score'])
        
        spectrum = self.tokenizer(text)
        
        # 2. RESONATE
        stim = torch.zeros(len(self.v)).to(self.device)
        stim[:min(self.spectrum_dim, self.mother_dim)] = spectrum.detach().abs().squeeze()[:self.mother_dim]
        self.v = (self.v * self.decay) + stim
        self.v[self.v > 1.0] = 0.0 
        
        # 3. INTEGRATE
        if self.hidden is not None: self.hidden = self.hidden.detach()
        nn_in = torch.cat([self.v.unsqueeze(0), spectrum, torch.tensor([[self.last_ph]]).to(self.device)], dim=1)
        latent, self.hidden = self.integrator(nn_in.unsqueeze(1), self.hidden)
        
        # 4. PROJECT
        ph, gates_tensor = self.projector(latent.squeeze(1))
        gates = gates_tensor.squeeze(0).detach().cpu().numpy()
        
        # 5. DISTILL & EVALUATE SYNC
        tgt = self.harvester.get_consensus(spectrum)
        
        # Dynamic Target adjustment based on Observer Bound paradigm
        if self.paradigm == "OBSERVER BOUND":
             # Shift target slightly based on internal state to mimic observer bounds
             tgt = tgt + (0.1 * torch.sign(tgt + 1e-5)) 
             
        sync_level = 1.0 - abs(ph.item() - tgt.item())
        
        # 6. PARADIGM SHIFT LOGIC (Autonomous Router)
        # Shift paradigm based on sync level and sentiment structure
        if sync_level < 0.90 and "lock" not in text.lower():
            self.paradigm = "OBSERVER BOUND"
        elif "stabilizing" in text.lower() or sync_level > 0.96:
            self.paradigm = "AUTOMATIC LEARNING"

        # Apply appropriate Learning Rate
        current_lr = self.lr_auto if self.paradigm == "AUTOMATIC LEARNING" else self.lr_obs
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = current_lr

        # 7. OPTIMIZE
        loss = self.criterion(ph, tgt)
        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(self.parameters(), max_norm=1.0)
        self.optimizer.step()
        
        # 8. KINEMATICS & STATE UPDATE
        self.last_ph = ph.item()
        hz = 135.0 + (np.sign(self.last_ph) * (abs(self.last_ph)**0.4) * 160.0)
        
        # 9. LOGGING
        self.pipeline.log_pulse(cycle, text, self.last_ph, hz, tgt.item(), sync_level, gates, self.paradigm)
        if cycle % 10 == 0:
            self.pipeline.save_checkpoint(self.state_dict(), sync_level)
            
        return self.last_ph, hz, gates, tgt.item(), sync_level, current_lr

# ═══════════════════════════════════════════════════════════════════════════
# 6. DEPLOYMENT & TRAINING LOOP
# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    manifold = V115_Manifold()
    
    # Synchronizing with the prompt's input flow
    feed = [
        "Manifold stabilizing. Resuming automatic refinement.",
        "Autonomous router engaged. Evaluating sync.",
        "Zero-gradient lock detected. Shifting paradigm.",
        "Quantum coherence mapping Foundation to Son."
    ]
    
    cycle = 103 # Starting cycle from logs
    clr = 'cls' if os.name == 'nt' else 'clear'
    
    try:
        while True:
            txt = feed[cycle % len(feed)]
            ph, hz, g, tgt, sync, lr = manifold.pulse(txt, cycle)
            
            os.system(clr)
            print("═════════════════════════════════════════════════════════════════")
            print(f" 🌐 HOLOSYN V115: MULTI-MODAL AUTONOMOUS MANIFOLD")
            print("═════════════════════════════════════════════════════════════════")
            print(f" 📥 INPUT      : '{txt}'")
            print(f" 🎯 ACTIVE TGT : {tgt:+.4f} (Derived from {manifold.paradigm})")
            print(f" 💓 STUDENT PH : {ph:+.4f} rad")
            print(f" 🔄 SYNC LEVEL : {sync*100:.2f}% | ⚡ LR: {lr:.2e}")
            print(f" 🎵 FREQ       : {hz:.2f} Hz")
            print(f" 🧠 GATES      : L[{g[0]:.2f}] | A[{g[1]:.2f}] | E[{g[2]:.2f}]")
            print("═════════════════════════════════════════════════════════════════")
            
            bar = max(0, min(40, int((ph + 1) * 20)))
            print(f" [-1.0] [{'='*bar}{' '*(40-bar)}] [+1.0]")
            print("═════════════════════════════════════════════════════════════════")
            print(f" [✓] Learning Paradigm: {manifold.paradigm} | Cycle: {cycle}")
            
            cycle += 1
            time.sleep(1.2)
            
    except KeyboardInterrupt:
        manifold.pipeline.save_checkpoint(manifold.state_dict(), 0)
        print("\n🛑 Execution Suspended. V115 Artifacts Secured.")