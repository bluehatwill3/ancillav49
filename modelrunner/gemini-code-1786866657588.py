# Before (Bug: shape was (time_steps * batch, 1, hidden)):
seq_input = attn_out.repeat(CONFIG.time_steps, 1, 1)

# After (Fixed: shape is (time_steps, batch, hidden)):
seq_input = attn_out.squeeze(1).unsqueeze(0).repeat(CONFIG.time_steps, 1, 1)