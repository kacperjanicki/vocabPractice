from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from datasets import load_dataset
""" sample usage:
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("./llama3-finetuned")
tokenizer = AutoTokenizer.from_pretrained("./llama3-finetuned")
prompt = '{"word": "kot", "native": "pl", "foreign": "en"}\n'
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=128)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
"""

"""
    attaching INIT_PROMPT to every translation prompt causes long waiting times
    Instead, I decided to train the model with 500 examples of good responses. 
    prompt:
    You are a multilingual dictionary dataset generator.
    Your task is to generate exactly 500 single-line JSON objects, each representing a dictionary-style translation entry.
    Each object must contain two fields:
    - "prompt": a JSON string request that includes a word and language pair
    - "completion": a JSON string response containing a semantically correct and useful dictionary entry for the word
    ### Format:
    {"prompt": "{\"word\": \"<word_in_native>\", \"native\": \"<xx>\", \"foreign\": \"<yy>\"}", 
    "completion": "{\"translation\": \"<translation_in_foreign>\", 
                    \"meaning\": \"<accurate_dictionary_definition_in_native>\", 
                    \"type\": \"<part_of_speech_in_native>\", 
                    \"synonyms\": [\"syn1\", \"syn2\", \"syn3\"], 
                    \"examples\": [\"Example 1 in foreign\", \"Example 2 in foreign\", \"Example 3 in foreign\"]}"}
    ### Rules:
    1. The "word" must always be in the native language and selected from a realistic base list of ~100 common European words.
    2. The "meaning" must be a real dictionary-style explanation of the word in the native language.
    - Do not use generic definitions.
    - It must directly explain the actual meaning of the given word.
    3. The "type" (part of speech) must be correct for the word, and expressed in the native language.
    4. The "translation" must be a real and precise translation of the word into the foreign language.
    5. "synonyms" must be three real synonyms in the native language.
    6. "examples" must be three meaningful example sentences in the foreign language using the translated word naturally and correctly.
    7. Use diverse language pairs across popular European languages:
    - Examples: pl–en, en–es, fr–de, de–it, es–pl, etc.
    - Use ISO 639-1 codes, and make sure native ≠ foreign.
    8. Every combination of word + language pair must be unique across the dataset.
    ### Output constraints:
    - Output exactly 500 lines.
    - Each line must be a valid JSON object (not an array), as shown above.
    - Do not include any explanations, headers, summaries, or comments.
    - Each line must be parseable and standalone.
    💡 Focus on semantic quality:
    - All fields must logically relate to the given word.
    - Meaning, type, and synonyms must all match the actual word.
    - Examples must be proper sentences in the foreign language using the translation.
    Begin generating now. Format only as described above.
"""

data_file = "dictionary_dataset.json"
model_name = "meta-llama/Meta-Llama-3-8B"

model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

dataset = load_dataset("json", data_files={"train": data_file})

def preprocess(example):
    return {
        "text": example["prompt"] + "\n" + example["completion"]
    }

tokenized_dataset = dataset["train"].map(
    preprocess,
    remove_columns=dataset["train"].column_names
).map(
    lambda e: tokenizer(e["text"], truncation=True, padding="max_length", max_length=512),
    batched=True
)

training_args = TrainingArguments(
    output_dir="./llama3-finetuned",
    per_device_train_batch_size=1,
    num_train_epochs=3,
    save_steps=50,
    logging_steps=10,
    fp16=True,
    learning_rate=2e-5
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset
)

trainer.train()
trainer.save_model("./llama3-finetuned")
