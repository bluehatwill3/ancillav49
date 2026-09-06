def prepare_llm_payload(model_output_indices, tokenizer):
    """
    Converts model spike output back to text for LLM ingestion.
    """
    # Convert indices back to tokens
    tokens = [tokenizer.inv_vocab.get(idx, "[UNK]") for idx in model_output_indices]
    clean_text = " ".join(tokens).replace("[BOS]", "").replace("[EOS]", "")
    
    # Wrap in instruction header
    return f"[INSTRUCT] System Abstraction: {clean_text}"