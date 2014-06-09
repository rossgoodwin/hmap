# image histogram remapping

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
width = srcImg.size[0]
height = srcImg.size[1]

#load pixel maps
srcPix = srcImg.load()
tgtPix = tgtImg.load()

#Get histograms of the images
#only take the first 256 values for now since they're B&W
srcHist = srcImg.histogram()[:256]
tgtHist = tgtImg.histogram()[:256]

#make value list
pxlsByVal = []
for _ in range(256):
    pxlsByVal.append([])

for i in range(width):
    for j in range(height):
        value = srcPix[i, j][0]
        pxlsByVal[value].append((i,j))

print "pxlsByVal created..."

equalBins = []
excessBins = []
deficitBins = []

#sort bins into lists
for i in range(len(srcHist)):
    if srcHist[i] < tgtHist[i]:
        deficitBins.append(i)
    elif srcHist[i] > tgtHist[i]:
        excessBins.append(i)
    elif srcHist[i] == tgtHist[i]:
        equalBins.append(i)

print "list of excess and deficit values created..."

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
        pxlsByVal[tgtVal].append(pxl)

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
        print "On value", curValue, "with", excess, "excess pixels"
    while excess > 0:
        tgtValue = deficitBins[0]
        deficit = tgtHist[tgtValue] - srcHist[tgtValue]
        if excess > deficit :
            nToMove = excess - deficit
            deficitBins = deficitBins[1:]
        else:
            nToMove = excess
            if deficit == excess:
                deficitBins = deficitBins[1:]

        change_n_pixels_smooth(curValue,tgtValue,nToMove)
        excess -= nToMove

srcImg.show()
