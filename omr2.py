import cv2
import cv2
import numpy as np
import utils
import os

questions=10
choices =5
img = cv2.imread("Sheet2.jpg")
height,width=720,720
ans = [1,2,0,1,4,1,2,0,1,4]


img=cv2.resize(img,(height,width))
imgContours=img.copy()
imgBiggestContours = img.copy()
imgBlank=np.zeros_like(img)
imgGray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur= cv2.GaussianBlur(imgGray,(5,5),1)
imgCanny= cv2.Canny(imgBlur,10,50)
countours, hierarchy = cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cv2.drawContours(imgContours,countours,-1,(0,255,0),10)


rectCon = utils.rectCountour(countours)
biggestContour = utils.getCornerPoints(rectCon[0])
RollNumberPoints = utils.getCornerPoints(rectCon[1])


if biggestContour.size != 0 and RollNumberPoints.size != 0:
    myData=[]
    cv2.drawContours(imgBiggestContours,biggestContour,-1,(0,255,0),20)
    cv2.drawContours(imgBiggestContours,RollNumberPoints, -1, (0, 0,255), 20)

    biggestContour=utils.reorder(biggestContour)
    RollNumberPoints=utils.reorder(RollNumberPoints)

    pt1 = np.float32(biggestContour)
    pt2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
    matrix = cv2.getPerspectiveTransform(pt1,pt2)
    imgWarpColored= cv2.warpPerspective(img,matrix,(width,height))

    pt11 = np.float32(RollNumberPoints)
    pt12 = np.float32([[0,0],[width,0],[0,width],[height,width]])
    matrix1 = cv2.getPerspectiveTransform(pt11,pt12)
    imgWarpColored1= cv2.warpPerspective(img,matrix1,(height,width))
    cv2.imshow("Roll Number",imgWarpColored1)

    imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
    imgThresh = cv2.threshold(imgWarpGray,150,255,cv2.THRESH_BINARY_INV)[1]

    boxes = utils.splitBoxes(imgThresh)
    myPixelVal = np.zeros((questions,choices))
    countC = 0
    countR = 0
    for image in boxes:
        totalPixels = cv2.countNonZero(image)
        myPixelVal[countR][countC] = totalPixels
        countC+=1
        if(countC == choices):
            countR+=1
            countC=0
    #print(myPixelVal)

    myIndex = []
    for x in range(0,questions):
        array = myPixelVal[x]
        #print(array)
        myIndexVal = np.where(array ==np.amax(array))
        #print(myIndexVal[0])
        myIndex.append(myIndexVal[0][0])
    print(myIndex)

    grading=[]
    for x in range(0,questions):
        if ans[x] == myIndex[x]:
            grading.append(1)
        else:
            grading.append(0)
    print(grading)
    score = sum(grading)
    print(score)
    ''' idher excel ka '''

    #RollNumberDisplay = cv2.resize(imgWarpColored1, (1000, 1000))
    imgWarpGray1 = cv2.cvtColor(imgWarpColored1,cv2.COLOR_BGR2GRAY)
    imgThresh1 = cv2.threshold(imgWarpGray1,150,255,cv2.THRESH_BINARY_INV)[1]

    cv2.imshow("Pic",imgThresh1)

    boxes1 = utils.splitBoxes1(imgThresh1)
    myPixelVal1 = np.zeros((9,10))
    countC1 = 0
    countR1 = 0
    for image1 in boxes1:
        totalPixels1 = cv2.countNonZero(image1)
        myPixelVal1[countR1][countC1] = totalPixels1
        countC1+=1
        if(countC1 == 10):
            countR1+=1
            countC1=0

    myIndex1 = []
    for x1 in range(0,9):
        array1 = myPixelVal1[x1]
        #print(array)
        myIndexVal1 = np.where(array1==np.amax(array1))
        #print(myIndexVal[0])
        myIndex1.append(myIndexVal1[0][0])
    print(myIndex1)
'''data = []
with open('results.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(data)'''

imgArray= ([img,imgGray,imgBlur,imgCanny],[imgContours,imgBiggestContours,imgWarpColored,imgThresh])

imgStacked= utils.stackImages(imgArray,0.5)


cv2.imshow("Original",imgStacked)
cv2.waitKey(0)