import os
from langchain_community.document_loaders import TextLoader, UnstructuredExcelLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE_URL = (
    os.getenv("OPENAI_API_BASE_URL")
    or os.getenv("OPENAI_API_BASE")
    or "https://openai.vocareum.com/v1"
)

DATA_FOLDER = "documents"
VECTOR_DB_PATH = "customersupport_faiss_index"

documents = []

for file in os.listdir(DATA_FOLDER):
    file_path = os.path.join(DATA_FOLDER, file)
    try:
        if file.endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
            documents.extend(loader.load())
            print("filename = ", file)
        elif file.endswith(".xlsx"):
            loader = UnstructuredExcelLoader(file_path, mode="elements")
            documents.extend(loader.load())
            print("filename = ", file)
    except Exception as e:
        print(f"Error loading {file}: {e}")

print(f"Loaded {len(documents)} document objects.")

if not documents:
    raise ValueError("No documents were loaded. Check dependencies and input files.")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

chunks = text_splitter.split_documents(documents)
print(f"Split documents into {len(chunks)} chunks.")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=OPENAI_API_KEY,
    base_url=OPENAI_API_BASE_URL
)

vectorstore = FAISS.from_documents(chunks, embeddings)
vectorstore.save_local(VECTOR_DB_PATH)

print("Customer support knowledge base created and saved to disk.")
