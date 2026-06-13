import os
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding


CLOUD_BASE_URL = "https://ollama.com"

# Paths for persisting indexes
POLICIES_INDEX_PATH = "data/persistence/policies_index"
CONTRACTS_INDEX_PATH = "data/persistence/contracts_index"
REPORTS_INDEX_PATH = "data/persistence/reports_index"


def configure_ollama():
    """Configure the Ollama LLM and embeddings at runtime."""
    try:
        import streamlit as st
    except ImportError:
        raise RuntimeError(
            "Streamlit is required to configure Ollama in this app.")

    if "OLLAMA_API_KEY" in st.secrets:
        api_key = st.secrets["OLLAMA_API_KEY"]
        os.environ["OLLAMA_API_KEY"] = api_key
    else:
        st.error("🔑 Missing OLLAMA_API_KEY in Streamlit Cloud Secrets dashboard!")
        st.stop()

    Settings.llm = Ollama(
        model="qwen3-coder-next:cloud",
        base_url=CLOUD_BASE_URL,
        temperature=0.8,
        context_window=16000,
        request_timeout=6030.0,
        additional_kwargs={"headers": {"Authorization": f"Bearer {api_key}"}},
    )

    Settings.embed_model = OllamaEmbedding(
        model_name="nomic-embed-text:cloud",
        base_url=CLOUD_BASE_URL,
        request_timeout=6000,
        additional_kwargs={"headers": {"Authorization": f"Bearer {api_key}"}},
    )
