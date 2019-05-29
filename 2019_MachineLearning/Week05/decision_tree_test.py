from sklearn.neighbors import KNeighborsClassifier
from sklearn import datasets
from sklearn.model_selection import GridSearchCV
import numpy as np

iris = datasets.load_iris()

X, y = iris.data, iris.target
print('Size of data :%s' % (X.shape, ))
print('Target value : %s' % np.unique(y))
print(X[0:10, :])
sample = [[6, 4, 6, 2],]

knn = KNeighborsClassifier(n_neighbors=10, weights='distance')
knn.fit(X,y)

predicted_value = knn.predict(sample)
print(knn.predict_proba(sample))
print(iris.target_names[predicted_value])

parameters = {'n_neighbors':(1, 3, 10), 'weights':('uniform', 'distance')}
knn_base = KNeighborsClassifier()
grid_search = GridSearchCV(cv=5, estimator=knn_base, param_grid=parameters, scoring='accuracy', n_jobs=5)
grid_search.fit(X, y)
print(grid_search)
print(grid_search.best_params_)
print(grid_search.cv_results_)
