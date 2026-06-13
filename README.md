# 📋 Contract Review Expert

An AI-powered contract analysis tool that performs risk analysis and compliance checks using LlamaIndex workflows. The application auto-detects the deployment environment and adjusts configurations accordingly.

## ✨ Features

- **Risk Analysis**: Identifies potential risks and liabilities in contracts
- **Compliance Check**: Compares contracts against company policies and guidelines
- **Policy Management**: Upload and manage company policies as reference documents
- **Contract Management**: Upload contracts for analysis with version tracking
- **Chat Interface**: Interactive Q&A about contract terms, risks, and compliance
- **Report Generation**: Detailed analysis reports with sourced insights
- **Dual Environment Support**: Automatically adapts to local or cloud deployment

## 🚀 Quick Start

### Local Development

1. **Install dependencies**:

   ```bash
   uv sync
   ```

2. **Ensure Ollama is running locally**:

   ```bash
   ollama serve
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

The app will automatically detect local mode and use:

- **LLM**: Local Ollama (`llama2`)
- **Embeddings**: Local Ollama (`nomic-embed-text`)
- **Base URL**: `http://localhost:11434`

### Streamlit Cloud Deployment

1. **Set environment variables in Streamlit Cloud Secrets**:

   ```
   OLLAMA_API_KEY = <your-ollama-cloud-api-key>
   GOOGLE_API_KEY = <your-google-genai-api-key>
   ```

2. **Deploy**:
   - Connect your repository to Streamlit Cloud
   - App auto-detects cloud mode via `GOOGLE_API_KEY` presence
   - Uses cloud Ollama + Google embeddings

## 🔧 Environment Configuration

The application includes **automatic environment detection** in `configs.py`:

### Local Mode (Default)

Triggered when `GOOGLE_API_KEY` is **not** present:

```python
# LLM: Local Ollama
Settings.llm = Ollama(
    model="llama2",
    base_url="http://localhost:11434"
)

# Embeddings: Local Ollama
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    base_url="http://localhost:11434"
)
```

### Cloud Mode (Streamlit Cloud)

Triggered when `GOOGLE_API_KEY` is present in environment/secrets:

```python
# LLM: Cloud Ollama with authentication
Settings.llm = Ollama(
    model="qwen3-coder-next:cloud",
    base_url="https://ollama.com",
    headers={"Authorization": f"Bearer {OLLAMA_API_KEY}"}
)

# Embeddings: Google GenAI
Settings.embed_model = GoogleGenAIEmbedding(
    model_name="gemini-embedding-2-preview",
    api_key=GOOGLE_API_KEY
)
```

## 📦 Project Structure

```
.
├── app.py                          # Main Streamlit app entry point
├── configs.py                      # LLM and embedding configuration
├── contracts.py                    # Contract upload and analysis UI
├── policies.py                     # Policy management UI
├── reports.py                      # Report viewing interface
├── chat.py                         # Chat/Q&A interface
├── analysis.py                     # Risk and compliance analysis logic
├── contract_analysis_workflow.py   # LlamaIndex workflow orchestration
├── utils.py                        # Utility functions
├── data/
│   ├── contracts/                 # Uploaded contracts
│   ├── policies/                  # Uploaded policies
│   ├── reports/                   # Generated analysis reports
│   └── persistence/               # Index cache (git-ignored)
├── .gitignore
└── pyproject.toml
```

## 🔑 Required Secrets

### Local Development

No secrets required if running local Ollama.

### Streamlit Cloud

| Variable         | Purpose                     | Source                                          |
| ---------------- | --------------------------- | ----------------------------------------------- |
| `OLLAMA_API_KEY` | Ollama Cloud authentication | [ollama.com](https://ollama.com)                |
| `GOOGLE_API_KEY` | Google GenAI embeddings     | [Google AI Studio](https://aistudio.google.com) |

## 🛠️ Workflow

### Analysis Pipeline

1. User uploads contract and policies
2. `ContractAnalysisWorkflow` orchestrates parallel analysis:
   - **Risk Analysis**: LLM queries policy index against contract
   - **Compliance Check**: LLM compares contract against internal policies
3. Reports saved to `data/reports/`
4. User can view report and ask follow-up questions via chat

### Data Flow

```
Contract Upload
    ↓
ContractAnalysisWorkflow
    ├→ perform_risk_analysis()
    │  └→ Query policies_index with contract text
    └→ perform_compliance_check()
       └→ Compare contract against policies
    ↓
Generate Report
    ↓
Chat Interface (per contract)
```

## 🧠 Key Technologies

- **LlamaIndex**: Document indexing and retrieval
- **Streamlit**: Web UI framework
- **Ollama**: Local/cloud LLM inference
- **Google GenAI**: Cloud embeddings (Streamlit Cloud mode)

## 📝 Notes

- **Persistence**: Embedding indexes are cached in `data/persistence/` but not versioned (git-ignored) to avoid conflicts between local and cloud embeddings
- **Chat Context**: Each contract maintains separate chat history using Streamlit session state
- **Async Workflow**: Analysis runs asynchronously to prevent UI blocking
- **Error Handling**: Graceful fallbacks if embedding or LLM calls fail

## 🐛 Troubleshooting

### Local Mode Issues

- **Ollama not found**: Ensure `ollama serve` is running on `http://localhost:11434`
- **Model not found**: Pull required models: `ollama pull llama2 nomic-embed-text`

### Cloud Mode Issues

- **401 Unauthorized**: Check `OLLAMA_API_KEY` validity in Streamlit secrets
- **Embedding dimension mismatch**: Clear `data/persistence/` and rebuild indexes
- **Google API error**: Verify `GOOGLE_API_KEY` is active and has GenAI API enabled

### Clearing Indexes

If embedding models change, clear the cache:

```bash
rm -rf data/persistence/
```

Indexes will rebuild automatically on next analysis.

## 📄 License

Proprietary - Internal Use Only
