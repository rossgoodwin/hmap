Hmap
====

An image histogram remapping script written in Python 2.7 by Anthony Kesich and Ross Goodwin. Changes source image so that source image's histogram matches target image's histogram. Requires PIL/Pillow:

    $ sudo pip install Pillow

To run Hmap, cd into the directory where the hmap.py (for black and white images) or hmap_c.py (for color images) is located. Ensure source and target images have the same height and width dimensions (in pixels), and place them in the directory. Run the script with 2 additional arguments (source and target image files) as shown in the following example.

Example:

    $ sudo python hmap\_c.py source\_image.jpg target\_image.jpg
