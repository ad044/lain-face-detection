import cv2
import numpy as np
import os
import tensorflow as tf


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
    import_graph(os.getcwd() + '/retrained_graph.pb')
    with tf.Session() as sess:
        test_dir = os.getcwd() + '/test_images'
        for file in os.listdir(test_dir):
            cascade = cv2.CascadeClassifier("./lbpcascade_animeface.xml")
            image = cv2.imread(os.path.join(test_dir, file), cv2.IMREAD_COLOR)
            print(file, dir)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)

            faces = cascade.detectMultiScale(gray,
                                             scaleFactor=1.1,
                                             minNeighbors=5,
                                             minSize=(24, 24))
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
                print('\n{}'.format(os.path.join(test_dir, file)))
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
                    cv2.imshow(file, image)
                    print(result)

            cv2.waitKey()
            cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
