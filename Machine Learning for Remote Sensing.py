#tutorial from scikit-learn
import matplotlib.pyplot as plt
import time

from sklearn import datasets
from sklearn import svm

start = time.time()


#SVM to predict number 0-9 of hand written digit picture
#Features are inputs, Labels are known outputs
digits = datasets.load_digits()

"""
print digits.data
print digits.target
print digits.images[0]
"""

#gamma is learning rate, give and take b/t speed and accuracy in gradient descent, finding local minimum 
clf = svm.SVC(gamma=0.001, C=100)

#training the SVM ML classifier
z = 15
x,y = digits.data[:-z], digits.target[:-z]
#print len(digits.data)
clf.fit(x,y)

#predicting results for new data
print 'Prediction', clf.predict(digits.data[-z:])

end = time.time()
elapsed = end - start
print round(elapsed, 2), "seconds"


#display pictures that algorithm predicted to see if accurate
predVals = range(1, z+1)
predVals.reverse()

for i in predVals:
    plt.imshow(digits.images[-i], cmap=plt.cm.gray_r, interpolation="nearest")
    plt.show()


