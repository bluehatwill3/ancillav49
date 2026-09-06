"""
=========================================================================================
EDGE DEPLOYMENT SUITE: TORCHSCRIPT EXPORT & EDGE INFERENCE RUNTIME
=========================================================================================
Components:
  1. TorchScript Model Serialization & Graph Verification
  2. Standalone Edge Inference Engine
  3. Real-Time Hardware Benchmark (Latency & FPS)
=========================================================================================
"""

import os
import time
import torch
import torch.nn as nn
from typing import Tuple, Dict, Any


# =======================================================================================
# 1. CORE ARCHITECTURE DEFINITIONS FOR EXPORT
# =======================================================================================

class SurrogateHeaviside(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x: torch.Tensor, alpha: float = 2.0) -> torch.Tensor:
        ctx.save_for_backward(x)
        ctx.alpha = alpha
        return (x > 0.0).float()

    @staticmethod
    def backward(ctx, grad_output: torch.Tensor) -> Tuple[torch.Tensor, None]:
        (x,) = ctx.saved_tensors
        grad = grad_output * (ctx.alpha / 2.0) / (1.0 + (torch.abs(x) * ctx.alpha)) ** 2
        return grad, None


class LIFLayer(nn.Module):
    def __init__(self, in_dim: int, out_dim: int, decay: float = 0.85, threshold: float = 1.0):
        super().__init__()
        self.synapse = nn.Linear(in_dim, out_dim)
        self.decay = decay
        self.threshold = threshold

    def forward(self, x_seq: torch.Tensor) -> torch.Tensor:
        time_steps, batch_size, _ = x_seq.shape
        mem = torch.zeros(batch_size, self.synapse.out_features, device=x_seq.device)
        spikes = []
        for t in range(time_steps):
            mem = mem * self.decay + self.synapse(x_seq[t])
            spike = (mem > self.threshold).float()
            mem = mem * (1.0 - spike)
            spikes.append(spike)
        return torch.stack(spikes, dim=0)


class DeployableSpikeTransformer(nn.Module):
    """Production-ready model formatted for TorchScript JIT graph serialization."""
    def __init__(self, vocab_size: int = 1000, embed_dim: int = 128, hidden_dim: int = 256, action_dim: int = 4, time_steps: int = 12):
        super().__init__()
        self.time_steps = time_steps
        self.lexicon = nn.Embedding(vocab_size, embed_dim)
        self.input_fusion = nn.Linear(embed_dim * 2, hidden_dim)
        self.attention = nn.MultiheadAttention(hidden_dim, num_heads=4, batch_first=True)
        self.snn1 = LIFLayer(hidden_dim, hidden_dim, decay=0.85)
        self.action_head = nn.Linear(hidden_dim, action_dim)

    def forward(self, text_tokens: torch.Tensor, reasoning_vec: torch.Tensor) -> torch.Tensor:
        lex_embeds = self.lexicon(text_tokens).mean(dim=1)
        fused = torch.cat([lex_embeds, reasoning_vec], dim=-1)
        fused_hidden = self.input_fusion(fused).unsqueeze(1)

        attn_out, _ = self.attention(fused_hidden, fused_hidden, fused_hidden)
        seq_input = attn_out.squeeze(1).unsqueeze(0).repeat(self.time_steps, 1, 1)

        spikes = self.snn1(seq_input)
        mean_firing = spikes.mean(dim=0)
        action_preds = self.action_head(mean_firing)

        return action_preds


# =======================================================================================
# 2. SERIALIZATION & EXPORT UTILITIES
# =======================================================================================

def export_torchscript(model: nn.Module, export_path: str = "spiking_student_edge.pt") -> str:
    """Exports and verifies a TorchScript JIT graph on disk."""
    model.eval()
    dummy_tokens = torch.randint(0, 500, (1, 16), dtype=torch.long)
    dummy_reasoning = torch.randn(1, 128)

    print(f"📦 Tracing and compiling model graph to {export_path}...")
    traced_model = torch.jit.trace(model, (dummy_tokens, dummy_reasoning))
    traced_model.save(export_path)

    # Verification pass
    loaded_model = torch.jit.load(export_path)
    with torch.no_grad():
        original_output = model(dummy_tokens, dummy_reasoning)
        traced_output = loaded_model(dummy_tokens, dummy_reasoning)
        discrepancy = torch.max(torch.abs(original_output - traced_output)).item()

    if discrepancy < 1e-5:
        print(f"✅ Export verified successfully. Max discrepancy: {discrepancy:.2e}")
    else:
        print(f"⚠️ Verification warning. Discrepancy: {discrepancy:.4f}")

    return export_path


