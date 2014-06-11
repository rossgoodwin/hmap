# image histogram remapping

from __future__ import print_function
from sys import argv
from PIL import Image
import random

script, source_image, target_image = argv

#load our source and target images
srcImg = Image.open(source_image)
tgtImg = Image.open(target_image)

srcImg.show()
tgtImg.show()

#image data
width, height = srcImg.size

#load pixel maps
srcPix = srcImg.load()
tgtPix = tgtImg.load()

#Get histograms of the images
#only take the first 256 values for now since they're B&W
srcHist = srcImg.histogram()[:256]
tgtHist = tgtImg.histogram()[:256]

#make value list
pxlsByVal = [set() for _ in range(256)]

for i in range(width):
    for j in range(height):
        value = srcPix[i, j][0]
        pxlsByVal[value].add((i, j))

print("pxlsByVal created...")

equalBins = []
excessBins = []
deficitBins = []

#sort bins into lists
for i, _ in enumerate(srcHist):
    src_i = srcHist[i]
    tgt_i = tgtHist[i]
    if src_i < tgt_i:
        deficitBins.append(i)
    elif src_i > tgt_i:
        excessBins.append(i)
    else:
        equalBins.append(i)

print("#equal bins: %s\t#excess bins: %s\t#deficit bins: %s" % tuple(
    map(len, (equalBins, excessBins, deficitBins))))


#change one pixel function
def change_n_pixels(curVal, tgtVal, nToChange):
    #find a pixel to change
    candidatePxls = pxlsByVal[curVal]
    chosenPxls = random.sample(candidatePxls, nToChange)

    #change the pixel
    for pxl in chosenPxls:
        srcPix[pxl] = (tgtVal, tgtVal, tgtVal)
        #update pixel list
        pxlsByVal[curVal].remove(pxl)
        pxlsByVal[tgtVal].add(pxl)

    #update the histograms
    srcHist[curVal] -= nToChange
    srcHist[tgtVal] += nToChange


#change one pixel function
def change_n_pixels_smooth(curVal, tgtVal, nToChange):
    Nincrements = abs(curVal - tgtVal)
    for inc in range(Nincrements):
        # This part was throwing IndexErrors, so I adjusted it
        if tgtVal > curVal:
            try:
                change_n_pixels(curVal+inc, curVal+inc+1, nToChange)
            except IndexError:
                pass
        else:
            try:
                change_n_pixels(curVal-inc, curVal-inc-1, nToChange)
            except IndexError:
                pass


#move pixels in excess bins to deficit bins
for curValue in excessBins:
    excess = srcHist[curValue] - tgtHist[curValue]
    if curValue % 5 == 0:
        print("On value", curValue, "with", excess, "excess pixels")
    while excess > 0:
        tgtValue = deficitBins[0]
        deficit = tgtHist[tgtValue] - srcHist[tgtValue]
        if excess > deficit:
            nToMove = excess - deficit
            deficitBins = deficitBins[1:]
        else:
            nToMove = excess
            if deficit == excess:
                deficitBins = deficitBins[1:]

        change_n_pixels_smooth(curValue, tgtValue, nToMove)
        excess -= nToMove

srcImg.show()
