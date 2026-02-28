.PHONY: train eval test generate fuse install

# Default variables (can be overridden from CLI)
MODEL ?= "mlx-community/LFM2-8B-A1B-4bit"
ADAPTER_PATH ?= "adapters/"
DATA_PATH ?= "data/"
CONFIG ?= "configs/lora_config.yaml"
PROMPT ?= "Hello, what is your name?"

install:
	pip install -r requirements.txt

# Run finetuning with configuration file
train:
	python -m mlx_lm lora --config $(CONFIG) --train

# Example to override the model and data path from command line directly
train-cli:
	python -m mlx_lm lora \
		--model $(MODEL) \
		--data $(DATA_PATH) \
		--train \
		--adapter-path $(ADAPTER_PATH) \
		--batch-size 4 \
		--lora-layers 16 \
		--iters 1000

# Evaluate the model against the validation set
eval:
	python -m mlx_lm lora \
		--model $(MODEL) \
		--adapter-path $(ADAPTER_PATH) \
		--data $(DATA_PATH) \
		--test \
		--iters 0

# Test the finetuned model against test.jsonl
test:
	python -m mlx_lm lora \
		--model $(MODEL) \
		--adapter-path $(ADAPTER_PATH) \
		--data $(DATA_PATH) \
		--test

# Generate a response using the adapter
generate:
	python -m mlx_lm.generate \
		--model $(MODEL) \
		--adapter-path $(ADAPTER_PATH) \
		--prompt "$(PROMPT)"

# Fuse the LoRA adapter into the base model and save to models/
fuse:
	python -m mlx_lm.fuse \
		--model $(MODEL) \
		--adapter-path $(ADAPTER_PATH) \
		--save-path models/fused-model
