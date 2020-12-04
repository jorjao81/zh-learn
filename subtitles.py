from pysubparser import parser
import jieba
import sys


word_count = {}
sentence_count = {}

for filename in sys.argv[1:]:
    subtitles = parser.parse(filename)

    for subtitle in subtitles:
        sentence_count[subtitle.text] = sentence_count.get(subtitle.text, 0) + 1

        seg_list = jieba.cut(subtitle.text, cut_all=False)
        
        for word in seg_list:
            word_count[word] = word_count.get(word, 0) + 1


sorted_words = sorted(word_count.items(), key=lambda kv: kv[1])

for w, count in sorted_words:
    print(w + " -> " + str(count))


sorted_sentences = sorted(sentence_count.items(), key=lambda kv: kv[1])

for w, count in sorted_sentences:
    print(w + " -> " + str(count))
