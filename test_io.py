import io
import re
import functools

input_image = "/home/stephen.salmon/github/stepsal/wordpad_glitch/sku2.bmp"
output_image = "/home/stephen.salmon/github/stepsal/wordpad_glitch/test800.bmp"

def replace(img, replacements=()):
    for pattern, replacement in replacements:
        img = pattern.sub(replacement, img)
    return img

WORDPAD_GLITCH = [
    (b'\x07', b'\x20'),
    (b'\x0B', b'\x0A\x0D'),
    (b'(?<!\x0A)(\x0D)', b'\x0A\x0D'),
    (b'(\x0A)(?<!\x0D)', b'\x0A\x0D')]
_WORDPAD_GLITCH = [
    (re.compile(sub), replacement) for (sub, replacement) in WORDPAD_GLITCH]

wordpad_replacer = functools.partial(replace, replacements=_WORDPAD_GLITCH)

with open(input_image, 'rb') as rh:
    img = io.BytesIO(rh.read())

img.seek(0)
header = img.read(16 + 24)
glitched = io.BytesIO(header + wordpad_replacer(img.read()))
glitched.seek(0)
output = io.BytesIO(glitched.read())
# print(output.getbuffer().nbytes)
# output.seek(0)
# print(output.getbuffer().nbytes)

x = output.read()
with open(output_image, 'wb') as wh:
    wh.write(x)

wh.close()
