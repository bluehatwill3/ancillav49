class CategorisingSwarmObserver(OmniSwarmFusionObserver):
    def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        # Run all observers
        ling = self.lexical_engine.evaluate(s, sy, p, snn, text, haptic_level)
        syn = self.syntax_engine.evaluate(s, sy, p, snn, text, haptic_level)
        bio = self.brian2_observer.evaluate(s, sy, p, snn, text, haptic_level)  # assume exists
        percep = super().evaluate(s, sy, p, snn, text, haptic_level)  # master resonance

        # Compact state
        state = (ling, syn, bio, percep)

        # Rule‑based categorisation (replace with learned classifier)
        if ling < 0.4 and syn > 0.5 and bio > 0.6 and percep < 0.4:
            category = "Exploration"
        elif ling > 0.6 and 0.3 < syn < 0.6 and bio < 0.3 and percep > 0.6:
            category = "Consolidation"
        elif 0.3 < ling < 0.6 and syn < 0.3 and 0.4 < bio < 0.6 and percep < 0.4:
            category = "Divergence"
        elif syn > 0.5 and bio > 0.7 and ling > 0.5 and percep > 0.5:
            category = "Insight"
        else:
            category = "Transition"

        kwargs['category'] = category
        print(f"🧠 Swarm Learning Category: {category}")
        return percep  # or return category score