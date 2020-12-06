from pysubparser import parser
import sys

learned = [
    '好',
    '谢谢',
    '你',
    '我',
    '什么'
]

sentence_count = {}

for filename in sys.argv[1:]:
    subtitles = parser.parse(filename)

    for subtitle in subtitles:
        # skip known expressions
        if subtitle.text not in learned:
            sentence_count[subtitle.text] = sentence_count.get(subtitle.text, 0) + 1

sorted_sentences = sorted(sentence_count.items(), key=lambda kv: kv[1])

for w, count in sorted_sentences[-21:-1]:
    print(w + " -> " + str(count))