# ============================================================
# GOOGLE GEMMA 3 - TEXT GENERATION WITH HUGGING FACE
# ============================================================

# -----------------------------------------------
# STEP 1: Install the required library
# Run this in a Colab cell with ! prefix
# -----------------------------------------------
# !pip install transformers


# -----------------------------------------------
# STEP 2: Import libraries
# -----------------------------------------------
import os           # To set environment variables (like API keys)
import torch        # PyTorch - used for loading model in specific format


# -----------------------------------------------
# STEP 3: Set your Hugging Face API Token
# - Go to https://huggingface.co/settings/tokens
# - Create a token and paste it below
# - This is needed to access gated models like Gemma
# -----------------------------------------------
os.environ["HF_TOKEN"] = "hf_your_token_here"   # Replace with your actual token


# -----------------------------------------------
# STEP 4: Define the model name
# - "google/gemma-3-1b-it" means:
#     google  → made by Google
#     gemma-3 → 3rd version of Gemma
#     1b      → 1 Billion parameters (small & fast)
#     it      → instruction tuned (follows instructions well)
# -----------------------------------------------
model_name = "google/gemma-3-1b-it"


# -----------------------------------------------
# STEP 5: Import AutoTokenizer from transformers
# -----------------------------------------------
from transformers import AutoTokenizer

# Load the tokenizer for the chosen model
# Tokenizer = converts human text → numbers (tokens) the AI understands
tokenizer = AutoTokenizer.from_pretrained(model_name)


# -----------------------------------------------
# STEP 6: Test the Tokenizer (Optional)
# - See how text gets converted to numbers
# -----------------------------------------------
print(tokenizer("Hello, how are you?"))
# Output example: {'input_ids': [2, 9259, 236764, 1217, 659, 611], 'attention_mask': [1,1,1,1,1,1]}
# input_ids    → the numbers representing each word/token
# attention_mask → tells model which tokens to pay attention to (1=yes, 0=ignore)

# Get the token IDs only (as a list)
input_tokens = tokenizer("Hello, how are you?")["input_ids"]
print(input_tokens)
# Output: [2, 9259, 236764, 1217, 659, 611, 236881]


# -----------------------------------------------
# STEP 7: Import model class for text generation
# AutoModelForCausalLM = Auto model for "Causal Language Modeling"
# Causal = predicts the NEXT word based on previous words
# (This is exactly how ChatGPT/Gemma works!)
# -----------------------------------------------
from transformers import AutoModelForCausalLM

# Load the model (downloads the AI brain - may take a few minutes)
model = AutoModelForCausalLM.from_pretrained(model_name)


# -----------------------------------------------
# STEP 8: Reload model with bfloat16 for efficiency
# - bfloat16 = a lighter data format (uses less memory)
# - Normal format (float32) uses 2x more RAM/GPU memory
# - bfloat16 makes it faster and lighter with almost no quality loss
# -----------------------------------------------
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    dtype=torch.bfloat16   # Load in memory-efficient format
)


# -----------------------------------------------
# STEP 9: Create a Text Generation Pipeline
# - pipeline() = a simple ready-to-use tool
# - Combines model + tokenizer in one object
# - You just give it text → it returns generated text
# -----------------------------------------------
from transformers import pipeline

gen_pipeline = pipeline(
    "text-generation",    # Task type: we want to generate text
    model=model,          # The Gemma model we loaded
    tokenizer=tokenizer   # The tokenizer we loaded
)


# -----------------------------------------------
# STEP 10: Generate Text!
# - Give it any starting text (called a "prompt")
# - max_new_tokens = how many new words to generate (25 here)
# -----------------------------------------------
output = gen_pipeline("Hey there", max_new_tokens=25)

# Print the generated text
print(output)
# Output: [{'generated_text': "Hey there! I'm just a friendly AI assistant. How can I help you today? 😊"}]


# -----------------------------------------------
# BONUS: Generate with a custom prompt
# -----------------------------------------------
my_prompt = "Explain what is artificial intelligence in simple words"
result = gen_pipeline(my_prompt, max_new_tokens=100)
print(result[0]["generated_text"])   # Print only the text part


# ============================================================
# QUICK SUMMARY:
# 1. Install transformers library
# 2. Set HuggingFace token (for model access)
# 3. Load Tokenizer (text → numbers)
# 4. Load Model (the AI brain - Gemma 3)
# 5. Create Pipeline (easy wrapper for generation)
# 6. Generate text with any prompt!
# ============================================================