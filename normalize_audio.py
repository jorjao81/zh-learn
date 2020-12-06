from pydub import AudioSegment
import sys

TARGET_DBFS=-15.0

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

for filename in sys.argv[1:]:
    if not filename.endswith("_normalized.mp3"):
        sound = AudioSegment.from_mp3(filename)
        normalized_sound = match_target_amplitude(sound, TARGET_DBFS)
        new_filename = filename[0:-4] + "_normalized" ".mp3"
        print(new_filename)
        normalized_sound.export(new_filename, format="mp3")
