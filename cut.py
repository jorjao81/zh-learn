from pydub import AudioSegment
from pysubparser import parser
import sys
import re
from pysubparser.util import time_to_millis



def to_milissecond(srt_time):
    ## 00:02:35,639
    components = re.split("[:,]", srt_time)

    hours = int(components[0])
    minutes = int(components[1])
    seconds = int(components[2])
    milisseconds = int(components[3])

    return (((hours * 60) + minutes) * 60 + seconds) * 1000 + milisseconds


audio_filename = sys.argv[1]
subtitle_filename = sys.argv[2]


def extract(input, subtitle):
    start = time_to_millis(subtitle.start) - 100
    end = time_to_millis(subtitle.end) + 400

    print(subtitle.text + " " + str(start) + " to " +  str(end))

    cut = song[start:end]
    cut.export("out/" + subtitle.text + ".mp3", format="mp3")


song = AudioSegment.from_mp3(audio_filename)
subtitles = parser.parse(subtitle_filename)

for subtitle in subtitles:
    extract(song, subtitle)



