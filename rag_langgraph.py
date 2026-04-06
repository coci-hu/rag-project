from typing import TypedDict
from langgraph.graph import StateGraph, END

# 👇 引入你已经写好的RAG函数
from rag_core import (
    load_pdf,
    split_documents,
    build_vectorstore,
    retrieve_context,
    generate_answer
)

# ========= 1. 定义 State =========
class RAGState(TypedDict):
    query: str
    context: str
    answer: str


# ========= 2. 初始化向量库（只执行一次） =========
print("🚀 初始化向量数据库...")

docs = load_pdf("test.pdf")   # ⚠️改成你的PDF名字
chunks = split_documents(docs)
vectorstore = build_vectorstore(chunks)


# ========= 3. 节点1：检索 =========
def retrieve_node(state: RAGState):
    query = state["query"]

    context = retrieve_context(vectorstore, query)

    print("📚 检索完成")

    return {
        "query": query,
        "context": context
    }


# ========= 4. 节点2：生成 =========
def generate_node(state: RAGState):
    print("🤖 生成答案中...")

    result = generate_answer(state)

    return {
        "answer": result["answer"]
    }


# ========= 5. 构建 Graph =========
graph = StateGraph(RAGState)

graph.add_node("retrieve", retrieve_node)
graph.add_node("generate", generate_node)

graph.set_entry_point("retrieve")

graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)

app = graph.compile()


# ========= 6. 运行 =========
def ask(query: str):
    result = app.invoke({
        "query": query
    })
    return result["answer"]

