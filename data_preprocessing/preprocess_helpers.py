import cv2
import sys
import os.path
from detect import detect

# helper functions for detecting and cropping batches of images
# code here is a mess, if you want a brief overview just look at the last function

TRAINING_IMAGE_DIR = "../training_images"
TRAINING_IMAGE_DIR_EPISODES = "{}/lain/eps".format(TRAINING_IMAGE_DIR)
OUTPUT_DIR = "../training_cropped_images"
CASCADE_FILE_LOC = "../lbpcascade_animeface.xml"


# for images downloaded from the internet
def recognize_downloaded_images():
    for folder in os.listdir(TRAINING_IMAGE_DIR):
        if not os.path.exists("{}/{}".format(OUTPUT_DIR, folder)):
            os.makedirs("{}/{}".format(OUTPUT_DIR, folder))
        for training_img in os.listdir("{}/{}".format(TRAINING_IMAGE_DIR, folder)):
            src = "{}/{}/{}".format(TRAINING_IMAGE_DIR, folder, training_img)
            dest = "{}/{}/{}".format(OUTPUT_DIR, folder, training_img)
            print(dest)
            detect(src, dest, CASCADE_FILE_LOC)


# for images extracted frame-by-frame from the show
def recognize_from_episode_frames():
    for folder in os.listdir(TRAINING_IMAGE_DIR_EPISODES):
        for img in os.listdir("{}/{}".format(TRAINING_IMAGE_DIR_EPISODES, folder)):
            src = "{}/{}/{}".format(TRAINING_IMAGE_DIR_EPISODES, folder, img)
            print(src)
            dest = "{}/{}-{}".format(OUTPUT_DIR, folder, img)
            print(dest)
            detect(src, dest, CASCADE_FILE_LOC)


# just a simple function to point a folder to and itll just detect crop and save those images
def recognize_from_folder(src, dest):
    for image in os.listdir(src):
        source_dir = os.path.join(src, image)
        destinaton_dir = os.path.join(dest, image)
        print(destinaton_dir)
        detect(source_dir, destinaton_dir, CASCADE_FILE_LOC)

