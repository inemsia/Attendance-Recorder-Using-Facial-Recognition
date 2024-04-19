import os, sys

sys.path.append(os.getcwd())
from statistics import mean
from Preprocess import Preprocess
import numpy as np

# This class stores our model and uses it to make predictions of photos
# by comparing them to student data
class FacialRecognitionModel:
    # Constructor
    def __init__(self, students_list, model):
        self.model = model
        self.students_list = students_list

    # This function returns the similarity of a photo to a student
    # It loads all the student's pictures and compares the photo to them
    # The mean of the similarities is returned.
    def get_similiarity(self, photo, student):
        if photo is None:
            return 0
        threshold = 0.5
        true_pictures = student.get_array_of_pictures()
        if len(true_pictures == 0):
            return 0
        predictions = []
        for true_picture in true_pictures:
            if true_picture is not None:
                photo = np.array([photo])
                true_picture = np.array([true_picture])
                prediction = self.model.predict([photo, true_picture])
                predictions.append(prediction)
        if len(predictions) == 0:
            print("Array similarity is empty")
            return 0
        similarity = mean(predictions)
        if similarity > threshold:
            return similarity
        else:
            return 0

    # This function uses get_similarity to compare the photo to all students
    # The student with the highest similarity score is returned.
    def predict_photo(self, photo, students):
        # This array stores the similarity score of each student compared to photo
        students_scores = []
        for student in students.get_list_of_students():
            similarity = self.get_similiarity(photo, student)
            students_scores.append(similarity)
        maximum = 0
        position = 0
        for i in range(len(students_scores)):
            score = students_scores[i]
            if score > maximum:
                maximum = score
                position = i
        if maximum == 0:
            return ''
        else:
            student = students.get_list_of_students()[position]
            return student.get_name()



