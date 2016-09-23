# batch_wordpad_glitch
Batch Wordpad Glitch processer written in Python. (Should work on 2.7 + 3.x )
Requires pillow

PYthon implementation of the wordpad glitch effect.
(1) You dont need wordpad
(2) You dont need windows
(3) You dont have to bother converting your images to BMP
(5) It batch processes as many files as you want.
(3) It 100 times faster
(4) It never crashes on huge files like wordpad does.

[$ /usr/local/bin/python3.5 wordpad_glitch.py -help
usage: wordpad_glitch.py [-h] [-i INPUTDIR] [-o OUTPUTDIR] [-r ROTATE]

Batch Wordpad Glitch

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTDIR, --input INPUTDIR
                        input dir of source images
  -o OUTPUTDIR, --output OUTPUTDIR
                        ouput dir of glitched images
  -r ROTATE, --rotate ROTATE
                        Rotate the input images before glitching.. values 90,
                        180, 270, ALL

Big ups to Justin Fay for figuring out a very clever way of doing this.

