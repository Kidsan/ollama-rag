# Import modules
from llama_index.llms.ollama import Ollama
from pathlib import Path
import qdrant_client
from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.readers.file import HTMLTagReader
from llama_index.core import Settings
from langchain_community.embeddings import OllamaEmbeddings
import tiktoken

Settings.tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo").encode
Settings.llm = Ollama(model="llama2", temperature=0.2)
Settings.embed_model = OllamaEmbeddings(model="llama2:latest")

# Load JSON data
loader = HTMLTagReader()
documents = loader.load_data(Path('./docs/nixos.org/manual/nixos/stable/index.html'))

# Create Qdrant client and store
client = qdrant_client.QdrantClient(path="./qdrant_data")
vector_store = QdrantVectorStore(client=client, collection_name="manual")
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Initialize Ollama and ServiceContext
# llm = Ollama(model="llama2")
# service_context = ServiceContext.from_defaults(llm=llm , embed_model="local")

# Create VectorStoreIndex and query engine
index = VectorStoreIndex.from_documents(documents, show_progress=True, storage_context=storage_context)
query_engine = index.as_query_engine()

# Perform a query and print the response
# response = query_engine.query("How do I configure a basic keycloak instance on NixOS")
# print(response)
