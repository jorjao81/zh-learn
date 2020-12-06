from pysubparser import parser
from pysubparser.util import time_to_millis
from pydub import AudioSegment

# find segments of conversation

import sys

FIVE_SECONDS = 5000

def get_segments(subtitles):
    segments = []

    prev_end = -1000000
    curr_segment = None

    for subtitle in subtitles:
        this_start = time_to_millis(subtitle.start)
        if this_start - prev_end > FIVE_SECONDS:
            if curr_segment != None:
                segments.append(curr_segment)
            curr_segment = []

        curr_segment.append(subtitle)

        prev_end = time_to_millis(subtitle.end)

    # append last segment
    segments.append(curr_segment)

    return segments

def print_segment(seg):
    print(seg[0].start)

    for sub in seg:
        print(sub.text)

    print(seg[-1].end)
    print("------------------------------------")
    print("Segment duration: " + str((time_to_millis(seg[-1].end) - time_to_millis(seg[0].start))/1000))
    print("====================================")


audio_filename = sys.argv[1]
subtitle_filename = sys.argv[2]

subtitles = parser.parse(subtitle_filename)
segments = get_segments(subtitles)

song = AudioSegment.from_mp3(audio_filename)

folder = "out/"
episode = "e01"
n = 1
for seg in segments:
    start = time_to_millis(seg[0].start) - 1000
    end = time_to_millis(seg[-1].end) + 1500

    cut = song[start:end]
    cut.export(folder + episode + "_seg" + str(n) + ".mp3", format="mp3")

    print("===== Segment " + str(n) + " ========")
    print_segment(seg)

    n += 1

