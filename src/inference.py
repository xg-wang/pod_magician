from modal import gpu, method
from modal.cls import ClsMixin

from .common import (
    MODEL_PATH,
    generate_prompt,
    output_vol,
    stub,
    VOL_MOUNT_PATH,
    pod_model_path,
)


@stub.cls(
    gpu=gpu.A100(memory=20),
    network_file_systems={VOL_MOUNT_PATH: output_vol},
)
class OpenLlamaModel(ClsMixin):
    def __init__(self, pod: str):
        import sys

        import torch
        from peft import PeftModel
        from transformers import LlamaForCausalLM, LlamaTokenizer

        self.pod = pod
        CHECKPOINT = pod_model_path(self.pod)

        load_8bit = False
        device = "cuda"

        self.tokenizer = LlamaTokenizer.from_pretrained(MODEL_PATH)

        print("### Load pretrained")
        model = LlamaForCausalLM.from_pretrained(
            MODEL_PATH,
            load_in_8bit=load_8bit,
            torch_dtype=torch.float16,
            device_map="auto",
        )

        print("### Peft load pretrained")
        model = PeftModel.from_pretrained(
            model,
            CHECKPOINT,
            torch_dtype=torch.float16,
        )

        # unwind broken decapoda-research config
        model.config.pad_token_id = self.tokenizer.pad_token_id = 0  # unk
        model.config.bos_token_id = 1
        model.config.eos_token_id = 2

        # if not load_8bit:
        #     model.half()  # seems to fix bugs for some users.

        print("### Model eval")
        model.eval()
        if torch.__version__ >= "2" and sys.platform != "win32":
            model = torch.compile(model)
        self.model = model
        self.device = device
        print("### OpenLlamaModel ready")

    @method()
    def generate(
        self,
        input_prompt: str,
        max_new_tokens=128,
        **kwargs,
    ) -> str:
        import torch
        from transformers import GenerationConfig

        prompt = generate_prompt(self.pod, input_prompt)
        print(f"### Generated prompt\n{prompt}")
        inputs = self.tokenizer(prompt, return_tensors="pt")
        input_ids = inputs["input_ids"].to(self.device)
        # tokens = self.tokenizer.convert_ids_to_tokens(input_ids[0])
        # print(tokens)
        generation_config = GenerationConfig(
            **kwargs,
        )
        with torch.no_grad():
            print("### Go")
            generation_output = self.model.generate(
                input_ids=input_ids,
                generation_config=generation_config,
                return_dict_in_generate=True,
                output_scores=True,
                max_new_tokens=max_new_tokens,
            )

        s = generation_output.sequences[0]
        output = self.tokenizer.decode(s)
        print(f"### Raw output\n{output}")
        return output.split("### Response:")[1].strip()


@stub.local_entrypoint()
def main(pod: str):
    input_prompts = [
        "Balancing AI safety and exploiting capabilities",
        "How powerful will GPT-5 be",
        "What is a typical day of an AI researcher like",
        "What is the meaning of life",
    ]
    model = OpenLlamaModel.remote(pod)
    for input_prompt in input_prompts:
        print(f"### Input: {input_prompt}")
        response = model.generate(
            input_prompt,
            do_sample=True,
            temperature=0.3,
            top_p=0.85,
            top_k=40,
            num_beams=1,
            max_new_tokens=6000,
            repetition_penalty=1.2,
        )
        print("### Response")
        print(response)
