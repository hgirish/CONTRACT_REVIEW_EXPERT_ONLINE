from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# Configure the LLM model
Settings.llm = Ollama(
    model="qwen3-coder-next:cloud",
    base_url="http://localhost:11434",
    temperature=0.8,
    context_window=16000,
    request_timeout=6030.0
)

# Configure the embedding model
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    base_url="http://localhost:11434",
    request_timeout=6000
)

# Paths for persisisting indexes
POLICIES_INDEX_PATH = "data/persistence/policies_index"
CONTRACTS_INDEX_PATH = "data/persistence/contracts_index"
REPORTS_INDEX_PATH = "data/persistence/reports_index"
