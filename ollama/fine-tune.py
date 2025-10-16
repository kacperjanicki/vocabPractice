from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer, BitsAndBytesConfig
from datasets import load_dataset
import torch
import os


data_file = "training_data.jsonl"
model_name = "meta-llama/Meta-Llama-3-8B"


bnb_config = BitsAndBytesConfig(
    load_in_8bit=True,
    llm_int8_enable_fp32_cpu_offload=True,
    llm_int8_threshold=6.0
)


model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
    max_memory={
        0: "6GB",
        "cpu": "24GB"
    },
    torch_dtype=torch.float16,
    token=os.getenv("HF_TOKEN")
)

tokenizer = AutoTokenizer.from_pretrained(model_name, token=os.getenv("HF_TOKEN"))

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

tokenizer.padding_side = "right"


dataset = load_dataset("json", data_files={"train": data_file}, split="train")


def preprocess_function(examples):
    texts = []
    for prompt, completion in zip(examples["prompt"], examples["completion"]):
        texts.append(prompt + "\n" + completion)
    
    result = tokenizer(
        texts,
        truncation=True,
        padding="max_length",
        max_length=512,
        return_attention_mask=True
    )
    
    result["labels"] = result["input_ids"][:]
    
    return result


tokenized_dataset = dataset.map(
    preprocess_function,
    batched=True,
    remove_columns=dataset.column_names
)


training_args = TrainingArguments(
    output_dir="./llama3-finetuned",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    save_steps=50,
    logging_steps=10,
    fp16=True,
    learning_rate=2e-5,
    optim="paged_adamw_8bit",
    gradient_checkpointing=True,
    max_grad_norm=0.3,
    warmup_ratio=0.03
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset
)


trainer.train()
trainer.save_model("./llama3-finetuned")
tokenizer.save_pretrained("./llama3-finetuned")
