# image histogram remapping

from PIL import Image
import random

#image data - use size method to get automatically
width = 1600
height = 1280

#load our source and target images
srcImg = Image.open("one.jpg")
tgtImg = Image.open("two.jpg")

srcImg.show()
tgtImg.show()

#load pixel maps
srcPix = srcImg.load()
tgtPix = tgtImg.load()

#Get histograms of the images
#only take the first 245 values for now since they're B&W
srcHist = srcImg.histogram()[:256]
tgtHist = tgtImg.histogram()[:256]

#make value list
srcValuelist = []
pxlsByVal = [ ]
for _ in range(256):
    pxlsByVal.append([])

for i in range(width):
    for j in range(height):
        value = srcPix[i, j][0]
        pxlsByVal[value].append((i,j))

print "pxlsByVal created"

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

print "list of excess and deficit values created."

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
    return


#move pixels in excess bins to deficit bins
for curValue in excessBins:
    excess = srcHist[curValue] - tgtHist[curValue]
    for _ in range(excess):
        tgtValue = deficitBins[0]
        change_one_pixel(curValue,tgtValue)
        if srcHist[tgtValue] == tgtHist[tgtValue]:
            deficitBins = deficitBins[1:]

srcImg.show()
