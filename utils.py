import configs
import os
from pathlib import Path
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.core.readers import SimpleDirectoryReader

# base_dir = os.path.dirname(__file__)
persist_dir = configs.POLICIES_INDEX_PATH


def save_file(uploaded_file, folder):
    Path(folder).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(folder, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def load_policies_index():
    index_file = os.path.join(persist_dir, "docstore.json")
    if os.path.exists(index_file):
        print("Loading existing policies index from persistence")
        storage_context = StorageContext.from_defaults(
            persist_dir=persist_dir)
        index = load_index_from_storage(storage_context)
    else:
        # os.path.join(base_dir, "data", "policies")
        policy_dir = "data/policies"
        print("No valid index found - rebuilding policies index...")
        reader = SimpleDirectoryReader(policy_dir)
        docs = reader.load_data()
        index = VectorStoreIndex.from_documents(docs)
        os.makedirs(persist_dir, exist_ok=True)
        index.storage_context.persist(persist_dir=persist_dir)
    return index


def load_report(report_path):
    with open(report_path, "r", encoding="utf-8") as f:
        return f.read()


def list_files(folder: str):
    return [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]


def list_reports():
    Path("data/reports").mkdir(parents=True, exist_ok=True)
    reports = {}
    for fname in os.listdir("data/reports"):
        if fname.endswith(".txt"):
            contract = fname.split("_")[0]
            reports.setdefault(contract, []).append(
                os.path.join("data/reports", fname))
    return reports
