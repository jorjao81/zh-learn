from pysubparser import parser
import jieba
import sys

word_count = {}

learned = [
    '好',
    '你',
    '我',
    '什么',
    '了',
    '不',
    '好',
    '说',
    '的',
    '啊',
    '吧',
    '是',
    '吗',
    '就',
    '那',
    '去',
    '都', '我们', '呢',
    '顾未易', # gu wei yi
    '这', '吃', '走', '他', '给', '怎么', '在', '想', '也', '还',
    '要', '没有', '一下', '来', '有', '你们', '跟', '不是', '快', '你在干吗', '干吗'

]


for filename in sys.argv[1:]:
    subtitles = parser.parse(filename)

    for subtitle in subtitles:
        seg_list = jieba.cut(subtitle.text, cut_all=False)
        
        for word in seg_list:
            if word not in learned:
                word_count[word] = word_count.get(word, 0) + 1


sorted_words = sorted(word_count.items(), key=lambda kv: kv[1])

for w, count in sorted_words[-101:-1]:
    print(w + " -> " + str(count))
