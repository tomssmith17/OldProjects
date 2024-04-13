#Youtube tutorial by sentdex: https://www.youtube.com/watch?v=gT4F3HGYXf4&list=PLQVvvaa0QuDfKTOs3Keq_kaG2P55YRn5v&index=63
#Data from Kaggle: https://www.kaggle.com/c/dogs-vs-cats-redux-kernels-edition/data


#Use Convolution Neural Network to Identify Images of Dogs vs. Cats (using OpenCV and TensorFlow)

import cv2   #OpenCV
import numpy as np
import os
from random import shuffle
from tqdm import tqdm
#this script must be run in cmd for tqdm progress bar to work properly
#see link for more info: https://github.com/tqdm/tqdm#faq-and-known-issues


TRAIN_DIR = "C:/Users/tomss/Desktop/Python_Learning_Summer_2018/CatDog_Data/train/train"
TEST_DIR = "C:/Users/tomss/Desktop/Python_Learning_Summer_2018/CatDog_Data/test/test"
IMG_SIZE = 50
LR = 1e-3   #learning rate, larger it is, longer it takes to train
#large learning rate, more likely to miss the best objective, super small learning rate
#will either confine itself to a local maxima/minuma or take a super long time to run

MODEL_NAME = "dogsvscats-{}-{}.model".format(LR, "2conv-basic-video")


def label_img(img):
    word_label = img.split('.')[-3]
    if word_label == 'cat': return [1,0]
    elif word_label == 'dog': return [0,1]


def create_train_data():
    training_data = []
    for img in tqdm(os.listdir(TRAIN_DIR)):  
        label = label_img(img)
        path = os.path.join(TRAIN_DIR, img)
        img = cv2.resize(cv2.imread(path, cv2.IMREAD_GRAYSCALE), (IMG_SIZE, IMG_SIZE))
        training_data.append([np.array(img), np.array(label)])      
    shuffle(training_data)
    np.save('train_data.npy', training_data)
    return training_data


def process_test_data():
    testing_data = []
    for img in tqdm(os.listdir(TEST_DIR)):
        path = os.path.join(TEST_DIR, img)
        img_num = img.split('.')[0]
        img = cv2.resize(cv2.imread(path, cv2.IMREAD_GRAYSCALE), (IMG_SIZE, IMG_SIZE))
        testing_data.append([np.array(img), img_num])
    np.save('test_data.npy', testing_data)
    return testing_data


train_data = create_train_data()
# if you already have train data:
# train_data = np.load('train_data.npy') --> check exists via os and make sure same image dimensions

####### Spend time to understand part below #####

import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression


convnet = input_data(shape=[None, IMG_SIZE, IMG_SIZE, 1], name='input')

convnet = conv_2d(convnet, 32, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = conv_2d(convnet, 64, 2, activation='relu')
convnet = max_pool_2d(convnet, 2)

convnet = fully_connected(convnet, 1024, activation='relu')
convnet = dropout(convnet, 0.8)

convnet = fully_connected(convnet, 2, activation='softmax')
convnet = regression(convnet, optimizer='adam', learning_rate=LR, loss='categorical_crossentropy', name='targets')

model = tflearn.DNN(convnet, tensorboard_dir='log')


#Check to see if already saved a checkpoint, already trained a network for certain data/epochs aka best weights have been found, allow you to save progress as you go
if os.path.exists('{}.meta'.format(MODEL_NAME)):
    model.load(MODEL_NAME)
    print('model loaded!')


train = train_data[:-500]
test = train_data[-500:]    #testing our network against labeled training data

#data being fit to the model 
X = np.array([i[0] for i in train]).reshape(-1, IMG_SIZE, IMG_SIZE, 1) #i[0] is actual image/pixel info
Y = [i[1] for i in train] #i[1] is label of image

#data for testing accuracy
test_x = np.array([i[0] for i in test]).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
test_y = [i[1] for i in test]

model.fit({'input': X}, {'targets': Y}, n_epoch=5, validation_set=({'input': test_x}, {'targets': test_y}), 
    snapshot_step=500, show_metric=True, run_id=MODEL_NAME)



# run this script in cmd: C:\Users\tomss\AppData\Local\Programs\Python\Python36\python.exe C:\Users\tomss\Desktop\Python_Learning_Summer_2018\Cats_vs_Dogs.py
# put into cmd for graphical display of results: tensorboard --logdir=foo:C:\Users\tomss\Desktop\Python_Learning_Summer_2018\log
