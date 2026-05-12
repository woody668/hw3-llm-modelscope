# 大语言模型部署体验与横向对比分析

本仓库记录了在 ModelScope CPU Notebook 环境中部署并测试开源中文大语言模型的过程。实验分别运行 Qwen-7B-Chat、ChatGLM3-6B 和 Baichuan2-7B-Chat 三个模型，并使用同一组中文歧义理解问题进行横向比较。

仓库中保留了可复现的运行脚本、终端输出、部署截图、问答截图和实验报告，不包含模型权重文件。

## 实验路线

本实验采用 `transformers` 本地加载模型并进行问答推理的方式完成测试：

1. 在 ModelScope CPU Notebook 环境中准备 Python 依赖。
2. 将三个模型权重分别下载到 `/mnt/data` 下的对应目录。
3. 运行 `scripts/` 中的 Python 脚本加载 tokenizer 和模型。
4. 使用同一组 5 个中文语义理解问题进行测试。
5. 保存每个模型的终端输出和运行截图，并进行横向对比分析。

说明：课程参考资料中提供了 Intel Extension for Transformers / Neural Chat 的 chatbot 搭建流程，但本仓库实际实验路线是 CPU 环境下的本地模型推理，没有声称完成 INT4 量化或完整 chatbot 服务。

## 环境信息

| 项目     | 配置                |
| -------- | ------------------- |
| 平台     | ModelScope Notebook |
| 计算资源 | CPU，8 核 32GB      |
| 推理方式 | 本地加载模型推理    |
| Python   | 3.11                |
| PyTorch  | CPU 版本            |

环境截图见：[screenshots/01_environment.png](screenshots/01_environment.png)

## 测试模型

| 模型              | ModelScope 仓库                    | 本地路径                        | 运行脚本                                                  |
| ----------------- | ---------------------------------- | ------------------------------- | --------------------------------------------------------- |
| Qwen-7B-Chat      | `qwen/Qwen-7B-Chat`              | `/mnt/data/Qwen-7B-Chat`      | [scripts/run_qwen_cpu.py](scripts/run_qwen_cpu.py)           |
| ChatGLM3-6B       | `ZhipuAI/chatglm3-6b`            | `/mnt/data/chatglm3-6b`       | [scripts/run_chatglm3_cpu.py](scripts/run_chatglm3_cpu.py)   |
| Baichuan2-7B-Chat | `baichuan-inc/Baichuan2-7B-Chat` | `/mnt/data/Baichuan2-7B-Chat` | [scripts/run_baichuan2_cpu.py](scripts/run_baichuan2_cpu.py) |

模型权重体积较大，未提交到仓库。运行前需要在 ModelScope 环境中下载到上表对应路径。

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

三个脚本的基本流程相同：设置 CPU 线程数、加载 tokenizer、加载模型、遍历统一测试问题、输出回答并保存结果。

## 测试任务

本实验使用 5 个中文语义理解问题。它们不是普通知识问答，而是侧重考察模型对中文双关、歧义、复杂指代和多义词的理解能力。

| 编号 | 测试重点        | 问题内容                                                                           |
| ---- | --------------- | ---------------------------------------------------------------------------------- |
| 1    | 语境反转 / 双关 | 请说出以下两句话区别在哪里？1、冬天：能穿多少穿多少 2、夏天：能穿多少穿多少        |
| 2    | 句法歧义        | 请说出以下两句话区别在哪里？单身狗产生的原因有两个，一是谁都看不上，二是谁都看不上 |
| 3    | 多层逻辑嵌套    | 他知道我知道你知道他不知道吗？这句话里，到底谁不知道？                             |
| 4    | 中文分词与指代  | 明明明明明白白白喜欢他，可她就是不说。这句话里，明明和白白谁喜欢谁？               |
| 5    | 多义词解释      | 领导与小明对话中多次出现的“意思”分别是什么意思？                                 |

## 结果索引

| 模型              | 输出文本                                                                  | 问答截图                                                                                      |
| ----------------- | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Qwen-7B-Chat      | [outputs/qwen_result.txt](outputs/qwen_result.txt)                           | [screenshots/03_qwen_qa_result.png](screenshots/03_qwen_qa_result.png)                           |
| ChatGLM3-6B       | [outputs/chatglm3_result.txt](outputs/chatglm3_result.txt)                   | [screenshots/05_chatglm3_qa_result.png](screenshots/05_chatglm3_qa_result.png)                   |
| Baichuan2-7B-Chat | [outputs/baichuan2_7b_chat_result.txt](outputs/baichuan2_7b_chat_result.txt) | [screenshots/07_baichuan2_7b_chat_qa_result.png](screenshots/07_baichuan2_7b_chat_qa_result.png) |

