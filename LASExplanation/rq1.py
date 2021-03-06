from LIMEBAG import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
import pandas as pd
import os
import pkg_resources
"""
rq1) Can LIME be used to give summarized explanations on a group of individuals? 
"""

def main():
    file = pkg_resources.resource_filename('LASExplanation', 'camel-1.2.csv')
    #file = os.path.join(os.getcwd(), 'camel-1.2.csv')
    df = pd.read_csv(os.path.normpath(file))
    # demo using a software defect prediction dataset
    for i in range(0, df.shape[0]):
        if df.iloc[i, -1] > 0:
            df.iloc[i, -1] = 1
        else:
            df.iloc[i, -1] = 0
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05)
    sc = MinMaxScaler()
    X_train = pd.DataFrame(sc.fit_transform(X_train), columns=X_train.columns).copy()
    X_test = pd.DataFrame(sc.fit_transform(X_test), columns=X_train.columns).copy()
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)
    bag = LIMEBAG(clf=clf, y_train=y_train, X_test=X_test, X_train=X_train, K=1)
    # leave sensitive as none if the data has no fairness concerns
    for i in range(len(X_train.columns)):
        print('Index', i, ':', X_train.columns[i])
    ranks, rankvals = bag.explain()
    print("Feature importance ranks of all test data returned by LIMEBAG:")
    print(ranks)
    print("Feature importance weights of all test data returned by LIMEBAG:")
    print(rankvals)
    return

if __name__ == "__main__":
    main()
