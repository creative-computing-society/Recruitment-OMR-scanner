import cv2
import numpy as np
import utils
import pytesseract
import os
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

questions=10
choices =5
img = cv2.imread("Sheet1.jpg")
height,width=700,700
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
NamePoints = utils.getCornerPoints(rectCon[1])
RollNumberPoints = utils.getCornerPoints(rectCon[2])

if biggestContour.size != 0 and NamePoints.size != 0:
    cv2.drawContours(imgBiggestContours,biggestContour,-1,(0,255,0),20)
    cv2.drawContours(imgBiggestContours,NamePoints,-1,(255,0,0),20)
    cv2.drawContours(imgBiggestContours,RollNumberPoints, -1, (0, 0,255), 20)

    biggestContour=utils.reorder(biggestContour)
    NamePoints=utils.reorder(NamePoints)
    RollNumberPoints=utils.reorder(RollNumberPoints)

    pt1 = np.float32(biggestContour)
    pt2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
    matrix = cv2.getPerspectiveTransform(pt1,pt2)
    imgWarpColored= cv2.warpPerspective(img,matrix,(width,height))

    pt01 = np.float32(NamePoints)
    pt02 = np.float32([[0,0],[450,0],[0,50],[450,50]])
    matrix0 = cv2.getPerspectiveTransform(pt01,pt02)
    imgNameDisplay = cv2.warpPerspective(img,matrix0,(450,50))
    imgNameDisplay = cv2.resize(imgNameDisplay,(2250,250))
    cv2.imshow("Name",imgNameDisplay)

    orb = cv2.ORB_create()
    kp1, des1 = orb.detectAndCompute(imgNameDisplay, None)
    impKp1 = cv2.drawKeypoints(imgNameDisplay,kp1,None)
    cv2.imshow("KeyPoints Image",impKp1)

    pt11 = np.float32(RollNumberPoints)
    pt12 = np.float32([[0,0],[300,0],[0,50],[300,50]])
    matrix1 = cv2.getPerspectiveTransform(pt11,pt12)
    RollNumberDisplay= cv2.warpPerspective(img,matrix1,(300,50))
    cv2.imshow("Roll Number",RollNumberDisplay)

    imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
    imgThresh = cv2.threshold(imgWarpGray,150,255,cv2.THRESH_BINARY_INV)[1]

    boxes = utils.splitBoxes(imgThresh)
    #cv2.imshow("Test",boxes[2])


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
    ''' idher excel ka '''

'''data = []
with open('results.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(data)'''

imgArray= ([img,imgGray,imgBlur,imgCanny],[imgContours,imgBiggestContours,imgWarpColored,imgThresh])

imgStacked= utils.stackImages(imgArray,0.5)


cv2.imshow("Original",imgStacked)
cv2.waitKey(0)