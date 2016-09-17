# Python Wordpad Glitch by Stephen Salmon
# stephensalmon.mayo@gmail.com
# Justin Fay gets credit for coming up with such a neat way to achieve this during a ciggie break.

# This script recreate the classic wordpad glitch in python
# Which means you dont need bloody wordpad anymore and it never hangs  on big images like wordpad used to.
# Just throw a load of images into the input directory.. dont worry the script  converts them to bmp automatically
# before processing because I know you are lazy like me

__author__ = "Justin Fay & stephen salmon"

from subprocess import call
import functools
import os.path
import re
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import PIL
from PIL import Image
input_dir = '/home/stephen.salmon/Pictures/Wordpad_Glitch'
output_dir = '/home/stephen.salmon/Pictures/Wordpad_Glitch/output'
output_format = '.tif'
images = []
image_formats = ['.jpg', '.jpeg', '.png', '.tif', '.bmp']

"""
The wordpad glitch is a tuple of 2tuples containing
a match and a replacement.. you could come up with your own
"""
WORDPAD_GLITCH = [
    (b'\x07', b'\x20'),
    (b'\x0B', b'\x0A\x0D'),
    (b'(?<!\x0A)(\x0D)', b'\x0A\x0D'),
    (b'(\x0A)(?<!\x0D)', b'\x0A\x0D')]
_WORDPAD_GLITCH = [
    (re.compile(sub), replacement) for (sub, replacement) in WORDPAD_GLITCH]

#Functions
def file_read(path, options='rb'):
    with open(path, options) as rh:
        return rh.read()

def file_write(path, content, options='wb'):
    with open(path, options) as wh:
        wh.write(content)

def str_io(content=''):
    io = StringIO(content)
    io.seek(0)
    return io

def convert(fh, format='jpeg'):
    img = Image.open(fh)
    wh = str_io()
    img.save(wh, format=format)
    wh.seek(0)
    return wh

def replace(img, replacements=()):
    for pattern, replacement in replacements:
        img = pattern.sub(replacement, img)
    return img

wordpad_replacer = functools.partial(replace, replacements=_WORDPAD_GLITCH)


def wordpad(infile, outfile):
    image = convert(str_io(file_read(infile)), 'bmp')
    # need to parse the header from the bmp file
    header = image.read(16 + 24)
    # perform the glitch
    glitched = str_io(header + wordpad_replacer(image.read()))
    # convert the image to a the output fle
    output = convert(glitched, 'jpeg')
    file_write(outfile, output.read())

if __name__ == '__main__':

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file in os.listdir(input_dir):
        filepath = os.path.join(input_dir, file)
        if os.path.isfile(filepath):
            if os.path.splitext(filepath)[1].lower() in image_formats:
                output_file = os.path.join(output_dir,file)
                wordpad(filepath, output_file)

