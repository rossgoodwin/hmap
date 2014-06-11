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
#Now taking 3 different histograms for each image; 1 for each color channel
srcHist_R = srcImg.histogram()[:256]
tgtHist_R = tgtImg.histogram()[:256]

srcHist_G = srcImg.histogram()[256:512]
tgtHist_G = tgtImg.histogram()[256:512]

srcHist_B = srcImg.histogram()[512:]
tgtHist_B = tgtImg.histogram()[512:]

#make value lists
pxlsByVal_R = []
for _ in range(256):
    pxlsByVal_R.append([])

for i in range(width):
    for j in range(height):
        value = srcPix[i, j][0]
        pxlsByVal_R[value].append((i,j))

pxlsByVal_G = []
for _ in range(256):
    pxlsByVal_G.append([])

for i in range(width):
    for j in range(height):
        value = srcPix[i, j][1]
        pxlsByVal_G[value].append((i,j))

pxlsByVal_B = []
for _ in range(256):
    pxlsByVal_B.append([])

for i in range(width):
    for j in range(height):
        value = srcPix[i, j][2]
        pxlsByVal_B[value].append((i,j))

print "pxlsByVal created..."

equalBins_R = []
excessBins_R = []
deficitBins_R = []

equalBins_G = []
excessBins_G = []
deficitBins_G = []

equalBins_B = []
excessBins_B = []
deficitBins_B = []

#sort bins into lists
for i in range(256):
    if srcHist_R[i] < tgtHist_R[i]:
        deficitBins_R.append(i)
    elif srcHist_R[i] > tgtHist_R[i]:
        excessBins_R.append(i)
    elif srcHist_R[i] == tgtHist_R[i]:
        equalBins_R.append(i)
        
for i in range(256):
    if srcHist_G[i] < tgtHist_G[i]:
        deficitBins_G.append(i)
    elif srcHist_G[i] > tgtHist_G[i]:
        excessBins_G.append(i)
    elif srcHist_G[i] == tgtHist_G[i]:
        equalBins_G.append(i)

for i in range(256):
    if srcHist_B[i] < tgtHist_B[i]:
        deficitBins_B.append(i)
    elif srcHist_B[i] > tgtHist_B[i]:
        excessBins_B.append(i)
    elif srcHist_B[i] == tgtHist_B[i]:
        equalBins_B.append(i)

print "list of excess and deficit values created..."


#change one pixel function - R
def change_n_pixels_R(curVal, tgtVal, nToChange):
    #find a pixel to change
    candidatePxls = pxlsByVal_R[curVal]
    chosenPxls = random.sample(candidatePxls, nToChange)

    #change the pixel
    for pxl in chosenPxls:
        srcPix[pxl] = (tgtVal, srcPix[pxl][1], srcPix[pxl][2])
        #update pixel list
        pxlsByVal_R[curVal].remove(pxl)
        pxlsByVal_R[tgtVal].append(pxl)

    #update the histograms
    srcHist_R[curVal] -= nToChange
    srcHist_R[tgtVal] += nToChange


#change one pixel function - G
def change_n_pixels_G(curVal, tgtVal, nToChange):
    #find a pixel to change
    candidatePxls = pxlsByVal_G[curVal]
    chosenPxls = random.sample(candidatePxls, nToChange)

    #change the pixel
    for pxl in chosenPxls:
        srcPix[pxl] = (srcPix[pxl][0], tgtVal, srcPix[pxl][2])
        #update pixel list
        pxlsByVal_G[curVal].remove(pxl)
        pxlsByVal_G[tgtVal].append(pxl)

    #update the histograms
    srcHist_G[curVal] -= nToChange
    srcHist_G[tgtVal] += nToChange


#change one pixel function - B
def change_n_pixels_B(curVal, tgtVal, nToChange):
    #find a pixel to change
    candidatePxls = pxlsByVal_B[curVal]
    chosenPxls = random.sample(candidatePxls, nToChange)

    #change the pixel
    for pxl in chosenPxls:
        srcPix[pxl] = (srcPix[pxl][0], srcPix[pxl][1], tgtVal)
        #update pixel list
        pxlsByVal_B[curVal].remove(pxl)
        pxlsByVal_B[tgtVal].append(pxl)

    #update the histograms
    srcHist_B[curVal] -= nToChange
    srcHist_B[tgtVal] += nToChange


