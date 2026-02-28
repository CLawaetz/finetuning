# mlx-lm Finetuning Harness

A structured repository for fine-tuning LLMs on Apple Silicon using `mlx-lm`. 
This workspace helps organize datasets, adapters, merged models, and configurations.

## Directory Structure
- `data/`: Place your `train.jsonl`, `valid.jsonl`, and `test.jsonl` here.
- `adapters/`: Location where the fine-tuned LoRA adapter weights are saved.
- `models/`: Location to save fused/merged models or quantized weights.
- `configs/`: YAML configuration files (e.g., `lora_config.yaml`) for reproducibile training.
- `scripts/`: Custom data preparation or utility scripts.

## Setup

1. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   make install
   # or: pip install -r requirements.txt
   ```

## Usage

You can control fine-tuning via the [`Makefile`](Makefile) and [`configs/lora_config.yaml`](configs/lora_config.yaml).

### 1. Data Preparation
Format your data into JSONL files: `data/train.jsonl`, `data/valid.jsonl`.
Each line should be a JSON object with a `text` field (for raw text completion) or standard conversational roles if using chat templates.
Example:
```json
{"text": "<s>[INST] What is the capital of France? [/INST] The capital of France is Paris. </s>"}
```

### 2. Fine-Tuning
Review and edit `configs/lora_config.yaml` to set your base model and hyperparameters, then run:

```bash
make train
```
*Note: If `valid.jsonl` exists in `data/`, it will output validation loss periodically.*

### 3. Evaluation
To evaluate your current adapter on the validation set:
```bash
make eval
```

### 4. Generation / Chat (Testing the Roleplay)
I have created a custom script specifically for testing your D&D conversational agents.

**To test your Fine-Tuned Model (uses `adapters/`):**
```bash
python scripts/run_generation.py --situation "The king demands you kneel."
```

**To test the Original Base Model (ignores `adapters/` for comparison):**
```bash
python scripts/run_generation.py --adapter-path "" --situation "The king demands you kneel."
```

You can also test brand new character combinations on the fly:
```bash
python scripts/run_generation.py \
    --name "Orik" \
    --race "Dwarf" \
    --char-class "Cleric" \
    --trait "drunk, constantly complaining about his knees" \
    --situation "A shadow demon erupts from the ancient tome!"
```

### 5. Fusing the Model
Once satisfied, fuse the LoRA adapters back into the base model to create a standalone model:
```bash
make fuse
```
The fused model defaults to saving in `models/fused-model`.

### 6. Serving the Model (API)
Because this is a 4-bit MLX model, it runs blazingly fast natively on your Mac but cannot be easily converted to a generic GGUF file for Ollama.

Instead, `mlx-lm` has a built-in server that perfectly mimics the OpenAI API format (just like Ollama!). 
To serve your custom D&D model directly to your other applications, run:
```bash
make serve
```

Your other program can now connect to your fine-tuned model instantly at:
`http://localhost:8080/v1/chat/completions`