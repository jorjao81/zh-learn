from pysubparser import parser
import jieba
import sys
import csv


tsv_file = open("Chinese.txt")
read_tsv = csv.reader(tsv_file, delimiter="\t")

word_count = {}

ignore_list = [
    '》', '《'
]

for row in read_tsv:
    w = row[1]
    ignore_list.append(w)

for filename in sys.argv[1:]:
    subtitles = parser.parse(filename)

    for subtitle in subtitles:
        seg_list = jieba.cut(subtitle.text, cut_all=False)
        
        for word in seg_list:
            if word not in ignore_list:
                word_count[word] = word_count.get(word, 0) + 1


sorted_words = sorted(word_count.items(), key=lambda kv: kv[1])

for w, count in sorted_words[-101:-1]:
    print(w + " -> " + str(count))
