import cv2
import cv2.ml as ml
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import sys

from sklearn import svm, metrics
from sklearn.model_selection import KFold

PORO = 1

CLASS = {
    'b': 2,
    'f': 3,
    'i': 4
}

def slice_image(img, in_ground, half_window = 5):

    w,h = img.shape
    with open(in_ground) as ground_f:

        database = []

        for i, line in enumerate(ground_f):
            x,y,*clazz = line.strip().split(' ')
            x,y,clazz = int(x), int(y), CLASS[clazz[0]]  if len(clazz) else PORO

            # SVM require that matrix size is same for all elements into array
            if x < half_window or y < half_window or y + half_window > h or x + half_window > w:
                continue

            #Select ROI
            roi = img[max(x-half_window,0):min(x+half_window,w),max(y-half_window,0):min(y+half_window,h)]
            # print(roi.shape)
            # #Show ROI
            # cv2.imshow('image',roi)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            database.append((clazz,np.array(roi)))

        return database

    return []

if __name__ == '__main__':
    opt, *args = sys.argv[1:]

    if opt == 't' or opt == 'train':

        repo_in, repo_out = args

        dataset = {
            'label': [],
            'train': []
        }
        info = {
            'minutiae': {
                'iterations': 5,
                'fmt': 'jpg'
            },
            'pore': {
                'iterations': 1, #iterations
                'fmt': 'bmp' #file format
            }
        }
        tsamples = 0

        for keypoint in ['minutiae','pore']:

            repo = '{}{}/'.format(repo_in,keypoint)
            print('Repository "{}".'.format(repo))

            for iteration in range(1, info[keypoint]['iterations'] + 1):

                for idx in range(1,2):

                    filename = '{}{}_{}'.format(repo, idx, iteration)
                    in_img, in_ground = '{}.{}'.format(filename, info[keypoint]['fmt']), '{}.txt'.format(filename)
                    img = cv2.imread(in_img,0)

                    if img is None:
                        print('Image "{}" not found'.format(in_img))
                        continue

                    train_data = slice_image(img, in_ground)
                    labels, train_data = zip(*slice_image(img, in_ground))
                    labels, train_data = np.array(labels), np.array(train_data)
                    nsamples, nx, ny = train_data.shape
                    tsamples += nsamples
                    train_dataset = train_data.reshape((nsamples, nx*ny))
                    dataset['label'] += list(labels)
                    dataset['train'] += list(train_dataset)

        n_samples = int(len(dataset['train']) * 0.8)

        # SVM_PARAMS = dict( kernel_type = ml.SVM_LINEAR,
        #                     svm_type = ml.SVM_C_SVC,
        #                     C=2.67, gamma=5.383 )
        classifier = svm.SVC(gamma=0.001)
        classifier.fit(dataset['train'][:n_samples], dataset['label'][:n_samples])

        filename = 'model.svm'
        pickle.dump(classifier, open(filename, 'wb'))


        X_test = dataset['train'][n_samples:]
        Y_test = dataset['label'][n_samples:]
        loaded_model = pickle.load(open(filename, 'rb'))
        result = loaded_model.score(X_test, Y_test)
        print(result)

        X = np.array(dataset['train'])
        y = np.array(dataset['label'])
        kf = KFold(n_splits=2, shuffle=True, random_state=10**3)
        kf.get_n_splits(X)

        for train_index, test_index in kf.split(X):
            print("TRAIN:", len(train_index), "TEST:", len(test_index))
            X_train, X_test = X[train_index], X[test_index]
            y_train, y_test = y[train_index], y[test_index]
            print("TRAIN:", X_test, "TEST:", Y_test)

            expected = X_test
            predicted = classifier.predict(y_test)

            print("Classifier %s:\n%s\n" % (classifier, metrics.classification_report(expected, predicted)))
            print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))
            print("#", n_samples, "\n")

        # expected = dataset['label'][n_samples:]
        # predicted = classifier.predict(dataset['train'][n_samples:])
        #
        # print("Classifier %s:\n%s\n" % (classifier, metrics.classification_report(expected, predicted)))
        # print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))
        # print("#", n_samples, "\n")
        #
        # images_and_predictions = list(zip(dataset['train'][n_samples:], predicted))
        # for index, (image, prediction) in enumerate(images_and_predictions[:4]):
        #     print('index', index, image)
        #     # plt.subplot(2, 4, index + 5)
        #     plt.axis('off')
        #     plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
        #     plt.title('Prediction: %i' % prediction)
        #
        # plt.show()

        # Save images roi
        # for i, roi in enumerate(slice_pore_image(img, in_ground)):
            # cv2.imwrite('{}{}_{}.jpeg'.format(repo_out,idx,i), roi)
