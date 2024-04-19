import tensorflow as tf
import random
import numpy as np
from keras.backend import sqrt, sum, square, maximum, epsilon


# This function finds a positive pair of images within a set of images
# (Two images of the same person)
def positive_pair(X, number_of_people):
    picture1_index = random.randint(0,9)
    picture2_index = picture1_index
    while picture2_index == picture1_index:
        picture2_index = random.randint(0,9)
    random_person_index = random.randint(0,number_of_people - 1)
    picture1_index = random_person_index * 10 + picture1_index
    picture2_index = random_person_index * 10 + picture2_index
    #return np.array((X[picture1_index], X[picture2_index]))
    return X[picture1_index], X[picture2_index]

# This function finds a negative pair of images within a set of images
# (Two images of different people)
def negative_pair(X, number_of_people):
    person1_index = random.randint(0,number_of_people - 1)
    person2_index = person1_index
    while person2_index == person1_index:
        person2_index = random.randint(0,number_of_people - 1)
    picture1_index = random.randint(0,9)
    picture2_index = random.randint(0,9)
    picture1_index = person1_index * 10 + picture1_index
    picture2_index = person2_index * 10 + picture2_index
    return X[picture1_index], X[picture2_index]
    #return np.array((X[picture1_index], X[picture2_index]))

# This function creates a list of random input pairs (X) and a list of their labels (Y) from a set of images.
# It alternates between adding a positive and negative pair of images to X with matching labels to Y.
def create_X_pairs(X, number_of_people, size):
    X_pairs, X_pairs_labels = [], []
    for i in range(size):
        if i % 2 == 0:
            X_pairs.append(positive_pair(X, number_of_people))
            X_pairs_labels.append(1)
        else:
            X_pairs.append(negative_pair(X,number_of_people))
            X_pairs_labels.append(0)
    return (X_pairs, X_pairs_labels)

# For the following two functions, I am using the code provided by J. Loy. Implementing
# a Facial Recognition System with Neural Networks. Neural Network Projects with Python.
# Packt Publishing, February 2019.[1]

# This function calculates the euclidean distance between two outputs
def euclidean_distance(outputs):
    out1, out2 = outputs
    sum_square = sqrt(sum(square(out1 - out2), axis=1, keepdims=True))
    return sqrt(maximum(sum_square, epsilon()))

# This function calculates the contrastive loss
def contrastive_loss(true_pair_label, distance, margin=1.0):
    true_pair_label = tf.cast(true_pair_label, tf.float32)
    loss = true_pair_label * tf.square(distance) + (1 - true_pair_label) * tf.square(tf.maximum(margin - distance, 0))
    return loss

