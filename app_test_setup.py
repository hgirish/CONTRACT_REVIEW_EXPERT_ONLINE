import os
import streamlit as st
from llama_index.core import Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding

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

# 4. Setup Remote Embeddings with Google GenAI
google_api_key = os.environ.get(
    "GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
if google_api_key:
    Settings.embed_model = GoogleGenAIEmbedding(
        model_name="gemini-embedding-2-preview",
        api_key=google_api_key,
        timeout=6000,
    )
else:
    st.error(
        "🔑 Missing GOOGLE_API_KEY in Streamlit Cloud Secrets dashboard or environment for Google embeddings!"
    )
    st.stop()

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
