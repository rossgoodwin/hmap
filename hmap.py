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
def change_one_pixel(curVal, tgtVal):
    #find a pixel to change
    candidatePxls = pxlsByVal[curVal]
    chosenPxl = random.choice(candidatePxls)

    #change the pixel
    srcPix[chosenPxl] = (tgtVal, tgtVal, tgtVal)

    #update the histograms
    srcHist[curVal] -= 1
    srcHist[tgtVal] += 1

    #update pixel list
    pxlsByVal[curVal].remove(chosenPxl)
    pxlsByVal[tgtVal].append(chosenPxl)
    

#change one pixel function
def change_one_pixel_smooth(curVal, tgtVal):
    Nincrements = abs(curVal - tgtVal)
    for inc in reversed(range(Nincrements)):
    # This part was throwing IndexErrors with certain images, so I adjusted it. Not sure if this is the best fix though!
        if tgtVal > curVal:
            try:
                change_one_pixel(curVal+inc,curVal+inc+1)
            except IndexError:
                pass
        else:
            try:
                change_one_pixel(curVal-inc,curVal-inc-1)
            except IndexError:
                pass


#move pixels in excess bins to deficit bins
for curValue in excessBins:
    if curValue % 5 == 0:
        print "On value", curValue
    excess = srcHist[curValue] - tgtHist[curValue]
    for _ in range(excess):
        tgtValue = deficitBins[0]
        change_one_pixel_smooth(curValue,tgtValue)
        if srcHist[tgtValue] == tgtHist[tgtValue]:
            deficitBins = deficitBins[1:]

srcImg.show()
