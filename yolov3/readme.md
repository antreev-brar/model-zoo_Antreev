# Tensorflow Implementation of YOLOv3

Download weights in the repo containing files
```bash 
$ wget https://pjreddie.com/media/files/yolov3.weights
```
## Usage
```bash
$ python3 main.py 
```
In order to use the model on custom images add them into images directory

> **_NOTE:_** on Colab Notebook use following command:
```python
!git clone https://github.com/antreev-brar/model-zoo.git
%cd /content/model-zoo/yolov3
!wget https://pjreddie.com/media/files/yolov3.weights
!python main.py
```
## Contributed by:
* [Antreev Singh Brar](https://github.com/antreev-brar)
## References

* **Title**: YOLOv3: An Incremental Improvement
* **Authors**: Joseph Redmon, Ali Farhadi
* **Link**: https://arxiv.org/abs/1804.02767v1
* **Tags**: Neural Network
* **Year**: 2018

# Summary

## Why new Model(Drawbacks of YOLOv1 and YOLOv2)

* YOLOv1 imposes strong spatial constraints on bounding box predictions since each grid cell only predicts two boxes and can only have one class. This spatial constraint limits the number of nearby objects that our model can predict. Model struggles with small objects that appear in groups, such as flocks of birds. Since the model learns to predict bounding boxes from data, it struggles to generalize to objects in new or unusual aspect ratios or configurations.  Model also uses relatively coarse features for predicting bounding boxes since their architecture has multiple downsampling layers from the input image. Finally, while  train on a loss function that approximates detection performance, their loss function treats errors the same in small bounding boxes versus large bounding boxes. A small error in a large box is generally benign but a small error in a small box has a much greater effect on IOU. The main source of error is incorrect localizations
* YOLO v2 used a custom deep architecture darknet-19, an originally 19-layer network supplemented with 11 more layers for object detection. With a 30-layer architecture, YOLO v2 often struggled with small object detections. This was attributed to loss of fine-grained features as the layers downsampled the input.YOLO v2’s architecture was still lacking some of the most important elements that are now staple in most of state-of-the art algorithms. No residual blocks, no skip connections and no upsampling. YOLO v2 used softmax for class prediction which isn't the most suitable choice .
## Introduction 
Main purpose of a object detector is to be fast and accurate and able to recognize wide dataset.


## Key features of YOLOv3
### Bounding Box
 - It is same as that used in Previous versions . Cordinates are predicted and sum of squared error loss is used while training
- Objectness score is predicted using logistic regression

### Class Prediction
- Softmax is not used.
- Independent logistic classifiers are used and binary cross-entropy loss is used

### Prediction on different scales
- As my personal opinion it is the best feature of YOLOv3 , it predicts bounding boxes on 3 different scales for detection on different scales . Previous versions used just one .
- k-means clustering is used here as well to find better bounding box prior but this version used predefined anchor box dimensions.
- Darknet - 53 feature extractor is used which is much deeper than Darknet- 19 used in YOLO v2


### Model Summary
![4](./assets/architecture.png)
```
Total params: 62,001,757
Trainable params: 61,949,149
Non-trainable params: 52,608
```
I used yolov3 pretrained on MSCOCO dataset

## What happens in the Background 
#### I wanna use this part of summary to take you through a journey as from the perspective on an image on how predictions are made.
 - We build a model as per the architecture defined above and load it weights which were trained on MSCOCO dataset that has 80 classes.
 - Now you have to define anchor box dimensions ,will explain later what it means but there are two ways to do it . Run k-means clustering algorithm through your image dataset to find best anchor dimensions or set them manually.
##### We are ready to start image processing now .

YOLOv3 needs that all images that enter the neural net should have dimensions of (416 * 416) . So we need to change dimensions of image to the ones required.Further we need to set one more value that is class_threshold . 

The best way to see it is , you are telling the model about the minimum value that a class prediction should have to be considered as a true prediction . For eg lets say if model thinks that the figure enclosed in a bounding box is [53% human , 10 % car , 10% tree ..] (rest of the values dont matter as we deal only with maximum) and we have set class threshold at 0.5 then it will consider that it is a human and will show it as an output , if it were higher like 0.6 then this prediction would be rejected.


##### Lets make predictions 

- We pass the image of shape (416,416,3) into the neural architecture then it makes ((13 * 13 )+(26 * 26) +(52 * 52) * 3 * 3) predictions . As for each cell on each scales it makes 3 bounding box predictions and for each box we have 3 anchor boxes so total 9 . 
- Look at the architecture the ouput seems to be three 3D arrays of shape (13,13,69) , (26,26,69) ,(52,52,69) . Here in our case the number is 255 , but the 13,26,52 are fixed as they describe that u divided the image into 13 * 13 cells and then made predictions on them , likewise for 26 and 52.
- Lets have a look on the 255 number itself it is 3 * 85 , 3 being the number of boxes predicted for each cell and 85 comes from 5 + number_of_classes (i.e 80 ) .This is all the information u need to make a predication . The 5 values in the begining are :
* tx - will give us X cordinate of the centre of box after an operation;  
* ty - will give us Y cordinate of the centre of box after an operation;
* th - will give us height of box after an operation;
* tw - will give us width of box after an operation;
* p - probability of having any object at all in the cell





# Results

## Images
![4](./assets/i0.jpg)
![4](./assets/i11.jpg)
![4](./assets/i210.jpg)
![4](./assets/i365.jpg)