## 横向对比摘要

| 测试维度       | Qwen-7B-Chat                                      | ChatGLM3-6B                                          | Baichuan2-7B-Chat                       |
| -------------- | ------------------------------------------------- | ---------------------------------------------------- | --------------------------------------- |
| 语境反转理解   | 第 1 题能识别冬夏语境下同一句式含义相反，表现较好 | 第 1 题将夏天解释为多穿衣服散热，理解错误            | 第 1 题同样误解夏天表达，表现较弱       |
| 句法歧义理解   | 第 2 题能意识到句子存在差异，但解释不够准确       | 第 2 题能部分解释“看不上别人 / 被别人看不上”的区别 | 第 2 题对歧义理解较弱，解释偏离题目     |
| 多层逻辑推理   | 第 3 题能重述逻辑结构，但没有明确回答谁不知道     | 第 3 题将句子判断为悖论，没有回答“谁不知道”        | 第 3 题能直接指出“他”不知道，表现较好 |
| 分词与指代消解 | 第 4 题回答过于笼统，没有准确区分明明和白白       | 第 4 题对“白白喜欢他”的关系判断较接近              | 第 4 题倾向于认为无法确定，表现较弱     |
| 多义词语境解释 | 第 5 题能说明“意思”有多种含义，但没有逐项对应   | 第 5 题只做泛化解释，缺少语境分析                    | 第 5 题尝试逐项解释，但准确性不足       |

总体来看，在本组中文歧义理解问题中，Qwen-7B-Chat 综合表现相对较好，ChatGLM3-6B 输出流畅但容易泛化，Baichuan2-7B-Chat 在个别逻辑问题上表现较好但整体较谨慎。该结论只反映本次小规模测试结果，不能直接代表模型在所有任务上的综合能力。

## 截图说明

| 文件                                                                              | 内容                                        |
| --------------------------------------------------------------------------------- | ------------------------------------------- |
| [01_environment.png](screenshots/01_environment.png)                                 | Python、PyTorch、ModelScope、磁盘和内存环境 |
| [02_qwen_git_clone.png](screenshots/02_qwen_git_clone.png)                           | Qwen-7B-Chat 下载记录                       |
| [03_qwen_qa_result.png](screenshots/03_qwen_qa_result.png)                           | Qwen-7B-Chat 问答结果                       |
| [04_chatglm3_git_clone.png](screenshots/04_chatglm3_git_clone.png)                   | ChatGLM3-6B 下载记录                        |
| [05_chatglm3_qa_result.png](screenshots/05_chatglm3_qa_result.png)                   | ChatGLM3-6B 问答结果                        |
| [06_baichuan2_7b_chat_git_clone.png](screenshots/06_baichuan2_7b_chat_git_clone.png) | Baichuan2-7B-Chat 下载记录                  |
| [07_baichuan2_7b_chat_qa_result.png](screenshots/07_baichuan2_7b_chat_qa_result.png) | Baichuan2-7B-Chat 问答结果                  |

## 实验报告

Word 实验报告保存在：

```text
report/hw3_2453619_薛毓哲.docx
```

报告中包含公开项目链接、部署截图、问答截图和横向对比分析。s

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
├── screenshots/
│   ├── 01_environment.png
│   ├── 02_qwen_git_clone.png
│   ├── 03_qwen_qa_result.png
│   ├── 04_chatglm3_git_clone.png
│   ├── 05_chatglm3_qa_result.png
│   ├── 06_baichuan2_7b_chat_git_clone.png
│   └── 07_baichuan2_7b_chat_qa_result.png
└── report/
    ├── hw3_2453619_薛毓哲.docx
    └── hw3_2453619_薛毓哲.pdf
```

## 注意事项

- 本仓库只保存实验代码、输出、截图和报告，不保存模型权重。
- 脚本中的模型路径为 ModelScope Notebook 环境路径，若在其他环境运行，需要同步修改路径。
- CPU 推理速度较慢，模型加载和生成结果都需要等待较长时间。
- 本实验测试问题数量有限，结果仅用于课程作业中的模型部署体验和中文语义理解横向比较。
