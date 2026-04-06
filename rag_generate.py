from langchain_openai import ChatOpenAI

# ========= API开关 =========
USE_LLM =True   # 🔥 你可以随时开关

# ========= Prompt构建 =========
def build_prompt(context, query):

    prompt = f"""
你是一个专业的文档问答助手，请基于提供的内容回答问题：

【回答要求】
1️⃣ 先用一句话总结核心结论  
2️⃣ 再用2-4条分点说明  
3️⃣ 内容必须严格基于资料，不允许编造  
4️⃣ 表达要清晰、有条理  

【资料内容】
{context}

【用户问题】
{query}
"""

    return prompt


# ========= 生成回答 =========
def generate_answer(state):
    query = state["query"]
    context = state["context"]

    return {
        "answer": "（调试模式）\n" + context[:200]
    }

