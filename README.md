# zh-learn
Tools to help learning Chinese

# User provided files

Some scripts expect files in a specific format to be available in the same folder as the scripts.

## Chinese.txt: Anki Export

The `Chinese.txt` file should be a tsv file with the second column containing the simplified characters.

## skritter-export.tsv: Skritter export

This is just the word list exported from Skritter in tsv format.

# Scripts
## normalize_audio.py

Normalizes the volume of audio files. Useful for keeping your Anki audio at a similar loudness level.

## summary.py

Shows some useful information:

* Characters in Skritter not in Anki
* Missing chars in Anki: characters that appear in Anki Multi-Char words, but have not been added as a single character (by frequency).
* Missing chars in Skritter: same thing, but for Skritter
* Missing words HSK: words the HSK level (hardcode to 3) not included in Anki yet (random).

Requires `Chinese.txt` anki export and `skritter-export.tsv` to exist.

## words.py

Given a subtitle file in .srt format, shows the words *not in the users current vocabulary* present in the subtitle,
by frequency order. Useful for pre-study.

Requires `Chinese.txt`
