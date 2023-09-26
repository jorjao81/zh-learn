from pysubparser import parser
import sys


for filename in sys.argv[1:]:
    subtitles = parser.parse(filename)

    outputFilename = filename + ".txt"
    output = open(outputFilename, "w")
    for subtitle in subtitles:
        output.write("- " + subtitle.text + "\n")

    print("Wrote " + outputFilename)
    output.close()