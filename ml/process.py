import json
import os
import sys

import pandas
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


from joblib import dump, load
clf = load('decision-tree.joblib')

def classify(line):
    bbox = line['boundingBox']
    fr = pandas.DataFrame([{'x1': bbox[0],  'y1': bbox[1], 'x2': bbox[2], 'y2': bbox[3], 'x3': bbox[4], 'y3': bbox[5], 'x4': bbox[6], 'y4': bbox[7]}])
    pred = clf.predict(fr)
    return pred[0]

termTitle = ""
seenTerm = []
for filename in sys.argv[1:]:
    firstTerminal = True
    print(filename)
    f = open(filename)
    j = json.load(f)

    lines = j['readResult']['pages'][0]['lines']

    for line in lines:
        c = classify(line)
        if c == 'terminal':
            if firstTerminal:
                firstTerminal = False
                if termTitle != line['content']:
                    # new terminal email
                    termTitle = line['content']
                    print("===========================")
                    print(line['content'])
                    print('--------------')
                    seenTerm = []
            else:
                if line['content'] not in seenTerm:
                    print(line['content'])
                    seenTerm.append(line['content'])


        print(line['content'] + " - " + c)

