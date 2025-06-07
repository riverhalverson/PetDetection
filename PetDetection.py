import os
import sys
import cv2
import pygame.mixer
from datetime import datetime
from ultralytics import YOLO
from Screen import Display
from AI import Prompts
from playsound import playsound
import asyncio

from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

def main():
    # Define path to model and other user variables
    model_path = 'Model/my_model/my_model.pt'  # Path to model
    min_thresh = 0.50  # Minimum detection threshold


    display = Display()
    display.setResolution(1920, 1080)

    # Check for valid model file and that it exists
    if (not os.path.exists(model_path)):
        print('Error: Model path is invalid or model was not found')
        sys.exit()

    # Load the model into memory and get labelmap
    model = YOLO(model_path, task='detect')
    labels = model.names

    # Initialize camera
    display.initializeCamera()

    # Initialize pygame for audio
    pygame.mixer.init()

    # Set bounding box colors.
    bbox_colors = [(164, 120, 87), (68, 148, 228), (93, 97, 209)]

    # Initialize variable to hold every pet detected in this frame
    currentPetName = ""
    petsDetected = []
    speaking = False
    detectedTime = 0

    # Begin inference loop
    while True:

        # Grab frame from counter
        frame = display.getFrame()

        # Run inference on frame with tracking enabled (tracking helps object to be consistently detected in each frame)
        results = model.track(frame, verbose=False)

        # Extract results
        detections = results[0].boxes

        # Go through each detection and get bbox coords, confidence and class
        for i in range(len(detections)):

            # Get bounding box coordinates
            # Ultralytics returns results in Tensor format, which have to be converted to a regular Python array
            xyxy_tensor = detections[i].xyxy.cpu()  # Detections in Tensor format in CPU memory
            xyxy = xyxy_tensor.numpy().squeeze()  # Convert tensors to Numpy array
            xMin, yMin, xMax, yMax = xyxy.astype(int)  # Extract individual coordinates and convert to int

            # Get bounding box class ID and name
            classidx = int(detections[i].cls.item())
            className = labels[classidx]

            # Get bounding box confidence
            confidence = detections[i].conf.item()

            # Draw box around detected pet if confidence is high enough
            if confidence > 0.7:
                # Draw box around pet
                color = bbox_colors[classidx % 10]
                display.drawLabel(frame, className, confidence, xMin, yMin, xMax, yMax, 2, color)

                # Add pet to list of detected pets
                petsDetected.append(className)

                key = cv2.waitKey(5)

        #display.showResults(frame)  # Display image

        # If array has filled up, check to see if only one unique pet
        if (len(petsDetected) == 60) and speaking == False:
            currentPetName = getCurrentPet(petsDetected)

            # Clean up array for next detection
            petsDetected = []

            if(currentPetName != ""):
                '''
                currentTime = datetime.now()
                minute = currentTime.minute
                detectedTime = minute
                speaking = True

                prompt = Prompts()
                speechFile = prompt.getPetSonaVoice(currentPetName)
                sound = pygame.mixer.Sound(speechFile)
                sound.play()
                #playsound(speechFile)
                '''
                prompt = Prompts()
                asyncio.run(prompt.getPetSonaVoiceRT(currentPetName))


        currentTime = datetime.now()
        minute = currentTime.minute
        if(minute > detectedTime):
            speaking = False

        display.showResults(frame)  # Display image

        key = cv2.waitKey(5)

        if key == ord('q') or key == ord('Q'):  # Press 'q' to quit
            break

    # Clean up
    display.cleanUp()

# Gets current pet that has been on screen for roughly 30 seconds
def getCurrentPet(petArray):
    petFound = False
    petName = ""

    for index, pet in enumerate(petArray):
        if petArray[index] == petArray[0]:
            petFound = True
        else:
            petFound = False

    if petFound:
        petName = petArray[0]
        print("Found " + petName)

    return petName

def sendPrompt(petName):
    if(petName != ""):
        prompt = Prompts()
        prompt.getPetSona(petName)

    return


if __name__ == '__main__':
    main()