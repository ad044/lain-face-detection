
## Lain image detection using Inception V3 and LBP Cascade

Brief overview of the history behind this projcet
------------
Here we are, again. Another shot at creating a "Lain vs All" classifier that works on universally any type of image. My [last attempt at that](https://github.com/d9x33/lain-vs-hotdog) was a complete failure. At the beginning, my plan was to just put a bunch of random, messy Lain images that I didn't filter against a bunch of random images hoping it'd work. Unsurprisingly, it didn't. So I scrapped the project and turned it into a binary classifier of Lain vs Hot-dogs - better than nothing, I suppose.

Fast forward to today, I came across [freedomofkeima's anime face detection project](https://github.com/freedomofkeima/transfer-learning-anime) which gave me a new outlook about this problem, so here we are, I present to you my Lain detection model.

Model overview
-----------

Visual overview taken from the [original anime transfer learning repo](https://github.com/freedomofkeima/transfer-learning-anime) (except I replaced Maki with Lain so it makes more sense)
![img](https://i.imgur.com/x2VpXcA.png)
The basic principle of this entire project is to leave the feature extraction part of image classification to LBP cascade using [nagadomi's anime face detection](https://github.com/nagadomi/lbpcascade_animeface), and then train the Inception v3 model using those images. Same goes for images used for testing, before reaching the classification phase, we use cv2 to crop the images, extract features, and pass those images into the model.

**Training**:
1. Get random images of anime characters using the [danbooru 2019 dataset](https://www.gwern.net/Danbooru2019), pass them through the anime face detector which recognizes the faces, crops the image, resizes it to be 96x96px and saves it as training data.
2. Do the same for Lain images.
3. Train the model using "lain" and "not lain" labels, for which the features are already extracted (from cropping the important features using LBP cascade) and save it.

**Testing**:
1. Load the image, pass it to the face detector, crop it, resize it to 96x96px.
2. Use that cropped image to classify, if it matches "lain", we draw a rectangle around the crop area in the original image. 

As an example, this is what the uncropped training dataset looks like (what I used for my old model):
![Img](https://i.imgur.com/SVY2mvL.jpg)
This is what it it looks like now:

![img](https://i.imgur.com/g4dZDMG.jpg)

Results
-----------
Well, they're looking quite good.

![img](https://i.imgur.com/b2KMqVL.png)
The training finished with a final test accuracy of about **91%** at step 4200.

Considering the entire Lain dataset is only 618 images (along with help from using the pretrained model with transfer learning), the results surprised me.

On a test set with 160 images, which you can see [here](https://mega.nz/folder/0cdA3I4D#q7evL4yDlko5aaQQOMI6wA), the model only got **16** images incorrectly.

As a general rule of thumb, if the LBP Cascade can recognize Lain in the image, the model will almost certainly predict accurately. The anime face detector has about a **83%** accuracy rate at recognizing faces, which reflects on the model itself.

Code overview
-----------
As a general warning, most of the code in this project are helpers I used to gather/clean data, I wrote them up mostly in a couple of minutes to automate tasks, so they're extremely messy.

- **retrained_graph.pb** - is the output graph fom the training process that you can use, along with the labels contained in **output_labels.txt**.
- **dataset.txt** - All the images I used, formatted.
- **data_preprocessing** - scripts used to batch detect/crop images with the anime face detector.
- **data_cleaning** - scripts used to remove duplicates and in general format the freshly downloaded, messy data.
- **get_training_data** - scripts used to automate mass downloading Lain images.
- **lbpcascade_animeface.xml** - parameters for LBP Cascade provided by [nagadomi](https://github.com/nagadomi/lbpcascade_animeface).
- **test.py** - testing batches of images from a certain folder
- **train.py** - training code for the Inception V3 model using transfer learning.

Todo
-----------
- Add **eval.py** - a simple and hackable version of test.py that people can use easily.
- Test the model's performance on moving frames such as videos.

Requirements
-----------
-   OpenCV ([https://github.com/opencv/opencv](https://github.com/opencv/opencv))
-   TensorFlow ([https://github.com/tensorflow/tensorflow](https://github.com/tensorflow/tensorflow))

References
-----------
- https://github.com/freedomofkeima/transfer-learning-anime
- https://github.com/nagadomi/animeface-2009
- http://freedomofkeima.com/blog/posts/flag-15-image-recognition-for-anime-characters
