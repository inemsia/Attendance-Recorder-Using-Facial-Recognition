# Attendance-Recorder-Using-Facial-Recognition
For this project, we are building an attendance recorder web application using facial recognition. The goal is to use the webcam of the computer to take input of attendees, and scan data from their faces to add the people that walk through the camera frame. The project makes use of Siamese Neural Networks to achieve this. 

## What was done
- Importing the data
- Finding negative and positive pairs of images
- Splitting the data into training and testing models. Setting it to the shape the siamese network expects (pairs of images).
- Building our model

## Current Error
The loss function is outputting NaN. We will be updating the model layers as well as inspecting the code to fix this error

## Future steps
- Working on the current error of the model.
- Testing the model
- Exporting the model and creating the interface of the application in which I will be using it to record attendance with facial recognition.
