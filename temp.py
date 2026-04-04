import os

from huggingface_hub import hf_hub_download

hf_hub_download(
    repo_id="bartowski/Llama-3.2-3B-Instruct-GGUF",
    filename="Llama-3.2-3B-Instruct-Q4_K_M.gguf",
    local_dir="models",
    token=os.getenv("HF_TOKEN")
)