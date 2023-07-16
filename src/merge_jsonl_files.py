import os
import pathlib
import json

JSONL_DIR_PREFIX = pathlib.Path(__file__).parent.parent / "data" / "finetune_dataset" / "LexFridman"

JSONL_OUTPUT_DIR = pathlib.Path(__file__).parent.parent / "data" / "finetune_dataset" / "Lex Fridman Podcast"

def merge_files(directory, output_file):
    with open(output_file, 'wb') as outfile:
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'rb') as infile:
                    outfile.write(infile.read())
                    outfile.write(b'\n')  # Add a newline after each file


os.makedirs(JSONL_OUTPUT_DIR, exist_ok=True)
merge_files(JSONL_DIR_PREFIX,  JSONL_OUTPUT_DIR / "data.json")

