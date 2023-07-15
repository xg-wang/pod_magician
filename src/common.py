from modal import Image, NetworkFileSystem, Stub, Mount
from typing import Optional
from pathlib import Path, PurePosixPath

VOL_MOUNT_PATH = Path("/vol")
_LOCAL_DATASET_PATH = Path("./data/finetune_dataset")
_MOUNTED_DATASET_PATH = PurePosixPath("/root/finetune_dataset")

MODEL_PATH = "/model"


def download_models():
    from transformers import LlamaForCausalLM, LlamaTokenizer

    model_name = "openlm-research/open_llama_13b"

    model = LlamaForCausalLM.from_pretrained(model_name)
    model.save_pretrained(MODEL_PATH)

    tokenizer = LlamaTokenizer.from_pretrained(model_name)
    tokenizer.save_pretrained(MODEL_PATH)


openllama_image = (
    Image.micromamba()
    .micromamba_install(
        "cudatoolkit=11.7",
        "cudnn=8.1.0",
        "cuda-nvcc",
        channels=["conda-forge", "nvidia"],
    )
    .apt_install("git")
    .pip_install(
        "accelerate==0.18.0",
        "bitsandbytes==0.37.0",
        "bitsandbytes-cuda117==0.26.0.post2",
        "datasets==2.10.1",
        "fire==0.5.0",
        "gradio==3.23.0",
        "peft @ git+https://github.com/huggingface/peft.git@e536616888d51b453ed354a6f1e243fecb02ea08",
        "transformers @ git+https://github.com/huggingface/transformers.git@a92e0ad2e20ef4ce28410b5e05c5d63a5a304e65",
        "torch==2.0.0",
        "torchvision==0.15.1",
        "sentencepiece==0.1.97",
    )
    .run_function(download_models)
)

stub = Stub(name="pod_magician", image=openllama_image)

output_vol = NetworkFileSystem.persisted(label="pod_magician_finetune_vol", cloud="gcp")

local_dataset_mount = Mount.from_local_dir(local_path=_LOCAL_DATASET_PATH, remote_path=_MOUNTED_DATASET_PATH)


def generate_prompt(pod: str, input: str, output=""):
    return f"""You are the podcast host of \"{pod}\", a podcast about AI technology and society. Below is an input example of a topic of the conversation. Write a response that appropriately fleshes out the topic into a deep discussion, which should be deep, thought provoking and interesting.

### Input:
{input}

### Response:
{output}"""


def pod_data_path(pod: str) -> PurePosixPath:
    return _MOUNTED_DATASET_PATH / pod / "data.json"


def pod_model_path(
    pod: str, checkpoint: Optional[str] = None
) -> Path:
    path = VOL_MOUNT_PATH / "data" / pod
    if checkpoint:
        path = path / checkpoint
    return path
