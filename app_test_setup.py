import os
import streamlit as st
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

st.title("🦙 LlamaIndex + Ollama Cloud Production")

# 1. Fetch and store the Ollama API Key securely
api_key = os.environ.get("OLLAMA_API_KEY") or st.secrets.get("OLLAMA_API_KEY")
if api_key:
    os.environ["OLLAMA_API_KEY"] = api_key
else:
    st.error(
        "🔑 Missing OLLAMA_API_KEY in Streamlit Cloud Secrets dashboard or environment!")
    st.stop()

headers = {"Authorization": f"Bearer {api_key}"}

# 2. Point to the root cloud URL (LlamaIndex automatically adds /api internally)
CLOUD_BASE_URL = "https://ollama.com"

# 3. Setup the Remote LLM with header authorization injection
Settings.llm = Ollama(
    model="qwen3-coder-next:cloud",
    base_url=CLOUD_BASE_URL,
    temperature=0.8,
    context_window=16000,
    request_timeout=6030.0,
    # Adds proper cloud auth
    headers=headers,
)

# 4. Setup Remote Embeddings with identical token authentication
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text:cloud",
    base_url=CLOUD_BASE_URL,
    request_timeout=6000,
    # Adds proper cloud auth
    client_kwargs={"headers": headers},
)

# --- Basic UI Inference Check ---
user_query = st.text_input("Ask your cloud-hosted developer model:")
if user_query:
    with st.spinner("Streaming response from Ollama Cloud infrastructure..."):
        try:
            response = Settings.llm.complete(user_query)
            st.markdown("### Output Result:")
            st.write(str(response))
        except Exception as e:
            st.error(f"Execution Error: {e}")
