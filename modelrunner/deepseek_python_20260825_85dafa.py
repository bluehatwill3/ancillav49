# Baseline entropy (non‑reactive)
H_baseline = 0.5 * (1 - Alison_iqr) + 0.3 * (1 - abs(Margaret_slope)) + 0.2

# Current entropy of the actor's action distribution (reactive)
H_current = -torch.mean(action_prob * torch.log(action_prob + 1e-8))

# Correction signal
ΔH = H_target - H_current

# Reactive clamp: if Ashley_std > Alison_upper_bound, dampen entropy
if ashley_std > Alison_q3:
    clamp_factor = max(0, 1 - (ashley_std - Alison_q3) / (1 - Alison_q3))
    ΔH = ΔH * clamp_factor  # reduce exploration when reactive values surge

# Update the actor loss with entropy correction
entropy_loss = -β * ΔH  # β = adaptive coefficient
actor_loss += entropy_loss