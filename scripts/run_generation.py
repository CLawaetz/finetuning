import argparse
from mlx_lm import load, generate

def test_character(model_path, adapter_path, char_name, race, char_class, trait, situation):
    print(f"\nLoading model from: {model_path}")
    if adapter_path:
        print(f"Loading adapter from: {adapter_path}")
        model, tokenizer = load(model_path, adapter_path=adapter_path)
    else:
        model, tokenizer = load(model_path)

    system_prompt = f"You are playing the role of {char_name}. You are a {race} {char_class} who is {trait}. Reply in character with no out-of-character text."
    user_prompt = f"The Game Master says: \"{situation}\"\n\nHow do you react?"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    print("\n--- Input Format ---")
    print(f"System: {system_prompt}")
    print(f"User: {user_prompt}")
    print("--------------------\n")

    prompt = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True
    )

    print("Generating response...\n")
    text = generate(model, tokenizer, prompt=prompt, verbose=True)
    return text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test D&D Character Generation with LoRA")
    parser.add_argument("--model", type=str, default="mlx-community/LFM2-8B-A1B-4bit", help="Base model path")
    parser.add_argument("--adapter-path", type=str, default="adapters/", help="Path to LoRA adapters (leave empty to test base model)")
    
    # Character kwargs
    parser.add_argument("--name", type=str, default="Thogar", help="Character name")
    parser.add_argument("--race", type=str, default="Half-Orc", help="Character race")
    parser.add_argument("--char-class", type=str, default="Barbarian", help="Character class")
    parser.add_argument("--trait", type=str, default="protective but quick to anger", help="Character personality trait")
    
    # Situation
    parser.add_argument("--situation", type=str, default="A mimic disguised as a treasure chest suddenly bites your hand.", help="The scenario from the GM")

    args = parser.parse_args()

    # Pass args to the main function
    test_character(
        model_path=args.model,
        adapter_path=args.adapter_path,
        char_name=args.name,
        race=args.race,
        char_class=args.char_class,
        trait=args.trait,
        situation=args.situation
    )
