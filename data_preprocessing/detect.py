import cv2
import sys
import os.path


# anime face recognition model
# slightly modified version of the example provided in https://github.com/nagadomi/lbpcascade_animeface

# detects the face, crops the image around it and saves it
def detect(file_name, output_name, cascade_file):
    cascade = cv2.CascadeClassifier(cascade_file)
    image = cv2.imread(file_name, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    faces = cascade.detectMultiScale(gray,
                                     scaleFactor=1.1,
                                     minNeighbors=5,
                                     minSize=(24, 24))
    for (x, y, w, h) in faces:
        # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        crop_img = image[y:y+h, x:x+w]
        # print(faces)
        cv2.imwrite(output_name, cv2.resize(crop_img, (96, 96)))