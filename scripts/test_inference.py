from mlx_lm import load, generate

print("Loading model...")
model, tokenizer = load("mlx-community/LFM2-8B-A1B-4bit")

print("Generating prompt...")
prompt = "Write a story about Einstein"
messages = [{"role": "user", "content": prompt}]

prompt = tokenizer.apply_chat_template(
    messages, add_generation_prompt=True
)

print("Starting generation...")
text = generate(model, tokenizer, prompt=prompt, verbose=True)
print(text)
