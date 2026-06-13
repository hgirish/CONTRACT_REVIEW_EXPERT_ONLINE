import os
import streamlit as st
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

st.title("🦙 LlamaIndex + Ollama Cloud App")

# 1. Safely retrieve the API Key from Streamlit Secrets
# The underlying Ollama library automatically looks for OLLAMA_API_KEY
if "OLLAMA_API_KEY" in st.secrets:
    os.environ["OLLAMA_API_KEY"] = st.secrets["OLLAMA_API_KEY"]
else:
    st.error("Missing OLLAMA_API_KEY in Streamlit Secrets!")
    st.stop()

# 2. Configure the Cloud LLM model (Remove localhost base_url)
# The ':cloud' suffix tells Ollama to execute inference on remote cloud GPUs
Settings.llm = Ollama(
    model="qwen3-coder-next:cloud",
    temperature=0.8,
    context_window=16000,
    request_timeout=6030.0
)

# 3. Configure the Embedding model for Cloud
# For cloud applications, you should use the cloud-optimized variant
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text:cloud",
    request_timeout=6000
)

# --- Basic UI Test ---
user_query = st.text_input("Ask a coding question:")
if user_query:
    with st.spinner("Streaming from Ollama Cloud..."):
        response = Settings.llm.complete(user_query)
        st.markdown("### Response:")
        st.write(str(response))
