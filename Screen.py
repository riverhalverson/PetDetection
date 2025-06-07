import os
import sys
import cv2

class Display:
    frame = None
    capture = None
    ret = False
    cameraInputIndex = 0
    cameraImgResW = 0
    cameraImgResH = 0

    def setResolution(self, width, height):
        Display.cameraImgResW = width
        Display.cameraImgResH = height

    def setCameraInputIndex(self, index):
        Display.cameraInputIndex = index

    def initializeCamera(self):
        Display.capture = cv2.VideoCapture(Display.cameraInputIndex)
        Display.ret = Display.capture.set(3, Display.cameraImgResW)
        Display.ret = Display.capture.set(4, Display.cameraImgResH)
        
    def getFrame(self):
        Display.ret, Display.frame = Display.capture.read()

        if (Display.frame is None) or (not Display.ret):
            print('Error: Problem with camera')
        else:
            return Display.frame
        
    def drawBox(self, frame, xMin, yMin, xMax, yMax, color, shape):
        cv2.rectangle(frame, (xMin,yMin), (xMax,yMax), color, shape)
        
    def drawLabel(self, frame, className, confidenceLevel, xMin, yMin, xMax, yMax, shape, color):
        cv2.rectangle(frame, (xMin,yMin), (xMax,yMax), color, shape)
        
        label = f'{className}: {int(confidenceLevel*100)}%'
        labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1) # Get font size
        label_yMin = max(yMin, labelSize[1] + 10) # Dont draw label too close to top of window
        cv2.rectangle(frame, (xMin, label_yMin - labelSize[1] - 10), (xMin + labelSize[0], label_yMin + baseLine - 10),
                     color, cv2.FILLED) # Draw white box to put label in
        cv2.putText(frame, label, (xMin, label_yMin - 7),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0,), 1) # Draw label text

    def showResults(self, frame):
        cv2.imshow('Pet Detector 9000', frame)

    def cleanUp(self):
        Display.capture.release()
        cv2.destroyAllWindows()
        