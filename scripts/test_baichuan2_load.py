import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig

os.environ["TOKENIZERS_PARALLELISM"] = "false"
torch.set_num_threads(8)

model_path = "/mnt/data/Baichuan2-7B-Chat"

print("Loading tokenizer...", flush=True)
tokenizer = AutoTokenizer.from_pretrained(
    model_path,
    use_fast=False,
    trust_remote_code=True
)

print("Loading model...", flush=True)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    trust_remote_code=True,
    torch_dtype="auto",
    low_cpu_mem_usage=True,
    device_map="cpu"
).eval()

try:
    model.generation_config = GenerationConfig.from_pretrained(model_path)
except Exception as e:
    print("GenerationConfig failed:", repr(e), flush=True)

print("Model loaded.", flush=True)

question = "请说出以下两句话区别在哪里？1、冬天：能穿多少穿多少 2、夏天：能穿多少穿多少"
messages = [{"role": "user", "content": question}]

print("Question:", question, flush=True)
print("Answer:", flush=True)
response = model.chat(tokenizer, messages)
print(response, flush=True)
