import numpy as np
import cv2
import face_recognition
import os

cap = cv2.VideoCapture(0)
cap.set(3, 640) # width
cap.set(4,480) # height
cap.set(10, 150) # brightness

myColours = [[41,154,0,113,255,255],[0,130,130,17,255,255]] # (h_min,s_min,v_min,h_max,s_max,v_max)
myColourValues = [(255,0,0), (0,111,255)]

myPoints = [] # (x,y,colourID)

def findContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            # cv2.drawContours(Result, cnt, -1, (0,255,0), 3)
            epsilon = 0.02 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            x,y,w,h = cv2.boundingRect(approx)
    return x+w//2,y

def findColors(img, myColours, myColourValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for colour in myColours:
        lower = np.array(colour[0:3])
        upper = np.array(colour[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x,y = findContours(mask)
        cv2.circle(Result, (x,y), 10, myColourValues[count], cv2.FILLED)
        if x!= 0 and y!=0:
            newPoints.append((x,y,count))
        count+=1
        # cv2.imshow(str(myColourValues[0]), Result)
    return newPoints

def drawOnCanvas(myPoints, myColourValues):
    for points in myPoints:
        cv2.circle(Result, (points[0], points[1]), 10, myColourValues[points[2]], cv2.FILLED)

while True:
    _ , img = cap.read()
    Result = img.copy()
    newPoints = findColors(img, myColours, myColourValues)

    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColourValues)

    cv2.imshow("img", Result)
    cv2.waitKey(1)