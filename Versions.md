## Version
#### 19.0.0 Current Version (2024-12-27)

* Remove similar images **after** resize --> significantly reduced number of images
* Update Tensorflow training environment to v2.18

#### 13.3.0 Current Version (2021-11-23)

* New images for digits
* BMP as input for the rescaling script is now also supported

#### 13.2.0 Current Version (2021-10-29)

* New images (7-segment LCD, new analog types)
* Changed convolutional layer 2 & 3 to RELU activation function

#### 13.1.0 Current Version (2021-10-06)

* New images (minor change)

* License change (remove MIT license, remark see below)

  

**ATTENTION: LICENSE CHANGE - removal of MIT License.** 

- Currently no licence published - copyright belongs to author
- If you are interested in a commercial usage or dedicated versions please contact the developer



#### 13.0.0 Current Version - (2021-09-12)

* New type of digits (green LCD)

#### 12.1.0 Current Version - (2021-09-10)

* Adaption of augmentation range (reduction)
* Additional images, new type of digits

#### 12.0.0 Current Version - (2021-08-01)

* Save classification in file name instead of subdirectory
* Additional images, new type of digits

11.1.0 Current Version - (2021-07-28)

* Additional images, new type of digits

#### 11.0.0 Current Version - (2021-07-13)

* Updated quantization implementation (use original images)
* Internal improvements (speed)

#### 10.3.0 Current Version - (2021-06-29)

* Update with additional set of digits

#### 10.2.0 Current Version - (2021-06-27)

* Update with additional set of digits

#### 10.0.0 Current Version - (2021-06-19)

* Removing of double images
* Adding of V200 digits

#### 9.0.1 Current Version - (2021-05-29)

* NEW 9.0.1: Additional digits for the last variant
* New type of LCD-numbers integrated (white on black)
* Update with additional set of digits

#### **8.7.0** Current Version - (2021-05-27)

* Update with additional set of digits

#### 8.6.0 Current Version - (2021-05-18)

* Update with additional set of digits

#### 8.5.0 Current Version - (2021-05-07)

* Update with additional set up digits

#### 8.3.1 Current Version - (2021-04-11)

* Update with additional set up digits

#### 8.2.0 Current Version - (2021-03-25)

* Update with additional set up digits

* Change file naming convention (tflite file)

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