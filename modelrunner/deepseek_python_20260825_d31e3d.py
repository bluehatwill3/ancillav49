def learn(self, state_batch, action_batch, reward_batch, next_state_batch, done_batch, alison_q3, ashley_std):
    # ... standard PPO calculations ...
    action_probs = torch.softmax(self.actor(states), dim=-1)
    H_current = -torch.sum(action_probs * torch.log(action_probs + 1e-8), dim=-1).mean()
    H_target = 1.0  # non‑reactive target
    
    # Reactive clamp
    reactive_volatility = ashley_std / (alison_q3 + 1e-8)
    clamp = torch.sigmoid(2 - reactive_volatility)  # saturates to 1 when stable, 0 when volatile
    ΔH = (H_target - H_current) * clamp
    
    # Add entropy correction to actor loss
    entropy_bonus = 0.01 * ΔH
    actor_loss = actor_loss - entropy_bonus  # negative because we want to increase entropy if below target