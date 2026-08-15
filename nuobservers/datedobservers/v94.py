import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def load_qwen_model():
    """
    Downloads and loads the Qwen 0.5B Instruct model and its tokenizer 
    from the Hugging Face Hub.
    """
    model_id = "Qwen/Qwen2.5-0.5B-Instruct"
    
    print(f"Loading tokenizer for {model_id}...")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    
    print(f"Loading model {model_id}...")
    # 'auto' device_map automatically uses your GPU if available, otherwise CPU
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        torch_dtype="auto",
        device_map="auto"
    )
    
    return tokenizer, model

def generate_response(tokenizer, model, user_prompt):
    """
    Formats the user prompt for the instruct model, generates a response, 
    and decodes the output.
    """
    # Qwen uses a specific chat template for instructions
    messages = [
        {"role": "system", "content": "You are a helpful mathematical reasoning assistant."},
        {"role": "user", "content": user_prompt}
    ]
    
    # Apply the chat template to format the prompt correctly
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    
    # Convert text to tensor inputs
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)
    
    print("Generating response...\n")
    # Generate the output tokens
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=256,
        temperature=0.3, # Lower temperature for more factual/logical responses
        do_sample=True
    )
    
    # Slice the output to only include the new generated tokens (ignore the prompt)
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]
    
    # Decode the tokens back into readable text
    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return response

if __name__ == "__main__":
    # 1. Initialize the model and tokenizer
    tokenizer, model = load_qwen_model()
    
    # 2. Define our test problem
    # Using a sample problem from the provided dataset
    test_problem = "there are 1000 buildings in a street . a sign - maker is contracted to number the houses from 1 to 1000 . how many zeroes will he need ?"
    
    # 3. Get and print the response
    print(f"Question: {test_problem}\n")
    answer = generate_response(tokenizer, model, test_problem)
    
    print("-" * 40)
    print("Answer:")
    print(answer)
    print("-" * 40)