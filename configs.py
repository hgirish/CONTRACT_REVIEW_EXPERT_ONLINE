import os
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding


CLOUD_BASE_URL = "https://ollama.com"
LOCAL_BASE_URL = "http://localhost:11434"

# Paths for persisting indexes
POLICIES_INDEX_PATH = "data/persistence/policies_index"
CONTRACTS_INDEX_PATH = "data/persistence/contracts_index"
REPORTS_INDEX_PATH = "data/persistence/reports_index"


def configure_ollama():
    """
    Configure the Ollama LLM and embeddings at runtime.

    Auto-detects environment:
    - Local: Uses local Ollama URL + OllamaEmbedding
    - Streamlit Cloud: Uses cloud Ollama URL + GoogleGenAIEmbedding
    """
    try:
        import streamlit as st
    except ImportError:
        raise RuntimeError(
            "Streamlit is required to configure Ollama in this app.")

    # Detect if running on Streamlit Cloud by checking for Google API key
    google_api_key = os.environ.get(
        "GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")

    if google_api_key:
        # Streamlit Cloud mode: Use cloud Ollama + Google embeddings
        _configure_cloud_mode(st, google_api_key)
    else:
        # Local mode: Use local Ollama + Ollama embeddings
        _configure_local_mode(st)


def _configure_cloud_mode(st, google_api_key: str):
    """Configure for Streamlit Cloud deployment."""
    from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
    # Get Ollama API key for cloud authentication
    ollama_api_key = os.environ.get(
        "OLLAMA_API_KEY") or st.secrets.get("OLLAMA_API_KEY")
    if not ollama_api_key:
        st.error(
            "🔑 Missing OLLAMA_API_KEY in Streamlit Cloud Secrets!")
        st.stop()

    os.environ["OLLAMA_API_KEY"] = ollama_api_key
    headers = {"Authorization": f"Bearer {ollama_api_key}"}

    # Cloud LLM configuration
    Settings.llm = Ollama(
        model="qwen3-coder-next:cloud",
        base_url=CLOUD_BASE_URL,
        temperature=0.8,
        context_window=16000,
        request_timeout=6030.0,
        headers=headers,
    )

    # Cloud embedding configuration
    Settings.embed_model = GoogleGenAIEmbedding(
        model_name="gemini-embedding-2-preview",
        api_key=google_api_key,
        timeout=6000,
    )

    st.sidebar.info("☁️ Running on Streamlit Cloud")


def _configure_local_mode(st):
    """Configure for local development with local Ollama instance."""
    # Local LLM configuration
    Settings.llm = Ollama(
        model="qwen3-coder-next:cloud",
        base_url=LOCAL_BASE_URL,
        temperature=0.8,
        context_window=4096,
        request_timeout=120.0,
    )

    # Local embedding configuration
    Settings.embed_model = OllamaEmbedding(
        model_name="nomic-embed-text",
        base_url=LOCAL_BASE_URL,
        embed_batch_size=10,
    )

    st.sidebar.info("🏠 Running locally with Ollama")
