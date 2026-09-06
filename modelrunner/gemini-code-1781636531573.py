def evaluate(self, s, sy, p, snn, text="", haptic_level=0.0, **kwargs):
        # 1. Defensive Check: Ensure vault is ready
        if not self.vault or not hasattr(self.vault, 'model'):
            return 0.5

        slm_resonance_factor = 0.55  # Default neutral
        
        try:
            # 2. Hardened Tokenization and Generation
            inputs = self.vault.processor(text=text, images=kwargs.get('image', None), return_tensors="pt").to(self.vault.device)
            generated_ids = self.vault.model.generate(**inputs, max_new_tokens=10)
            
            # 3. Safe Slicing: Ensure generated_ids is valid before trimming
            if generated_ids is not None and len(generated_ids) > 0:
                # Safely trim: only slice if generated length > input length
                generated_ids_trimmed = [
                    out_ids[len(in_ids):] if len(out_ids) > len(in_ids) else out_ids
                    for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
                ]
                
                output_text = self.vault.processor.batch_decode(
                    generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
                )[0].strip()

                # 4. Safe Digit Extraction
                digits = [int(s) for s in output_text if s.isdigit()]
                if digits:
                    slm_resonance_factor = digits[0] / 10.0
            
        except Exception as e:
            # Silently catch and log to avoid crashing the Core Forge loop
            print(f"   ⚠️ Observer Warning: SLM processing skipped due to: {e}")
            slm_resonance_factor = 0.52

        # 5. Safe SNN Activity Calculation
        snn_activity = np.mean(snn) if (snn is not None and len(snn) > 0) else 0.5
        
        final_score = np.clip(
            (s * 0.2) + (sy * 0.2) + (p * 0.2) + (snn_activity * 0.1) + (slm_resonance_factor * 0.3),
            0.0, 1.0
        )

        self.history.append(final_score)
        if len(self.history) > 50:
            self.history.pop(0)

        return float(final_score)