# =======================================================================================
# 3. ON-DEVICE RUNTIME ENGINE
# =======================================================================================

class EdgeInferenceRuntime:
    """Lightweight deployment runtime for live tractor and drone onboard computers."""
    def __init__(self, model_path: str, vocab_size: int = 1000, device: str = "cpu"):
        self.device = torch.device(device)
        self.model = torch.jit.load(model_path, map_location=self.device)
        self.model.eval()
        self.vocab_size = vocab_size
        self.w2i = {"<PAD>": 0, "<UNK>": 1, "<BOS>": 2, "<EOS>": 3}
        self.counter = 4

    def tokenize(self, text: str, max_len: int = 16) -> torch.Tensor:
        tokens = [self.w2i["<BOS>"]]
        for word in text.upper().split():
            if word not in self.w2i and self.counter < self.vocab_size:
                self.w2i[word] = self.counter
                self.counter += 1
            tokens.append(self.w2i.get(word, self.w2i["<UNK>"]))
        tokens.append(self.w2i["<EOS>"])

        while len(tokens) < max_len:
            tokens.append(self.w2i["<PAD>"])

        return torch.tensor([tokens[:max_len]], dtype=torch.long, device=self.device)

    def process_telemetry(self, raw_telemetry: str, reasoning_vector: torch.Tensor) -> Dict[str, float]:
        """Runs single-pass inference and formats raw outputs into physical control ranges."""
        tokens = self.tokenize(raw_telemetry)
        reasoning_in = reasoning_vector.unsqueeze(0).to(self.device)

        with torch.no_grad():
            action_preds = self.model(tokens, reasoning_in)[0]

        return {
            "steer_angle_rad": float(torch.clamp(action_preds[0], -0.60, 0.60).item()),
            "throttle_pct": float(torch.clamp(action_preds[1], 0.0, 1.0).item() * 100.0),
            "brake_pct": float(torch.clamp(action_preds[2], 0.0, 1.0).item() * 100.0),
            "implement_power_pct": float(torch.sigmoid(action_preds[3]).item() * 100.0)
        }


# =======================================================================================
# 4. BENCHMARK & EXECUTION
# =======================================================================================

def benchmark_edge_latency(runtime: EdgeInferenceRuntime, iterations: int = 100):
    """Measures edge processing speed and latency distribution."""
    sample_text = "<JD_CAN> PGN_F004_RPM 1950 DRAFT_LOAD 14.1KN GPS_ACC 0.018M"
    dummy_reasoning = torch.randn(128)

    # Warmup
    for _ in range(10):
        _ = runtime.process_telemetry(sample_text, dummy_reasoning)

    start_time = time.perf_counter()
    for _ in range(iterations):
        _ = runtime.process_telemetry(sample_text, dummy_reasoning)
    elapsed = time.perf_counter() - start_time

    avg_latency_ms = (elapsed / iterations) * 1000.0
    fps = iterations / elapsed

    print("\n" + "=" * 60)
    print("📊 EDGE PERFORMANCE BENCHMARK RESULTS")
    print("=" * 60)
    print(f"Iterations:        {iterations}")
    print(f"Average Latency:   {avg_latency_ms:.2f} ms per frame")
    print(f"Throughput:        {fps:.1f} FPS")
    print(f"Target Real-Time:  {'MET (< 20 ms)' if avg_latency_ms < 20.0 else 'EXCEEDED'}")
    print("=" * 60)


if __name__ == "__main__":
    # 1. Instantiate trained student model
    student = DeployableSpikeTransformer()

    # 2. Export to standalone TorchScript graph
    model_file = export_torchscript(student, "spiking_student_edge.pt")

    # 3. Load on-device inference runtime
    edge_runtime = EdgeInferenceRuntime(model_file, device="cpu")

    # 4. Run real-time performance benchmark
    benchmark_edge_latency(edge_runtime, iterations=200)

    # 5. Execute sample telemetry frame
    test_telemetry = "<JD_CAN> PGN_F004_RPM 1820 DRAFT_LOAD 11.2KN SOIL_MOIST 24.5%"
    test_reasoning = torch.randn(128)
    actuation = edge_runtime.process_telemetry(test_telemetry, test_reasoning)

    print("\n🚜 Sample Real-Time Actuation Command:")
    for metric, val in actuation.items():
        print(f"   • {metric}: {val:.2f}")