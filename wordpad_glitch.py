# Python Wordpad Glitch Batch Processor by Stephen Salmon
# stephensalmon.mayo@gmail.com
# Justin Fay gets credit for coming up with such a neat way to
# achieve this during a ciggie break.
# This script recreate the classic wordpad glitch in python
# Which means you dont need bloody wordpad anymore and it never hangs
# on large images like wordpad used to.
# Just throw a load of images into the input directory.. dont worry
# the script  converts them to bmp automatically.

__author__ = "Justin Fay & Stephen Salmon"

import argparse
import functools
import io
import os.path
import re
import sys

from PIL import Image

INPUT_DIR = 'input'
OUTPUT_DIR = 'output'
IMG_FORMATS = ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.gif', '.bmp']
ROTATE = False
ROTATIONS = [90, 180, 270]
ROTATE_ARGS = ''
PATHS = []

WORDPAD_GLITCH = [
    (b'\x07', b'\x27'),
    (b'\x0B', b'\x0A\x0D'),
    (b'(?<!\x0A)(\x0D)', b'\x0A\x0D'),
    (b'(\x0A)(?<!\x0D)', b'\x0A\x0D')]

_WORDPAD_GLITCH = [
    (re.compile(sub), replacement) for (sub, replacement) in WORDPAD_GLITCH]


def replace(img, replacements=()):
    for pattern, replacement in replacements:
        img = pattern.sub(replacement, img)
    return img


wordpad_replacer = functools.partial(replace, replacements=_WORDPAD_GLITCH)


def wordpad_glitch(input_image, output_image):
    with open(input_image, 'rb') as rh:
        img = io.BytesIO(rh.read())
    img.seek(0)
    header = img.read(16 + 24)
    glitched = io.BytesIO(header + wordpad_replacer(img.read()))
    glitched.seek(0)
    output = io.BytesIO(glitched.read())
    with open(output_image, 'wb') as wh:
        wh.write(output.read())
    print("saved image {0}".format(output_image))
    wh.close()


def create_output_dirs():
    if ROTATE_ARGS == "ALL":
        for degree in ROTATIONS:
            sub_dir = str(degree)
            path = os.path.join(OUTPUT_DIR, sub_dir)
            PATHS.append(path)
    else:
        sub_dir = ROTATE_ARGS
        path = os.path.join(OUTPUT_DIR, sub_dir)
        PATHS.append(path)
    for path in PATHS:
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError as exc:
                print(str(exc))
                print("could not create subdir dir {0}".format(path))
                sys.exit(2)
    if not os.path.exists(OUTPUT_DIR):
        try:
            os.makedirs(OUTPUT_DIR)
        except:
            print("could not create output dir")
            sys.exit(2)


def create_output_files(img, filename):
    output_files = []
    output_filepath = os.path.join(OUTPUT_DIR, 'wp_' + filename + '.bmp')
    try:
        img.save(output_filepath)
        output_files.append(output_filepath)
    except IOError:
        print("could not save bmp file {0}".format(output_filepath))

    if ROTATE:
        if ROTATE_ARGS == "ALL":
            for degrees in ROTATIONS:
                output_directory = os.path.join(OUTPUT_DIR, str(degrees))
                output_filepath = os.path.join(
                    output_directory,
                    'wp_{0}_{1}.bmp'.format(degrees, filename))
                img = img.rotate(degrees, expand=True)
                try:
                    img.save(output_filepath)
                    output_files.append(output_filepath)
                except IOError:
                    print("could not save bmp file {0}".format(
                        output_filepath))
        else:
            output_directory = os.path.join(OUTPUT_DIR, ROTATE_ARGS)
            output_filepath = os.path.join(
                output_directory,
                'wp_{0}_{1}.bmp'.format(ROTATE_ARGS, filename))
            img = img.rotate(int(ROTATE_ARGS), expand=True)
            try:
                img.save(output_filepath)
                output_files.append(output_filepath)
            except IOError:
                print("could not save bmp file {0}".format(output_filepath))
    return output_files


def main():
    if not os.path.exists(INPUT_DIR):
        print("error: could not find the input folder")
        sys.exit(2)
    create_output_dirs()

    # convert all the images in the input directory to bitmaps then glitch them
    for file in os.listdir(INPUT_DIR):
        filepath = os.path.join(INPUT_DIR, file)
        if os.path.isfile(filepath):
            if os.path.splitext(filepath)[1].lower() in IMG_FORMATS:
                img = Image.open(filepath)
                filename = os.path.basename(filepath).split('.')[0]
                for output_filepath in create_output_files(img, filename):
                    wordpad_glitch(output_filepath, output_filepath)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Batch Wordpad Glitch')
    parser.add_argument(
        "-i", "--input", dest="INPUTDIR", help="input dir of source images")
    parser.add_argument(
        "-o", "--output",
        dest="OUTPUTDIR",
        help="ouput dir of glitched images")
    parser.add_argument(
        "-r", "--rotate",
        dest="ROTATE",
        help="Rotate the input images before glitching.. "
        "values 90, 180, 270, ALL")
    try:
        args = parser.parse_args()
    except:
        print("Args Error")
        parser.print_help()
        sys.exit(2)

    if args.INPUTDIR:
        INPUT_DIR = args.INPUTDIR
    if args.OUTPUTDIR:
        OUTPUT_DIR = args.OUTPUTDIR
    if args.ROTATE:
        if args.ROTATE not in ['90', '180', '270', 'ALL']:
            print("Invalid Rotation Argument")
            parser.print_help()
            sys.exit(2)
        else:
            ROTATE = True
            ROTATE_ARGS = args.ROTATE
    main()
