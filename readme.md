# Pod Magician 🧙

## Why?

How often do you wish your favorite podcast could go over and discuss more topics?

## How it works

### Overview

1. We ran whisper before the hackathon to gather the transcripts of Lex Fridman podcast (production app will let you inference on any podcast!).
2. We finetune the transcripts dataset.
3. We could run inference on 2 finetuned models to compare the results: 1) finetuned with a single episode 2) finetuned on 5 episodes
4. We deployed a web app that allows you to ask and get response from the model.

### Dataset

### Finetune

Finetuning is performed on [OpenLLaMA](https://github.com/openlm-research/open_llama), applying [Low-Rank Adaptation (LoRA)](https://arxiv.org/abs/2106.09685), a [parameter-efficient fine-tuning technique](https://huggingface.co/blog/peft). We ran the training on A100 via [Modal](https://www.modal.com)

## Demo!
