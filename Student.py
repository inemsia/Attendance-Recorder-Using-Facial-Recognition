import os, sys
sys.path.append(os.getcwd())
from Preprocess import Preprocess
import os
import cv2

# This class represents each student. It allows us to access student information such as their pictures.
# It also allows us to modify their attendance state.
class Student:

    # Constructor
    def __init__(self, name, folder_path):
        self.name = name # student name
        self.folder_path = folder_path # path where pictures are stored
        self.attendance = False # true if student is present

    # Returns name of student
    def get_name(self):
        return self.name

    # Returns student's folder path
    def get_path(self):
        return self.folder_path

    # Returns black and white versions of stored pictures
    def get_pictures(self):
        pictures = []
        if not os.path.isdir(self.folder_path):
            print("No folder was created for this student yet.")
            return []
        else:
            pics_names = os.listdir(self.folder_path)
            for pic_name in pics_names:
                pic_path = self.folder_path + "/" + pic_name
                picture = cv2.imread(pic_path)
                picture = cv2.cvtColor(picture, cv2.COLOR_BGR2GRAY)
                pictures.append(picture)
            return pictures

    # Returns pictures converted into numpy arrays
    def get_array_of_pictures(self):
        pictures = self.get_pictures()
        return [Preprocess.image_to_array(picture) for picture in pictures]

    # Sets the attendance of the student to value
    def set_attendance(self, value):
        self.attendance = value

#%%
