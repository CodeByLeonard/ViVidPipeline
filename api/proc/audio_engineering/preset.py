# Currently manual speed preset, need to extract to preset.txt later
# 105% is the optimal value for @ClipVerseRookie
speed_preset = 0.95 * (1+(1-0.9872)) * 1.011 # = 0.93884

# ALL FILE LOCATIONS ARE NOW HARDCODED
# FILE LOCATIONS: "files/original.mkv", "files/clip.mp4"
# FILE LOCATIONS: "tmp/eng.mp3", "tmp/ger.mp3", "tmp/clip.mp3"
original = "files/original.mkv"
clip = "files/clip.mp4"
mono_eng = "tmp/eng.mp3"
mono_ger = "tmp/ger.mp3"
mono_clip = "tmp/clip.mp3"

# MAIN_MAPPER
cutoff = 0.2
start_find_duration = 2 + cutoff
end_find_duration = 1
next_find_duration = 1