import os
import streamlit as st
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

st.title("🦙 LlamaIndex + Ollama Cloud Production")

# 1. Force the API key validation check
if "OLLAMA_API_KEY" in st.secrets:
    os.environ["OLLAMA_API_KEY"] = st.secrets["OLLAMA_API_KEY"]
else:
    st.error("🔑 Missing OLLAMA_API_KEY in Streamlit Cloud Secrets dashboard!")
    st.stop()

# 2. Point to Ollama's Universal Cloud API Gateway
# Explicitly setting base_url prevents LlamaIndex from checking localhost
CLOUD_GATEWAY = "https://ollama.com/api"

# 3. Configure the Remote LLM
Settings.llm = Ollama(
    model="qwen3-coder-next:cloud",
    base_url=CLOUD_GATEWAY,  # <-- Critical parameter change
    temperature=0.8,
    context_window=16000,
    request_timeout=6030.0
)

# 4. Configure Remote Embeddings
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text:cloud",
    base_url=CLOUD_GATEWAY,  # <-- Critical parameter change
    request_timeout=6000
)

# --- App Interface ---
user_query = st.text_input("Ask your cloud-hosted developer model:")
if user_query:
    with st.spinner("Streaming response from Ollama Cloud infrastructure..."):
        try:
            response = Settings.llm.complete(user_query)
            st.markdown("### Output Result:")
            st.write(str(response))
        except Exception as e:
            st.error(f"Execution Error: {e}")
