import  cv2
import os
from matplotlib import pyplot as plt
from model import *
from utils import *
import os
import time
import logging
import argparse
import numpy as np
import random
from numpy import expand_dims
from keras.preprocessing.image import load_img, img_to_array
import tensorflow as tf


def main():

    model = make_yolov3_model()
    # load the model weights
    # I have loaded the pretrained weights in a separate dataset
    weight_reader = WeightReader('yolov3.weights')

    # set the model weights into the model
    weight_reader.load_weights(model)

    # save the model to file
    model.save('model.h5')

    from keras.models import load_model
    model = load_model('model.h5')

    model.summary()

    anchors = [[116,90, 156,198, 373,326], [30,61, 62,45, 59,119], [10,13, 16,30, 33,23]]

    # define the expected input shape for the model
    WIDTH, HEIGHT = 416, 416

    # define the probability threshold for detected objects
    class_threshold = 0.5

    
    images=os.listdir('images')

    for file in images:
    
        if file == '.DS_Store':
            continue
        photo_filename ='images/' + file
        #a = tf.timestamp()
        # load picture with old dimensions
        image, image_w, image_h = load_image_pixels(photo_filename, (WIDTH, HEIGHT))
    
        # Predict image
        yhat = model.predict(image)
        print(len(yhat))

        # Create boxes
        boxes = list()
        for i in range(len(yhat)):
            # decode the output of the network
            boxes += decode_netout(yhat[i][0], anchors[i], class_threshold, HEIGHT, WIDTH)

        # correct the sizes of the bounding boxes for the shape of the image
        correct_yolo_boxes(boxes, image_h, image_w, HEIGHT, WIDTH)

        # suppress non-maximal boxes
        do_nms(boxes, 0.5)

        # define the labels (Filtered only the ones relevant for this task, which were used in pretraining the YOLOv3 model)
        labels = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck","boat","traffic light",
"fire hydrant","stop sign","parking meter","bench","bird","cat","dog","horse","sheep",
"cow","elephant","bear","zebra","giraffe","backpack","umbrella","handbag","tie","suitcase",
"frisbee","skis","snowboard","sports ball","kite",'baseball bat','baseball glove','skateboard','surfboard','tennis racket','bottle',
'wine glass','cup','fork','knife','spoon','bowl','banana','apple','sandwich','orange','broccoli',
'carrot','hot dog','pizza','donut','cake','chair','sofa','pottedplant','bed','diningtable',
'toilet','tvmonitor','laptop','mouse','remote','keyboard','cell phone','microwave','oven','toaster','sink','refrigerator',
'book',"clock","vase","scissors","teddy bear",'hair drier',"toothbrush"]

        # get the details of the detected objects
        v_boxes, v_labels, v_scores = get_boxes(boxes, labels, class_threshold)

        # summarize what we found
        for i in range(len(v_boxes)):

            print(v_labels[i], v_scores[i])

        # draw what we found
        draw_boxes(photo_filename, v_boxes, v_labels, v_scores)
        #b= tf.timestamp()
        #print(b-a)

if __name__ == '__main__':
    main()        