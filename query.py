# Import modules
import qdrant_client
from llama_index.core import VectorStoreIndex, ServiceContext
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.qdrant import QdrantVectorStore
from langchain_community.embeddings import OllamaEmbeddings

from llama_index.core import Settings

import tiktoken

Settings.tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo").encode
Settings.llm = Ollama(model="llama2")
Settings.embed_model = OllamaEmbeddings(model="llama2:latest")
# Create Qdrant client and vector store
client = qdrant_client.QdrantClient(path="./qdrant_data")
vector_store = QdrantVectorStore(client=client, collection_name="manual")

# Initialize Ollama and ServiceContext
# llm = Ollama(model="llama2")
# service_context = ServiceContext.from_defaults(llm=llm, embed_model="local")

# Create VectorStoreIndex and query engine with a similarity threshold of 20
index = VectorStoreIndex.from_vector_store(vector_store=vector_store)# , service_context=service_context)
query_engine = index.as_query_engine(similarity_top_k=20,streaming=True)

# Perform a query and print the response
response = query_engine.query("How do i configure a basic keycloak instance on nixos?")
# print(response)
response.print_response_stream()
