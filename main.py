from rag_core import load_pdf, split_documents, build_vectorstore, retrieve_context
from rag_generate import generate_answer


def main():
    print("🚀 RAG智能问答系统启动")

    # 1️⃣ 加载PDF
    documents = load_pdf("test.pdf")

    # 2️⃣ 切分
    chunks = split_documents(documents)

    # 3️⃣ 向量库
    vectorstore = build_vectorstore(chunks)

    while True:
        query = input("\n请输入问题（exit退出）：")

        if query.lower() == "exit":
            break

        # 4️⃣ 检索
        context = retrieve_context(vectorstore, query)

        # 5️⃣ 生成
        answer = generate_answer(query, context)

        print("\n📌 回答：\n")
        print(answer)


if __name__ == "__main__":
    main()
