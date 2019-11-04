Hmap
====

An image histogram remapping script written in Python 2.7 by [Anthony Kesich](http://kesi.ch) and [Ross Goodwin](http://rossgoodwin.com). Changes source image so that source image's histogram matches target image's histogram. Requires PIL/Pillow:

    $ sudo pip install Pillow

To run Hmap, cd into the directory where hmap.py (for black and white images) or hmap_c.py (for color images) is located. Ensure source and target images have the same height and width dimensions (in pixels), and place them in the directory. Run the script with 2 additional arguments (source and target image files) as shown in the following example.

Example:

    $ python hmap_c.py source_image.jpg target_image.jpg


hmap.py
=======

Source Image:

![Source Image](http://imgur.com/MGCUWZo.jpg "Source Image")


Target Image:

![Target Image](http://imgur.com/vuGrjAY.jpg "Target Image")


Result:

![Result](http://imgur.com/KavoDjf.jpg "Result")

*Photographs by Ansel Adams*


hmap_c.py
=========

Color Source Image:

![Color Source Image](http://imgur.com/2KzkN8p.jpg "Color Source Image")

Color Target Image:

![Target Image](http://imgur.com/VyaVBkQ.jpg "Target Image")

Result:

![Result](http://imgur.com/kiNBR57.jpg "Result")

*Photographs by Steve McCurry*
