# 大语言模型部署体验

本仓库记录了一次在 ModelScope CPU Notebook 环境中部署并测试开源大语言模型的过程。项目保留了可复现的运行脚本、问答输出和关键截图，不包含模型权重文件。

## 项目内容

- 在 CPU 环境中本地加载并运行 3 个中文对话模型。
- 使用同一组中文问题测试模型在双关理解、歧义消解、嵌套逻辑和多义词解释上的表现。
- 保存每个模型的终端输出和运行截图，方便查看和复核。

## 环境信息

| 项目 | 配置 |
| --- | --- |
| 平台 | ModelScope Notebook |
| 计算资源 | CPU，8 核 32GB |
| 推理方式 | 本地推理 |
| Python | 3.11 |
| PyTorch | CPU 版本 |

环境截图见：[screenshots/01_environment.png](screenshots/01_environment.png)

## 测试模型

| 模型 | 本地路径 | 运行脚本 |
| --- | --- | --- |
| Qwen-7B-Chat | `/mnt/data/Qwen-7B-Chat` | [scripts/run_qwen_cpu.py](scripts/run_qwen_cpu.py) |
| ChatGLM3-6B | `/mnt/data/chatglm3-6b` | [scripts/run_chatglm3_cpu.py](scripts/run_chatglm3_cpu.py) |
| Baichuan2-7B-Chat | `/mnt/data/Baichuan2-7B-Chat` | [scripts/run_baichuan2_cpu.py](scripts/run_baichuan2_cpu.py) |

> 模型权重体积较大，未提交到仓库。运行前需要在 ModelScope 环境中下载到上表对应路径。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 下载模型

```bash
cd /mnt/data

git clone https://www.modelscope.cn/qwen/Qwen-7B-Chat.git
git clone https://www.modelscope.cn/ZhipuAI/chatglm3-6b.git
git clone https://www.modelscope.cn/baichuan-inc/Baichuan2-7B-Chat.git
```

如果磁盘空间不足，建议一次只下载并运行一个模型。

### 3. 运行测试

进入本仓库目录后执行：

```bash
python scripts/run_qwen_cpu.py | tee outputs/qwen_result.txt
python scripts/run_chatglm3_cpu.py | tee outputs/chatglm3_result.txt
python scripts/run_baichuan2_cpu.py | tee outputs/baichuan2_7b_chat_result.txt
```

## 测试问题

1. 请说出以下两句话区别在哪里？1、冬天：能穿多少穿多少 2、夏天：能穿多少穿多少
2. 请说出以下两句话区别在哪里？单身狗产生的原因有两个，一是谁都看不上，二是谁都看不上
3. 他知道我知道你知道他不知道吗？这句话里，到底谁不知道？
4. 明明明明明白白白喜欢他，可她就是不说。这句话里，明明和白白谁喜欢谁？
5. 领导：你这是什么意思？小明：没什么意思。意思意思。领导：你这就不够意思了。小明：小意思，小意思。领导：你这人真有意思。小明：其实也没有别的意思。领导：那我就不好意思了。小明：是我不好意思。请问：以上“意思”分别是什么意思？

## 结果索引

| 模型 | 输出文本 | 运行截图 |
| --- | --- | --- |
| Qwen-7B-Chat | [outputs/qwen_result.txt](outputs/qwen_result.txt) | [screenshots/03_qwen_qa_result.png](screenshots/03_qwen_qa_result.png) |
| ChatGLM3-6B | [outputs/chatglm3_result.txt](outputs/chatglm3_result.txt) | [screenshots/05_chatglm3_qa_result.png](screenshots/05_chatglm3_qa_result.png) |
| Baichuan2-7B-Chat | [outputs/baichuan2_7b_chat_result.txt](outputs/baichuan2_7b_chat_result.txt) | [screenshots/07_baichuan2_7b_chat_qa_result.png](screenshots/07_baichuan2_7b_chat_qa_result.png) |

## 截图说明

| 文件 | 内容 |
| --- | --- |
| [01_environment.png](screenshots/01_environment.png) | Python、PyTorch、ModelScope、磁盘和内存环境 |
| [02_qwen_git_clone.png](screenshots/02_qwen_git_clone.png) | Qwen-7B-Chat 下载记录 |
| [03_qwen_qa_result.png](screenshots/03_qwen_qa_result.png) | Qwen-7B-Chat 问答结果 |
| [04_chatglm3_git_clone.png](screenshots/04_chatglm3_git_clone.png) | ChatGLM3-6B 下载记录 |
| [05_chatglm3_qa_result.png](screenshots/05_chatglm3_qa_result.png) | ChatGLM3-6B 问答结果 |
| [06_baichuan2_7b_chat_git_clone.png](screenshots/06_baichuan2_7b_chat_git_clone.png) | Baichuan2-7B-Chat 下载记录 |
| [07_baichuan2_7b_chat_qa_result.png](screenshots/07_baichuan2_7b_chat_qa_result.png) | Baichuan2-7B-Chat 问答结果 |

## 仓库结构

```text
.
├── README.md
├── requirements.txt
├── scripts/
│   ├── run_qwen_cpu.py
│   ├── run_chatglm3_cpu.py
│   └── run_baichuan2_cpu.py
├── outputs/
│   ├── qwen_result.txt
│   ├── chatglm3_result.txt
│   └── baichuan2_7b_chat_result.txt
└── screenshots/
    ├── 01_environment.png
    ├── 02_qwen_git_clone.png
    ├── 03_qwen_qa_result.png
    ├── 04_chatglm3_git_clone.png
    ├── 05_chatglm3_qa_result.png
    ├── 06_baichuan2_7b_chat_git_clone.png
    └── 07_baichuan2_7b_chat_qa_result.png
```

## 注意事项

- 本仓库只保存实验代码、输出和截图，不保存模型权重。
- 脚本中的模型路径为 ModelScope Notebook 环境路径，若在其他环境运行，需要同步修改路径。
- CPU 推理速度较慢，模型加载和生成结果都需要等待较长时间。
