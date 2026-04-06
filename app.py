from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from rag_core import load_pdf, split_documents, build_vectorstore, retrieve_context
from rag_generate import generate_answer
from flask import send_from_directory

app = Flask(__name__)
CORS(app)

# 👉 模拟用户缓存
vectorstore_cache = {}

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

print("🚀 服务启动完成")

# ========= 1️⃣ 上传PDF =========
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "没有文件"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    print("📄 开始处理PDF...")

    documents = load_pdf(filepath)
    chunks = split_documents(documents)
    vectorstore = build_vectorstore(chunks)

    # 👉 简化：用固定user_id（后期可升级）
    user_id = "default"
    vectorstore_cache[user_id] = vectorstore

    print("✅ 向量库构建完成")

    return jsonify({"message": "上传成功"})


# ========= 2️⃣ 问答 =========
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query", "")
    user_id = "default"

    if user_id not in vectorstore_cache:
        return jsonify({"error": "请先上传PDF"}), 400

    vectorstore = vectorstore_cache[user_id]

    context = retrieve_context(vectorstore, query)

    result = generate_answer({
        "query": query,
        "context": context
    })

    return jsonify(result)

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

if __name__ == "__main__":
    app.run(debug=True)
