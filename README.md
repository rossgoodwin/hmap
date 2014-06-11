Hmap
====

An image histogram remapping script written in Python 2.7 by [Anthony Kesich](http://akesich.com) and [Ross Goodwin](http://rossgoodwin.com). Changes source image so that source image's histogram matches target image's histogram. Requires PIL/Pillow:

    $ sudo pip install Pillow

To run Hmap, cd into the directory where the hmap.py (for black and white images) or hmap_c.py (for color images) is located. Ensure source and target images have the same height and width dimensions (in pixels), and place them in the directory. Run the script with 2 additional arguments (source and target image files) as shown in the following example.

Example:

    $ sudo python hmap_c.py source_image.jpg target_image.jpg


Source Image:

![Source Image](http://imgur.com/MGCUWZo.jpg "Source Image")


Target Image:

![Target Image](http://imgur.com/vuGrjAY.jpg "Target Image")


Result:

![Result](http://imgur.com/KavoDjf.jpg "Result")
