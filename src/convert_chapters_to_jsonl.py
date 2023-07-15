import os
import pathlib
import json

CHAPTERS_OUTPUT_DIR=pathlib.Path(__file__).parent.parent / "data" / "chapters" / "367_Sam_Altman_L_Guz73e6fw"
JSONL_OUTPUT_PATH=pathlib.Path(__file__).parent.parent / "data" / "finetune_dataset" / "367_Sam_Altman_L_Guz73e6fw"


def main():
    os.makedirs(JSONL_OUTPUT_PATH, exist_ok=True)
    jsonl_lines: list[str] = []

    for root, dirs, files in os.walk(CHAPTERS_OUTPUT_DIR):
        for file in files:
            chapter_name = file.split("__")[1].split(".txt")[0]
            content = open(os.path.join(root, file)).read()
            jsonl_lines.append(json.dumps({"pod": "Lex Friedman Podcast", "input": chapter_name, "output": content}) + "\n")

    with open(JSONL_OUTPUT_PATH / "data.json", 'w') as fh:
        fh.writelines(jsonl_lines)

if __name__ == '__main__':
    main()
