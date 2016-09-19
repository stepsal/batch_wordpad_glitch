# batch_wordpad_glitch
Batch Wordpad Glitch processer written in Python. (Should work on 2.7 + 3.x )
Requires pillow

Here is a platform independent implementation of the wordpad glitch effect, with some added bonuses.
(1) You dont need wordpad
(2) You dont need windows
(3) You dont have to bother converting your images to BMP
(5) It batch processes as many files as you want.
(3) It 100 times faster
(4) It never crashes on huge files like wordpad does.


Currently on workd with Python 3 due to changes in fact the StringIO was replaced with the io module in python 3
I'll make a python 2.x port to follow.

One of the interesting things about this is that now its possible to create you own implementation of how
the wordpad glitch works by fucking around with the WORDPAD_GLITCH substitution parameters. Give me
a shout if you come up with some new replacement pairs that look shit hot.

Big ups to Justin Fay for figuring out a very clever way of doing this.

