# Import modules
from llama_index.llms.ollama import Ollama
from pathlib import Path
from llama_index.core import VectorStoreIndex
from llama_index.readers.file import HTMLTagReader
from llama_index.core import Settings
from llama_index.embeddings.ollama import OllamaEmbedding
import sentencepiece as spm

import os
import qdrant_client
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import StorageContext

# use the tokenizer for llama2
Settings.tokenizer = spm.SentencePieceProcessor().Encode
Settings.llm = Ollama(model="llama2:7b", temperature=0.1)
Settings.embed_model = OllamaEmbedding(model_name="llama2:7b")

# Load JSON data
loader = HTMLTagReader()
manual = loader.load_data(Path("./docs/nixos.org/manual/nixos/stable/index.html"))

# Create VectorStoreIndex and query engine
client = None
vector_store = None

if os.path.isdir("./qdrant_data/") == False:
    client = qdrant_client.QdrantClient(path="./qdrant_data")
    vector_store = QdrantVectorStore(client=client, collection_name="manual")
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    loader = HTMLTagReader()
    manual = loader.load_data(Path("./docs/nixos.org/manual/nixos/stable/index.html"))
    index = VectorStoreIndex.from_documents(
        manual, show_progress=True, storage_context=storage_context
    )

# Create Qdrant client and vector store
if client == None:
    client = qdrant_client.QdrantClient(path="./qdrant_data")

if vector_store == None:
    vector_store = QdrantVectorStore(client=client, collection_name="manual")

index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
query_engine = index.as_query_engine(similarity_top_k=20, streaming=True)

while True:
    response = query_engine.query(input(">>> "))
    response.print_response_stream()
    print("\n")
