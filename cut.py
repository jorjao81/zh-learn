from pydub import AudioSegment
from pysubparser import parser
import sys
import re
from pysubparser.util import time_to_millis

to_extract = [
"永不凋谢",
"不应该呀", 
"好的",  
"他发烧了" 
"你吃完饭赶紧回家去", 
"不用了",
"吃药", 
"小顾", 
"秋风起", 
"喂", 
"下雪了", 
"给", 
"没有", 
"怎么了", 
"司徒末"

]


audio_filename = sys.argv[1]
subtitle_filename = sys.argv[2]


def extract(input, subtitle):
    start = time_to_millis(subtitle.start) - 100
    end = time_to_millis(subtitle.end) + 400

    print(subtitle.text + " " + str(start) + " to " +  str(end))

    cut = song[start:end]
    cut.export("out/" + subtitle.text + "_" + str(subtitle.index) + ".mp3", format="mp3")


song = AudioSegment.from_mp3(audio_filename)
subtitles = parser.parse(subtitle_filename)

i = 0
for subtitle in subtitles:
    i += 1
    if subtitle.text in to_extract:
        extract(song, subtitle)



