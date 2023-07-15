import os
import re

INPUT_TRANSCRIPT_TXT="./data/yt_transcripts/367_Sam_Altman_L_Guz73e6fw.txt"
INPUT_OUTLINE_TXT="./data/yt_outlines/367_Sam_Altman_L_Guz73e6fw.txt"
OUTPUT_DIR="./data/chapters/367_Sam_Altman_L_Guz73e6fw"


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
    sorted_timestamps_in_seconds = sorted(timestamps_in_seconds.items())

    def get_chapter(time_in_seconds):
        # Find the right chapter for the given time
        for i in range(1, len(sorted_timestamps_in_seconds)):
            if sorted_timestamps_in_seconds[i-1][0] <= time_in_seconds < sorted_timestamps_in_seconds[i][0]:
                return timestamps_in_seconds[sorted_timestamps_in_seconds[i-1][0]]
        return timestamps_in_seconds[sorted_timestamps_in_seconds[-1][0]]

    # Read transcript file
    with open(INPUT_TRANSCRIPT_TXT, 'r') as transcript:
        current_chapter_file = None
        current_chapter_name = None
        os.makedirs(OUTPUT_DIR)

        chapter_index = 1
        for line in transcript:
            # Extract timestamp
            match = re.match(r'\[(\d{2}:\d{2}:\d{2})\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\](.*)', line)
            if match:
                time_in_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(match.group(1).split(":"))))
                chapter_name = get_chapter(time_in_seconds)

                # If we're in a new chapter, open a new file
                if chapter_name != current_chapter_name:
                    if current_chapter_file:
                        current_chapter_file.close()
                        chapter_index += 1
                    current_chapter_name = chapter_name
                    current_chapter_file = open(f'{OUTPUT_DIR}/{chapter_index}__{current_chapter_name}.txt', 'w')

                # Write line to file
                if current_chapter_file:
                    current_chapter_file.write(match.group(2).strip() + '\n')

        if current_chapter_file:
            current_chapter_file.close()


if __name__ == '__main__':
    main()