# 文档智能问答系统 (RAG) 

## 项目简介
本项目基于大语言模型（LLM）构建文档智能问答系统，支持用户上传 PDF 文档后进行内容检索与问答。系统采用 **RAG（检索增强生成）** 方案提升回答准确性，并通过 **Agent 工作流** 实现多步骤任务处理，用于学习资料辅助与知识整理场景。

---

## 主要工作
- 设计文档问答产品核心功能，包括文档上传、知识点提取、智能问答等用户交互流程  
- 基于 **LangChain** 实现 PDF 文档解析、文本切分及向量化处理  
- 使用 **FAISS** 完成语义检索模块  
- 通过 **LLM API** 实现生成模块，并优化 Prompt 结构，使输出条理清晰（总结 + 分点）  
- 基于 **LangGraph** 对问答流程进行拆分（检索 / 生成），提升系统结构清晰度与可扩展性  
- 协助完成前后端联调（React + Python），验证系统在实际场景中的可用性

---

## 技术栈
- Python
- LangChain
- LangGraph
- LLM API
- FAISS（基础使用）
- React
- Git

---

## 项目结构示例
rag-project/
├─ app.py # Flask 服务入口
├─ rag_core.py # 核心逻辑：PDF 解析、向量化、问答
├─ requirements.txt # 项目依赖
├─ README.md # 项目说明
├─ static/ # 前端静态资源
├─ templates/ # 前端模板
└─ .gitignore

---

## 安装与运行

1. 克隆仓库
```bash
git clone https://github.com/你的用户名/rag-project.git
cd rag-project
```
2. 创建并激活虚拟环境
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```
3. 安装依赖
```bash
pip install -r requirements.txt
```
4. 启动 Flask 服务
```bash
python app.py
```
5. 打开浏览器访问
```bash
http://127.0.0.1:5000
```
---
### 使用说明
- 上传 PDF 文件
- 系统自动解析并构建向量库
- 提问系统会基于 PDF 内容生成回答
- 请勿上传敏感信息或大文件到 GitHub
- API Key 等敏感信息请放在 .env 文件中，并添加到 .gitignore