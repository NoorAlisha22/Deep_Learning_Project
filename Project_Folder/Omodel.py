# importing libraries

import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt
import os
import random
import glob  # to find files
import seaborn as sns
# Seaborn library for bar chart
#import seaborn as sns

# Libraries for TensorFlow
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing import image
from tensorflow.keras import models, layers

# Library for Transfer Learning
from tensorflow.keras.applications import VGG16
from keras.applications.densenet import preprocess_input

print("Importing libraries completed.")

path = 'Dataset/'

train_folder = path + "Train/"


# variables for image size
img_width = 224
img_height = 224

# variable for model
batch_size = 16
epochs = 3


print("Variable declaration completed.")

# listing the folders containing images

# Train Dataset
train_class_names = os.listdir(train_folder)
print("Train class names: %s" % (train_class_names))
# print("\n")

print("\nDataset class name listing completed.")

# declaration of functions


# Declaring variables
x = []  # to store array value of the images
y = []  # to store the labels of the images

for folder in os.listdir(train_folder):
    image_list = os.listdir(train_folder + "/" + folder)
    for img_name in image_list:
        # Loading images
        img = image.load_img(train_folder + "/" + folder + "/" + img_name, target_size=(img_width, img_height))

        # Converting to arrary
        img = image.img_to_array(img)

        # Transfer Learning: this is to apply preprocess of VGG16 model to our images before passing it to VGG16
        img = preprocess_input(img)  # Optional step

        # Appending the arrarys
        x.append(img)  # appending image array
        y.append(train_class_names.index(folder))  # appending class index to the array

print("Preparing Training Dataset Completed.")

# Training Dataset
print("Training Dataset")

x = np.array(x)  # Converting to np arrary to pass to the model
print(x.shape)

y = to_categorical(y)  # onehot encoding of the labels
# print(y)
print(y.shape)

# ===========


print("Summary of default DenseNet model.\n")

# we are using VGG16 for transfer learnin here. So we have imported it
from tensorflow.keras.applications import DenseNet121

model = DenseNet121(weights='imagenet')
model.summary()

print("Summary of Custom DenseNet model.\n")
input_layer = layers.Input(shape=(img_width, img_height, 3))
model = DenseNet121(weights='imagenet', input_tensor=input_layer, include_top=False)
model.summary()
last_layer = model.output
flatten = layers.Flatten()(last_layer)
output_layer = layers.Dense(6, activation='softmax')(flatten)
model = models.Model(inputs=input_layer, outputs=output_layer)

model.summary()
for layer in model.layers[:-1]:
    layer.trainable = False
model.summary()

from sklearn.model_selection import train_test_split

xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2, random_state=0)
print("Splitting data for train and test completed.")

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

print("Model compilation completed.")

history2 = model.fit(xtrain, ytrain, epochs=epochs, batch_size=batch_size, verbose=True, validation_data=(xtrain, ytrain))

print("Fitting the model completed.")

model.save("model.h5")

acc = history2.history['accuracy']
val_acc = history2.history['val_accuracy']
epochs = range(len(acc))

plt.plot(epochs, acc, label='Training Accuracy')
plt.plot(epochs, val_acc, label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.grid(True)
plt.show()

# Plot Model Loss
loss_train = history2.history['loss']
loss_val = history2.history['val_loss']
plt.plot(epochs, loss_train, label='Training Loss')
plt.plot(epochs, loss_val, label='Validation Loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.grid(True)
plt.show()

y_pred = model.predict(xtrain)
y_pred = np.argmax(y_pred, axis=1)
print(y_pred)
y_test=np.argmax(ytrain, axis=1)
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
print(cm)

sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix of DenseNet121 ')
plt.show()