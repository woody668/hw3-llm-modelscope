import os
import torch
from transformers import AutoTokenizer, AutoModel

os.environ["TOKENIZERS_PARALLELISM"] = "false"
torch.set_num_threads(8)

model_name = "/mnt/data/chatglm3-6b"

questions = [
    "请说出以下两句话区别在哪里？1、冬天：能穿多少穿多少 2、夏天：能穿多少穿多少",
    "请说出以下两句话区别在哪里？单身狗产生的原因有两个，一是谁都看不上，二是谁都看不上",
    "他知道我知道你知道他不知道吗？这句话里，到底谁不知道？",
    "明明明明明白白白喜欢他，可她就是不说。这句话里，明明和白白谁喜欢谁？",
    "领导：你这是什么意思？小明：没什么意思。意思意思。领导：你这就不够意思了。小明：小意思，小意思。领导：你这人真有意思。小明：其实也没有别的意思。领导：那我就不好意思了。小明：是我不好意思。请问：以上“意思”分别是什么意思？"
]

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    trust_remote_code=True
)

print("Loading model...")
model = AutoModel.from_pretrained(
    model_name,
    trust_remote_code=True,
    torch_dtype="auto",
    low_cpu_mem_usage=True
).eval()

print("Model loaded.\n")

for i, question in enumerate(questions, 1):
    print("=" * 80)
    print(f"问题 {i}: {question}")
    print("-" * 80)

    response, history = model.chat(tokenizer, question, history=[])
    print(response)
    print()
