import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
print("Token carregado")

# Carregar o modelo sem quantização de bitsandbytes
model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.2",
    token=token
)
print("Modelo Instanciado")

tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2", token=token)
print("Tokenizador Instanciado")

# Definindo o prompt
prompt = "My favourite condiment is"

messages = [
    {"role": "user", "content": "What is your favourite condiment?"},
    {"role": "assistant", "content": "Well, I'm quite partial to a good squeeze of fresh lemon juice. It adds just the right amount of zesty flavour to whatever I'm cooking up in the kitchen!"},
    {"role": "user", "content": "Do you have mayonnaise recipes?"}
]
print("Prompt e mensagens Definidos")


# Aplicar o template de chat e mover para a CPU
model_inputs = tokenizer.apply_chat_template(messages, return_tensors="pt").to("cpu")
print("Aplicado Chat Template")

# Gerar IDs
with torch.no_grad():  # Desativar o cálculo de gradientes
    generated_ids = model.generate(model_inputs, max_new_tokens=100, do_sample=True)

# Decodificar a resposta
response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
print(response)