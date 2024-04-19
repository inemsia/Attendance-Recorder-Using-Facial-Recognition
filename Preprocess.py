import cv2
import numpy as np

# This is a class that helps with preprocessing
class Preprocess:

    # Performs steps of preprocessing
    @staticmethod
    def preprocessed_image(img):
        if img is not None:
            # Resizes image into appropriate size for model
            img = cv2.resize(img, (92, 112))
            # Blurs image to decrease pixelation
            img = cv2.GaussianBlur(img, (3, 3), 0)
        return img

    # Converts image to numpy array
    @staticmethod
    def image_to_array(img):
        if img is not None:
            img = np.array(img)
            img = np.expand_dims(img, axis=2)
            img = img / 255.0

        return img

    # Converts set of images to set of numpy arrays
    @staticmethod
    def images_to_array(imgs):
        return [Preprocess.image_to_array(img) for img in imgs]
#%%

#%%
