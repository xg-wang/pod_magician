import os
import re

INPUT_DATA_TXT="./data/260_men_peter_atia.txt"
OUTPUT_DIR="./data/260_men_peter_atia"

# Chapter timestamps and titles
timestamps = {
    "0:00:00": "Intro",
    "0:01:18": "Mohit’s career path and interest in sexual medicine",
    "0:03:25": "The anatomy of the male genitalia",
    "0:05:06": "The prevalence of sexual dysfunction & impact on quality of life",
    "0:08:58": "Erectile dysfunction (ED): definition, diagnosis, pathophysiology",
    "0:13:41": "The history of medications to treat ED and the mechanisms of how they work",
    "0:18:21": "Relationship between aging & erectile dysfunction and Mohit's approach to treating patients",
    "0:29:14": "The impact of lifestyle on sexual health & the association between ED and cardiovascular disease",
    "0:37:52": "Causes and treatments for Peyronie’s Disease & penile fracture",
    "0:48:32": "The value of ultrasound for ED diagnosis and management strategies",
    "0:51:55": "Various treatment options for ED: injections, penile prosthesis",
    "0:59:38": "Priapism (prolonged erection)",
    "1:05:40": "Shockwave therapy as a treatment for ED",
    "1:11:46": "Stem cell therapy for ED",
    "1:15:48": "Platelet-rich plasma (PRP) injections as a treatment for ED",
    "1:18:36": "Premature ejaculation (PE): prevalence, pathophysiology, and treatment",
    "1:26:34": "Anorgasmia: causes and treatment",
    "1:31:52": "Sex hormones, impact of aging, symptoms of low T, & considerations for testosterone replacement therapy (TRT)",
    "1:44:49": "Methods for increasing endogenous testosterone",
    "2:00:03": "Testosterone replacement therapy: various forms of exogenous testosterone & weighing risk vs. reward",
    "2:11:03": "The physiology and purpose of testosterone and DHT, why some men feel fine even with “low” testosterone, personalized approaches to treating low T",
    "2:18:25": "Post-finasteride syndrome",
    "2:26:42": "The role of testosterone in prostate cancer and addressing the notion that TRT could increase risk",
    "2:38:29": "The effects of testosterone as an adjunct to therapy for estrogen-sensitive breast cancer in women",
    "2:40:08": "Resources for those looking for healthcare providers",
}

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
with open(INPUT_DATA_TXT, 'r') as transcript:
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

