import os
import pathlib
import re

CURR_PATH = str(pathlib.Path(__file__).parent.parent)
INPUT_TRANSCRIPT_TXT= CURR_PATH + "/data/yt_captions/386_Marc_Andreessen.txt"
INPUT_OUTLINE_TXT= CURR_PATH + "/data/yt_outlines/386_Marc_Andreessen.txt"
OUTPUT_DIR= CURR_PATH + "/data/chapters/386_Marc_Andreessen"


"""
{'0:00': 'Introduction', '1:06': 'Google Search', '8:54': 'LLM training', '21:25': 'Truth' ...}
"""
def parse_file(file_name):
    chapter_dict = {}

    with open(file_name, 'r') as file:
        for line in file:
            match = re.match(r'(\d+:\d+:\d+|\d+:\d+)\s-\s(.+)', line.strip())
            if match:
                time, chapter = match.groups()
                chapter_dict[time] = chapter

    return chapter_dict


def main():
    timestamps = parse_file(INPUT_OUTLINE_TXT)

    # Convert timestamps to seconds for easier comparison
    timestamps_in_seconds = {
        sum(int(x) * 60 ** i for i, x in enumerate(reversed(key.split(":")))): value
        for key, value in timestamps.items()
    }
    """
    [(0, 'Introduction'), (66, 'Google Search'), (534, 'LLM training'),...]
    """
    sorted_timestamps_in_seconds = sorted(timestamps_in_seconds.items())


    def get_chapter_with_index(index):
        return sorted_timestamps_in_seconds[index][1]

    # Read transcript file
    with open(INPUT_TRANSCRIPT_TXT, 'r') as transcript:
        chapter_index = 1
        old_chapter_name = get_chapter_with_index(0)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        caption_dict = {}
        current_time = None
        #i = 0
        for line in transcript:
            # debug
            # i += 1
            # if i > 30:
            #     break

            line = line.strip()

            if line in timestamps.values():
                # write old chapter to file
                if len(caption_dict) == 0:
                    old_chapter_name = line
                    continue

                print(f"LOG: chapter {chapter_index} - {old_chapter_name}")
                old_chapter_file = open(f'{OUTPUT_DIR}/{chapter_index}__{old_chapter_name}.txt', 'w')
                for _, content in caption_dict.items():
                    old_chapter_file.write(content + '\n')
                old_chapter_file.close()

                # new chapter
                chapter_index += 1
                old_chapter_name = line
                caption_dict= {}
            elif re.match(r"\d+:\d+(:\d+)?", line):
                current_time = line
            else:
                caption_dict[current_time] = line

        # write last chapter to file
        print(f"LOG: chapter {chapter_index} - {old_chapter_name}")
        old_chapter_file = open(f'{OUTPUT_DIR}/{chapter_index}__{old_chapter_name}.txt', 'w')
        for _, content in caption_dict.items():
            old_chapter_file.write(content + '\n')
        old_chapter_file.close()


if __name__ == '__main__':
    main()