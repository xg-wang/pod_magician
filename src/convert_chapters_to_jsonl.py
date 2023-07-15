import os
import pathlib
import json

DIR_NAMES = [
    "215_Wojciech_Zaremba",
    "299_Demis_Hassabis",
    "333_Andrej_Karpathy",
    "367_Sam_Altman_L_Guz73e6fw",
    "368_Eliezer_Yudkowsky",
    "371_Max_Tegmark",
    "381_Chris_Lattner",
    "386_Marc_Andreessen",
    ]
CHAPTERS_DIR_PREFIX = pathlib.Path(__file__).parent.parent / "data" / "chapters"
JSONL_OUTPUT_DIR_PREFIX = pathlib.Path(__file__).parent.parent / "data" / "finetune_dataset" / "LexFridman"


def main():
    os.makedirs(JSONL_OUTPUT_DIR_PREFIX, exist_ok=True)

    for dir_name in DIR_NAMES:

        jsonl_lines: list[str] = []
        dir_path = CHAPTERS_DIR_PREFIX / dir_name
        for root, dirs, files in os.walk(dir_path):
            # sort by chronological order for debugging purpose
            files.sort(key=lambda x: int(x.split("__")[0]))

            for file in files:
                chapter_name = file.split("__")[1].split(".txt")[0]
                content = open(os.path.join(root, file)).read()
                jsonl_lines.append(json.dumps({"pod": "Lex Fridman Podcast", "input": chapter_name, "output": content}) + "\n")

        with open(JSONL_OUTPUT_DIR_PREFIX / (dir_name + ".json"), 'w') as fh:
            fh.writelines(jsonl_lines)

if __name__ == '__main__':
    main()
