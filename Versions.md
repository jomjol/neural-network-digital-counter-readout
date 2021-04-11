## Version
#### 8.3.0 Current Version - (2021-04-06)

* Update with additional set up digits

#### 8.1.1 Current Version - (2021-02-27)

* Update with additional set up digits

#### 7.2.1 Current Version - (2020-12-29)

* Update with additional set up digits

#### 7.1.0 Current Version - (2020-11-17)

* Update with additional set up digits

#### 7.0.0 Current Version - (2020-10-31)

* Included LCD-digits in training

#### 6.5.0 Current Version - (2020-10-24)

* Update with additional set up digits (gas counter, electric power counter)

#### 6.4.0 Current Version - (2020-09-23)

* Update with additional set up digits

#### 6.3.0 Current Version - (2020-09-02)

* Relabeling of training images
  * Take out unambiguous (number or NaN)  - criteria for number: complete picture is in the ROI visible
    [Labeling-Criteria.md](Labeling-Criteria.md)
  * Remove replicated pictures
* Implementation of "train all" parameter
* Experiments with reduces network size for speeding up image recognition ("...-Small-vX.tflite")
* Training with new picture from iobroker users
* White on black, white on red digits - additional pictures

#### 6.2.0 Current Version - (2020-07-11)

* Training with new picture from iobroker users
* White on black, white on red digits

#### 6.1.2 Version - (2020-06-15)

* Training with new picture from iobroker users

#### 6.1.1 Version - (2020-05-29)

* Training with new picture from iobroker users

#### 6.1.0 Version (2020-05-09)

* Training with new picture from iobroker users
* For size minimized tflite-File implemented ("_quantized")

#### 6.0.0 Tensorflow 2.1 (2020-04-18)

* Updated to Tensorflow 2.1
* additional export to TF-Lite Version (.tflite)
* Training with new picture from iobroker users

#### 5.0.0 Current Version - Tensorflow 2.0
* Training with new picture from iobroker users
* Removal of standalone server - (included in main project)Training of additional digital number (provided from iobroker users)
#### 4.2.0 Current Version - Tensorflow 2.0
* Training of additional digital number (provided from iobroker users)
#### 4.0.0 Tensorflow 2.0, Pillow
* Image processing changed to Pillow (remove OpenCV)
* Usage of Tensorflow 2.0 for training
##### 3.0 Version number skipped due to consistency with other programm part
##### 2.0 Transfer from Node.JS to Python
* Change Image handling completely to OpenCV-Library
* Learning with increased ZoomRange (10% --> 40%), learning within one step
##### 1.0 Initial Version