from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

load_dotenv()

# 获取当前文件的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "introduction.txt")

loader = TextLoader(file_path)
docs = loader.load()

zhipuai_api_key = os.getenv("ZHIPUAI_API_KEY")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200
)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma(
    collection_name="ai_learning",
    embedding_function=ZhipuAIEmbeddings(
        api_key=zhipuai_api_key
        ),
    persist_directory="vectordb"
)
vectorstore.add_documents(splits)
documents = vectorstore.similarity_search("专栏的作者是谁？")
print(documents)
