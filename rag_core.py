import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

# ========= 1. PDF加载 =========
def load_pdf(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    print("✅ PDF加载完成")
    return documents


# ========= 2. 文本切分 =========
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)
    print(f"✅ 文本切分完成，共 {len(chunks)} 段")

    return chunks


# ========= 3. 向量库 =========
def build_vectorstore(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    texts = []
    metadatas = []

    for doc in chunks:
        if isinstance(doc.page_content, str) and doc.page_content.strip():
            texts.append(doc.page_content)
            metadatas.append(doc.metadata)

    print(f"✅ 清洗后文本数量: {len(texts)}")

    if len(texts) == 0:
        raise ValueError("❌ 没有可用文本")

    vectorstore = FAISS.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas
    )

    print("✅ 向量数据库构建完成")
    return vectorstore


# ========= 4. 检索 =========
def retrieve_context(vectorstore, query, k=3):
    docs = vectorstore.similarity_search(query, k=k)

    context = "\n".join([doc.page_content for doc in docs])

    return context



# ========= 5. 生成回答 =========
def generate_answer(state):
    query = state["query"]
    context = state["context"]

    prompt = f"""
你是一个专业的文档问答助手：

【内容】
{context}

【问题】
{query}
"""

    USE_LLM = False

    if not USE_LLM:
        return {
            "answer": "（调试模式）\n" + context[:200]
        }

    llm = ChatOpenAI(
        model="moonshot-v1-8k",
        temperature=0.3,
        openai_api_key=os.getenv("MOONSHOT_API_KEY"),
        openai_api_base=os.getenv("MOONSHOT_BASE_URL")
    )

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }
