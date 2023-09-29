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

from sklearn.model_selection import cross_val_score
clf = SVC()
scores = cross_val_score(clf, x, y, cv=5)
print("SVC: %0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

from sklearn import tree
clf = tree.DecisionTreeClassifier()
scores = cross_val_score(clf, x, y, cv=5)
print("DecisionTree: %0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

from sklearn.neural_network import MLPClassifier
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
scores = cross_val_score(clf, x, y, cv=5)
print("MLPClassifier: %0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

from sklearn.ensemble import HistGradientBoostingClassifier
clf = HistGradientBoostingClassifier(max_iter=100)
scores = cross_val_score(clf, x, y, cv=5)
print("HistGradientBoostingClassifier: %0.2f accuracy with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

svc_model = SVC()

svc_model.fit(x_train, y_train)

y_predict = svc_model.predict(x_test)

from sklearn.metrics import classification_report, confusion_matrix
cm = np.array(confusion_matrix(y_test, y_predict, labels=["other", "mission", "subtitle", "terminal", "information"]))
print(cm)

confusion = pd.DataFrame(cm, index=["other", "mission", "subtitle", "terminal", "information"], columns=["pred other", "pred mission", "pred subtitle", "pred terminal", "pred information"])
print(confusion)


from joblib import dump, load
clf = tree.DecisionTreeClassifier()
clf.fit(x, y)

dump(clf, "decision-tree.joblib")

print(x[0:1])
