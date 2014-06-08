# image histogram remapping

from PIL import Image
import random

#image data
width = 1600
height = 1280

#load our source and target images
srcImg = Image.open("source.gif")
tgtImg = Image.open("taget.gif")

#load pixel maps
srcPix = srcImg.load()
tgtPix = tgtImg.load()

#Get histograms of the images
#only take the first 245 values for now since they're B&W
srcHist = srcImg.histogram()[:256]
tgtHist = tgtImg.histogram()[:256]

#make map of image w/ histogram data
for x in range(len(srcPix)):
    for y in range(len(srcPix[0])):
        

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

#change one pixel function
def change_one_pixel(curVal, tgtVal):
    candidatePxls = srcPxlList[curVal]
    chosenPxl = candidatePxls[random.randint(0,len(candidatePxls)-1)]
    pass


#move pixels in excess bins to deficit bins
for curValue in excessBins:
    excess = srcHist[curValue] - tgtHist[curValue]
    for _ in range(excess):
        targetValue = deficitBins[0]
        change_one_pixel(curValue,tgtValue)
        if srcHist[tgtValue] == tgtHist[tgtValue]:
            deficitBins = deficitBins[1:]
