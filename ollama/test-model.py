from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("./llama3-finetuned")
tokenizer = AutoTokenizer.from_pretrained("./llama3-finetuned")

prompt = '{"word": "kot", "native": "pl", "foreign": "en"}\n'
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=128)

print(tokenizer.decode(outputs[0], skip_special_tokens=True))
