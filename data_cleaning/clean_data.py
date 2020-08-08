from PIL import Image, ImageOps, ImageStat
from shutil import move
import os
import subprocess

train_path = "../train_set"
test_path = "../test_set"


def join_path(path, file):
    return os.path.join(path, file)


def clear_extra_extensions(path):
    for file in [f for f in os.listdir(path) if (not f.endswith('.jpg'))
                                                and (not f.endswith('.png'))
                                                and (not f.endswitch('.jpeg'))]:
        os.remove(join_path(path, file))


def hash_image(image_path):
    img = Image.open(image_path).resize(
        (8, 8), Image.LANCZOS).convert(mode="L")
    mean = ImageStat.Stat(img).mean[0]
    return sum((1 if p > mean else 0) << i for i, p in enumerate(img.getdata()))


def get_image_size(image_path):
    img = Image.open(image_path)
    return img.size


def clear_duplicates_between_test_train(testpath, trainpath):
    hashes = []
    for file in os.listdir(trainpath):
        hashes.append(hash_image(join_path(trainpath, file)))

    for file in os.listdir(testpath):
        current_file = join_path(testpath, file)
        if hash_image(current_file) in hashes:
            os.remove(current_file)


def clear_dupliates_inside_dir(path):
    hashes = []
    for file in os.listdir(path):
        hashes.append(hash_image(join_path(path, file)))

    for file in os.listdir(path):
        if hashes.count(hash_image(join_path(path, file))) > 1:
            os.remove(join_path(path, file))


def unpack_folders(path, dest):
    for file in os.listdir(path):
        if os.path.isdir(path + file):
            curr_dir = path + file
            for file in os.listdir(curr_dir):
                current_file = curr_dir + '/' + file
                dest_file = dest + file
                move(current_file, dest_file)
            os.rmdir(curr_dir)


def delete_too_small(path):
    for file in os.listdir(path):
        current_size = get_image_size(path + file)
        if current_size[0] < 150 or current_size[1] < 150:
            os.remove(join_path(path, file))


def delete_corrupted_images(path):
    for file in os.listdir(path):
        if file.endswith('jpg') or file.endswith('jpeg'):
            try:
                status = subprocess.check_output(["jpeginfo", "-c", join_path(path, file)])
            except subprocess.CalledProcessError as e:
                if '[WARNING]' in str(e.output) or '[ERROR]' in str(e.output):
                    print(file)
                    os.remove(join_path(path, file))

