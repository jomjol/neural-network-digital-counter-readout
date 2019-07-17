# neural-network-digital-counter-readout
Training and using a neural network to readout the value of a digital counter - example including small node server for demonstration

The readout is used in a water meter measurement system. An overview can be found here: [https://github.com/jomjol/water-meter-measurement-system](https://github.com/jomjol/water-meter-measurement-system)

## Problem to solve

An image of a number between 0 and 9 should be recognized and converted to the corresponding digital value. One complicating issue is, that as the digits are comming from a rolling counter number, there are some pictures, which are not ambigious. In this case the result should be a "NaN", indicating, that this is not a full number.
To solve this problem a neural network approach is used.

The rolling counter meter looks like following:

<img src="./images/counter_complete.png" width="250">  

The image is sliced into individual pictures, which are analysed by a neural network.

## Neural Network Approach

Convolutional Neural Networks (CNN) are very promiment in image processing. Especially in classification of image content, e.g. identify objects (dog, cat, car, bike, ...) or classify hand written letters.

Here a classic approach is used to classify the picture into 11 output classes representing the 10 digits from 0 to 9 and the "NaN". 

| Picture        | Value           | Picture        | Value           | Picture        | Value           | Picture        | Value           |
| ------------- |:-------------:| ------------- |:-------------:|------------- |:-------------:| ------------- |:-------------:|
| <img src="./images/counter2.jpg" width="60"> | 2 | <img src="./images/counter6.jpg" width="60"> | 6 |<img src="./images/counter9.jpg" width="60"> | 9 | <img src="./images/counterNaN.jpg" width="60"> | NaN |


### Labeled Training Data

The images are coming from a camera system described elsewhere ([Overview](https://github.com/jomjol/water-meter-measurement-system), [HW](https://www.thingiverse.com/thing:3238162), [SW](https://github.com/jomjol/water-meter-picture-provider)). One major effort is to label the pictures with the target value. The labeling is done by hand. For each digit about 150 images are collected. For the "NaN" category about 3700 images were taken. The picture are rescaled to 32x20 pixels with RGB color (3 channels).

The resized pictures (subfolder Train-CNN_Analog-Needle-Readout/data_resize_all_NaN) as well as the original pictures (zipped in file "data_raw_all.zip") are included in the dataset. The pictures are stored in a subfolder for each digit (and NaN).

The project consists of two parts:
1. Training the network
2. Using the trained network within a simple http-server

## Training the network

The training is done using Keras in a python environment. For training purpuses the code is documented in Jupyter notebooks. The environment is setup using Ananconda with Python 3.7[1]. 

The training is descibed in detail in the subfolder [Train-CNN_Digital-Counter-Readout](Train-CNN_Digital-Counter-Readout).

The trained network is stored in the Keras H5-format and used as an input for a simple usage

## Using the trained network

### Server Usage

The setup and structure of the server is described in the subfolder [Server-CNN_Digital-Counter-Readout](Server-CNN_Digital-Counter-Readout)

The server is listening to port 3000 and accepts requests in the following syntac:

http://server-ip:3000/?url=http://picture-server/image.jpg

* server-ip: address of the node-server running the script
* parameter "url": url to the picture to be analysed 

The output is the following:

   <img src="./images/server_output.png" width="400">
   


Hopefully you have fun with neural networks and find this usefull. 

**Any questions, hints, improvements are very welcome through the GitHub channel**

Best regards,

**jomjol**
  
  
[1]: The following book is found very usefull for background, basic setting and different approaches:  
Mattheiu Deru and Alassane Ndiaye: Deep Learning with TensorFlow, Keras, und Tensorflow.js


 
