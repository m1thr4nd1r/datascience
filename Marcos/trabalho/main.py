import sys
import os
import cv2
import cv2.ml as ml

# import matplotlib.pyplot as plt
import numpy as np

def slice_image(img, in_ground, half_window = 5):

    w,h = img.shape

    with open(in_ground) as ground_f:

        database = []

        for line in ground_f:

            x,y = [ int(a) for a in line.split(' ') ]
            #Select ROI
            roi = img[max(x-half_window,0):min(x+half_window,w),max(y-half_window,0):min(y+half_window,h)]
            # #Show ROI
            # cv2.imshow('image',roi)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            database.append(roi)

        return database

    return []

if __name__ == '__main__':
    opt, *args = sys.argv[1:]

    if opt == 't' or opt == 'train':

        repo_in, repo_out = args

        for idx in range(1,31):

            filename = '{}{}'.format(repo_in,idx)
            in_img, in_ground = '{}.bmp'.format(filename), '{}.txt'.format(filename)
            img = cv2.imread(in_img,0)

            if img is None:
                print('Image "{}" not found'.format(in_img))
                sys.exit()

            # Save images roi
            # for i, roi in enumerate(slice_image(img, in_ground)):
                # cv2.imwrite('{}{}_{}.jpeg'.format(repo_out,idx,i), roi)
