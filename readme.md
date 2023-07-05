## Prepare data

```sh
yt-dlp -x --audio-format 'mp3' -o input_data.mp3 -- 'https://www.youtube.com/watch?v=<v_id>'
ffmpeg -i ./input_data.mp3 -ar 16000 -ac 1 -c:a pcm_s16le ./input_data.wav
# whisper.cpp
./main -m models/ggml-medium.en.bin -f ~/<path_to>/input_data.wav > data/input_data.txt
```
