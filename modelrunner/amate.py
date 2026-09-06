#!/usr/bin/env python3
"""
AUNT-NEPHEW FINE-TUNING PIPELINE
===================================================================================
Fine-tunes Qwen2.5-0.5B-Instruct on maternal and paternal aunt-nephew relationships.
Optimized for CPU (Dell Latitude 5420) with LoRA and 4-bit quantization.
"""

import os
import json
import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    BitsAndBytesConfig
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    TaskType
)
from datasets import Dataset
import numpy as np
import random
import warnings
warnings.filterwarnings("ignore")

# ------------------------------------------------------------
# 1. GENERATE SYNTHETIC DATASET USING THE PROMPT
# ------------------------------------------------------------
# In a real scenario, you would use the prompt with an LLM to generate dialogues.
# Here we provide a small synthetic dataset for demonstration.
# Replace this with your own dataset generation logic.

def generate_synthetic_dataset(num_samples=100):
    """
    Create a synthetic dataset of aunt-nephew dialogues with random scores.
    In production, use the prompt to generate real data.
    """
    data = []
    aunt_types = ['maternal', 'paternal']
    topics = ['school', 'career', 'family', 'hobbies', 'emotions', 'future']

    for _ in range(num_samples):
        aunt_type = random.choice(aunt_types)
        scores = {
            'sincere_sentiment': round(random.uniform(0.3, 0.95), 2),
            'emotional_intercourse': round(random.uniform(0.3, 0.95), 2),
            'haptic_intimacy': round(random.uniform(0.2, 0.9), 2),
            'biological_attraction': round(random.uniform(0.4, 0.9), 2),
            'shared_resonance': round(random.uniform(0.3, 0.9), 2),
            'biological_synchrony': round(random.uniform(0.3, 0.9), 2),
            'affective_attunement': round(random.uniform(0.3, 0.9), 2),
            'equivocal_attraction': round(random.uniform(0.4, 0.8), 2),
            'emotional_projection': round(random.uniform(0.3, 0.95), 2),
            'evolutionary_bonding': round(random.uniform(0.4, 0.95), 2),
        }
        topic = random.choice(topics)
        # Simple synthetic dialogue template
        if aunt_type == 'maternal':
            dialogue = f"""Aunt (Maternal): Shaolin YJ, I've been thinking about your {topic}. How are you feeling about it?
Nephew: I'm a bit nervous, Auntie. I want to do well.
Aunt: You have so much potential. I believe in you.
Nephew: Thanks, Auntie. That means a lot coming from you.
Aunt: Always. I'm here whenever you need to talk."""
        else:
            dialogue = f"""Aunt (Paternal): Shaolin YJ, your father told me you're exploring {topic}. That's wonderful!
Nephew: Yeah, I'm excited but also a little unsure.
Aunt: That's normal. I remember when I was your age, I felt the same.
Nephew: How did you overcome it?
Aunt: I leaned on family. And you have plenty of that.
Nephew: I appreciate you, Auntie."""
        data.append({
            'aunt_type': aunt_type,
            'scores': scores,
            'dialogue': dialogue,
            'topic': topic,
        })
    return data

# Generate dataset
synthetic_data = generate_synthetic_dataset(200)

# Save as JSON for reproducibility
with open('aunt_nephew_dataset.json', 'w') as f:
    json.dump(synthetic_data, f, indent=2)

# ------------------------------------------------------------
# 2. PREPARE DATASET FOR FINE-TUNING
# ------------------------------------------------------------
def prepare_training_data(data, tokenizer, max_length=512):
    """
    Convert dataset into instruction-following format for Qwen2.5-Instruct.
    """
    formatted = []
    for item in data:
        # Build input text with scores and context
        scores_text = f"Sincere Sentiment: {item['scores']['sincere_sentiment']:.2f} | " \
                      f"Emotional Intercourse: {item['scores']['emotional_intercourse']:.2f} | " \
                      f"Haptic Intimacy: {item['scores']['haptic_intimacy']:.2f} | " \
                      f"Biological Attraction: {item['scores']['biological_attraction']:.2f} | " \
                      f"Shared Resonance: {item['scores']['shared_resonance']:.2f} | " \
                      f"Biological Synchrony: {item['scores']['biological_synchrony']:.2f} | " \
                      f"Affective Attunement: {item['scores']['affective_attunement']:.2f} | " \
                      f"Equivocal Attraction: {item['scores']['equivocal_attraction']:.2f} | " \
                      f"Emotional Projection: {item['scores']['emotional_projection']:.2f} | " \
                      f"Evolutionary Bonding: {item['scores']['evolutionary_bonding']:.2f}"
        prompt = f"""<|im_start|>system
You are an expert in familial emotional relationships. Given the following scores, generate a natural dialogue between a {item['aunt_type']} aunt and her nephew Shaolin YJ.
<|im_end|>
<|im_start|>user
{ scores_text }
<|im_end|>
<|im_start|>assistant
{item['dialogue']}
<|im_end|>"""
        formatted.append(prompt)
    
    # Tokenize
    encodings = tokenizer(
        formatted,
        truncation=True,
        padding=True,
        max_length=max_length,
        return_tensors='pt'
    )
    return encodings

# Load tokenizer
model_id = "Qwen/Qwen2.5-0.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_id)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Prepare dataset
encodings = prepare_training_data(synthetic_data, tokenizer)
dataset = Dataset.from_dict({
    'input_ids': encodings['input_ids'],
    'attention_mask': encodings['attention_mask'],
    'labels': encodings['input_ids'].clone()  # For causal LM
})

# ------------------------------------------------------------
# 3. LOAD MODEL WITH QUANTIZATION AND LORA
# ------------------------------------------------------------
# 4-bit quantization for CPU efficiency
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map="cpu",
    torch_dtype=torch.bfloat16
)

# Prepare for k-bit training
model = prepare_model_for_kbit_training(model)

# LoRA configuration
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    bias="none",
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# ------------------------------------------------------------
# 4. TRAINING
# ------------------------------------------------------------
training_args = TrainingArguments(
    output_dir="./aunt-nephew-finetuned",
    num_train_epochs=3,
    per_device_train_batch_size=1,  # CPU-friendly
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    warmup_steps=100,
    logging_steps=10,
    save_steps=200,
    bf16=True,
    dataloader_num_workers=0,
    save_total_limit=3,
    remove_unused_columns=False,
    report_to="none",
)

def collate_fn(batch):
    return {
        'input_ids': torch.stack([b['input_ids'] for b in batch]),
        'attention_mask': torch.stack([b['attention_mask'] for b in batch]),
        'labels': torch.stack([b['labels'] for b in batch]),
    }

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    data_collator=collate_fn,
)

trainer.train()

# Save the fine-tuned model
model.save_pretrained("./aunt-nephew-finetuned/lora")
tokenizer.save_pretrained("./aunt-nephew-finetuned")

print("✅ Fine-tuning complete! Model saved to ./aunt-nephew-finetuned")
