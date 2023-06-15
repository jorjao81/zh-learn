#from pysubparser import parser
import jieba
import sys
import csv
import hanzidentifier
import re
import random


tsv_file = open("Chinese.txt")
read_tsv = csv.reader(tsv_file, delimiter="\t")

words = {}
characters = {}

for row in read_tsv:
    w = re.sub(r"\s+", "", row[1])
    # w = row[1]
    if len(w) > 0 and hanzidentifier.is_simplified(w):
        if len(w) == 1:
            characters[w] = 0
        elif len(w) < 5:
            words[w] = 0

tsv_file = open("skritter-export.tsv")
read_tsv = csv.reader(tsv_file, delimiter="\t")

skritter = {}

for row in read_tsv:
    if len(row) < 2:
        continue
    w = re.sub(r"\s+", "", row[1])
    # w = row[1]
    if len(w) > 0 and hanzidentifier.is_simplified(w):
        if len(w) == 1:
            skritter[w] = 0

print("Words: {}".format(len(words)) )
print("Chars Anki: {}".format(len(characters)))
print("Chars Skritter: {}".format(len(skritter)))

print("\nWords in skritter not in Anki")
for ch in skritter.keys():
    if ch not in characters.keys():
        print(ch)


missing_chars = {}

for k in words.keys():
    for ch in k:
        if ch not in characters.keys():
            missing_chars[ch] = missing_chars.get(ch, 0) + 1


print("\nMissing chars in Anki: {}".format(len(missing_chars)))

sorted_missing = sorted(missing_chars.items(), key=lambda kv: kv[1])

for w, count in sorted_missing[-21:-1]:
    print(w + " -> " + str(count))


missing_chars_skritter = {}

for k in words.keys():
    for ch in k:
        if ch in characters.keys(): # ignore stuff not in Anki, we want to add to Anki first always
            if ch not in skritter.keys():
                missing_chars_skritter[ch] = missing_chars_skritter.get(ch, 0) + 1


print("\nMissing chars in Skritter: {}".format(len(missing_chars_skritter)))

sorted_missing = sorted(missing_chars_skritter.items(), key=lambda kv: kv[1])

for w, count in sorted_missing[-21:-1]:
    print(w + " -> " + str(count))



tsv_file = open("HSK4.txt")
read_tsv = csv.reader(tsv_file, delimiter="\t")

hsk = {}

for row in read_tsv:
    w = row[0]
    hsk[w] = 0


missing_words_hsk = {}

random.seed(1984)

for w in hsk.keys():
    if w not in characters.keys():
        if w not in words.keys():
            missing_words_hsk[w] = random.randrange(0, 1024*1024)


print("\nMissing words HSK: {}".format(len(missing_words_hsk)))

sorted_missing = sorted(missing_words_hsk.items(), key=lambda kv: kv[1])

for w, count in sorted_missing[-41:-1]:
    print(w)
