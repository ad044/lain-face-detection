import cv2
import numpy as np
import os
import tensorflow as tf
import sys


def parse_labels(path):
    labels = []
    for line in tf.gfile.GFile(path):
        label = line.rstrip()
        labels.append(label)
    return labels


def import_graph(path):
    with tf.gfile.FastGFile(path, 'rb') as graph:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(graph.read())
        _ = tf.import_graph_def(graph_def, name='')


def main():
    cap = cv2.VideoCapture("./testvid.mp4")
    frame_width = int(cap.get(3))  
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter("./out.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                      10, (frame_width, frame_height))
    import_graph(os.getcwd() + '/retrained_graph.pb')
    with tf.Session() as sess:
        while(cap.isOpened()):
            ret, image = cap.read()
            cascade = cv2.CascadeClassifier("./lbpcascade_animeface.xml")
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)

            faces = cascade.detectMultiScale(gray,
                                             scaleFactor=1.1,
                                             minNeighbors=5,
                                             minSize=(24, 24))
            print(faces) 
            for (x, y, w, h) in faces:
                crop_img = image[y:y+h, x:x+w]
                img_to_array = np.array(crop_img)[:, :, 0:3]
                final_tensor = sess.graph.get_tensor_by_name(
                    'final_tensor:0')
                predictions = sess.run(
                    final_tensor, {'DecodeJpeg:0': img_to_array})
                sorted_predictions = predictions[0].argsort(
                )[-len(predictions[0]):][::-1]

                # if first element is 1 then the model has recognized lain in the image.
                # if so, draw a rectangle around her face, show image and continue
                if sorted_predictions.flat[0] == 1:
                    cv2.rectangle(
                        image, (x, y), (x + w, y + h), (0, 0, 255), 2)

                for prediction in sorted_predictions:
                    labels = parse_labels(
                        os.getcwd() + '/output_labels.txt')
                    label_to_str = labels[prediction]
                    confidence = predictions[0][prediction]
                    score_as_percent = confidence * 100.0
                    result = '{}, {:.2f}%'.format(
                        label_to_str, score_as_percent)

            if ret == True:
                out.write(image)
                #cv2.imshow('frame', image)


            cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