#change one pixel function - R
def change_n_pixels_smooth_R(curVal, tgtVal, nToChange):
    Nincrements = abs(curVal - tgtVal)
    for inc in range(Nincrements):
        # This part was throwing IndexErrors, so I adjusted it
        if tgtVal > curVal:
            try:
                change_n_pixels_R(curVal+inc, curVal+inc+1, nToChange)
            except IndexError:
                pass
        else:
            try:
                change_n_pixels_R(curVal-inc, curVal-inc-1, nToChange)
            except IndexError:
                pass


#change one pixel function - G
def change_n_pixels_smooth_G(curVal, tgtVal, nToChange):
    Nincrements = abs(curVal - tgtVal)
    for inc in range(Nincrements):
        # This part was throwing IndexErrors, so I adjusted it
        if tgtVal > curVal:
            try:
                change_n_pixels_G(curVal+inc, curVal+inc+1, nToChange)
            except IndexError:
                pass
        else:
            try:
                change_n_pixels_G(curVal-inc, curVal-inc-1, nToChange)
            except IndexError:
                pass


#change one pixel function - B
def change_n_pixels_smooth_B(curVal, tgtVal, nToChange):
    Nincrements = abs(curVal - tgtVal)
    for inc in range(Nincrements):
        # This part was throwing IndexErrors, so I adjusted it
        if tgtVal > curVal:
            try:
                change_n_pixels_B(curVal+inc, curVal+inc+1, nToChange)
            except IndexError:
                pass
        else:
            try:
                change_n_pixels_B(curVal-inc, curVal-inc-1, nToChange)
            except IndexError:
                pass


#move pixels in excess bins to deficit bins - R
for curValue in excessBins_R:
    excess = srcHist_R[curValue] - tgtHist_R[curValue]
    if curValue % 5 == 0:
        print "On R value", curValue, "with", excess, "excess pixels"
    while excess > 0:
        tgtValue = deficitBins_R[0]
        deficit = tgtHist_R[tgtValue] - srcHist_R[tgtValue]
        if excess > deficit :
            nToMove = excess - deficit
            deficitBins_R = deficitBins_R[1:]
        else:
            nToMove = excess
            if deficit == excess:
                deficitBins_R = deficitBins_R[1:]

        change_n_pixels_smooth_R(curValue,tgtValue,nToMove)
        excess -= nToMove


#move pixels in excess bins to deficit bins - G
for curValue in excessBins_G:
    excess = srcHist_G[curValue] - tgtHist_G[curValue]
    if curValue % 5 == 0:
        print "On G value", curValue, "with", excess, "excess pixels"
    while excess > 0:
        tgtValue = deficitBins_G[0]
        deficit = tgtHist_G[tgtValue] - srcHist_G[tgtValue]
        if excess > deficit :
            nToMove = excess - deficit
            deficitBins_G = deficitBins_G[1:]
        else:
            nToMove = excess
            if deficit == excess:
                deficitBins_G = deficitBins_G[1:]

        change_n_pixels_smooth_G(curValue,tgtValue,nToMove)
        excess -= nToMove
        

#move pixels in excess bins to deficit bins - B
for curValue in excessBins_B:
    excess = srcHist_B[curValue] - tgtHist_B[curValue]
    if curValue % 5 == 0:
        print "On B value", curValue, "with", excess, "excess pixels"
    while excess > 0:
        tgtValue = deficitBins_B[0]
        deficit = tgtHist_B[tgtValue] - srcHist_B[tgtValue]
        if excess > deficit :
            nToMove = excess - deficit
            deficitBins_B = deficitBins_B[1:]
        else:
            nToMove = excess
            if deficit == excess:
                deficitBins_B = deficitBins_B[1:]

        change_n_pixels_smooth_B(curValue,tgtValue,nToMove)
        excess -= nToMove

srcImg.show()
