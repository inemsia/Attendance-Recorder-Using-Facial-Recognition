import os, sys
sys.path.append(os.getcwd())
import cv2
from FacialRecognitionModel import FacialRecognitionModel
from Preprocess import Preprocess

# This class can record photos and preprocess them to be stored in the format
# required by our model. It also is meant for taking attendance.
class Camera:
    # Constructor
    def __init__(self, students_list, model):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.students_list = students_list
        self.model = FacialRecognitionModel(self.students_list, model)

    # This function uses facial detection to find the face of a student
    # in the frame and returns an array of pictures of the faces.
    # The pictures of the faces are cropped versions of the frame
    # that center the face detected.
    # The function was implemented with one person getting recorded at a time in mind.
    def record_photos(self, camera, desired_number):
        num_photos = 0
        photos = []
        while (True):
            # Initialize key input taking
            key = cv2.waitKey(1) & 0xFF
            # Quit option
            if key == ord('q'):
                camera.release()
                cv2.destroyAllWindows()
                return []
            # Get the photo at current frame
            ret, photo = camera.read()
            # Check if photo stores something
            if ret:
                # Find the position of the face
                face_position = self.find_face(photo)
                # Get cropped picture around the detected face
                face = self.get_face(photo, face_position)
                # Preprocess image of face
                preprocessed_face = Preprocess.preprocessed_image(face)

                # Add pictures of person by clicking on space bar
                if key == ord(' '):
                    photos.append(preprocessed_face)
                    num_photos += 1
                # Adding text to the displayed photo
                photo = cv2.putText(photo, f"Number Of Pictures: {num_photos + 1}", (50, 0), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (255, 255, 255), 2)
                # Drawing a square around the face
                self.draw_square(photo, face_position)
                cv2.imshow('Camera', photo)
            # End once we reach our count of pictures
            if num_photos == desired_number:
                break
        # Remove camera window
        camera.release()
        cv2.destroyAllWindows()
        return photos

    # This function uses record_photos to store the images returned
    # into the student's folder
    def add_student_pictures(self, student_name):
        camera = cv2.VideoCapture(0)
        #cv2.namedWindow("Adding student")
        self.students_list.add_student(student_name)
        photos = self.record_photos(camera, 10)
        if len(photos) == 10:
            path = self.students_list.get_path() + '/' + student_name
            for i in range(len(photos)):
                photo = photos[i]
                cv2.imwrite(f"{path}/{student_name}_{i}.jpg", photo)
        camera.release()
        cv2.destroyAllWindows()

    # This function is not fully functional
    # Intended function: The function gets the face of the student from the frame
    # and predicts which of the students from our registered students it is most similar to.
    # Once it finds the student, it sets their .attendance value to True.
    def take_attendance(self):
        # Initialize camera
        camera = cv2.VideoCapture(0)
        while (True):
            # Initialize key input taking
            key = cv2.waitKey(1) & 0xFF
            # Exit option
            if key == ord('q'):
                break
            # Get the photo at current frame
            ret, photo = camera.read()
            # Check if photo contains something
            if ret:
                face_position = self.find_face(photo)
                # Check if face_position is not null
                if face_position is not None:
                    # Draw square around face
                    self.draw_square(photo, face_position)
                    # Get cropped picture of face
                    face = self.get_face(photo, face_position)
                    if face is None:
                        continue
                    # Predict which of the students the face corresponds to
                    name = self.model.predict_photo(face, self.students_list)
                    # Add student to present students
                    student = self.students_list.get_student(name)
                    student.set_attendance(True)
                    # Draw name
                    if name != '':
                        self.draw_name(photo, face_position, '???')
                    else:
                        self.draw_name(photo, face_position, name)
            else:
                continue
        # Close camera
        camera.release()
        cv2.destroyAllWindows()

    # Referenced [1]
    # This function draws a square around the student's face using the face position
    def draw_square(self, photo, face_position):
        if(face_position is not None):
            (x, y, width, height) = face_position
            cv2.rectangle(photo, (x, y), (x + width, y + height), (255, 255, 255), 5)

    # Referenced [1]
    # This function draws the name of the student near the box
    def draw_name(self, photo, face_position, student_name):
        (x, y, width, height) = face_position
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(photo, f"student: {student_name}", (x, y+200), font, 1, (255, 255, 255), 2)

    # This function finds the position of the face on the frame
    def find_face(self, photo):
        faces_positions = self.face_cascade.detectMultiScale(photo, scaleFactor=1.3)
        if (len(faces_positions) == 1):
            return faces_positions[0]
        else:
            return None

    # This function takes the position of the face and returns
    # an image that is a cropped version of the original photo
    # around the face.
    def get_face(self, photo, face_position):
        if face_position is not None:
            (x, y, width, height) = face_position
            face = photo[y-50:y + height+50, x-50:x + width+50]
            return face
        else:
            return None


