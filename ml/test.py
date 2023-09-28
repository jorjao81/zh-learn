import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

data = pd.read_csv('/Users/pauloschreiner/git/jorjao81/zh-learn/azure-ocr/training.csv', delimiter=',')

x = data.drop(["class", "content"], axis=1)
y = np.ravel(data['class'])

x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.2, random_state=50)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler().fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

from sklearn.svm import SVC
svc_model = SVC()

svc_model.fit(x_train, y_train)

y_predict = svc_model.predict(x_test)

from sklearn.metrics import classification_report, confusion_matrix
cm = np.array(confusion_matrix(y_test, y_predict, labels=["other", "mission", "subtitle"]))
print(cm)

confusion = pd.DataFrame(cm, index=["other", "mission", "subtitle"], columns=["pred other", "pred mission", "pred subtitle"])
print(confusion)

print(y_predict)
