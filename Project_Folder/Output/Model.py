
import matplotlib.pyplot as plt
import warnings
import seaborn as sns
import numpy
import math
warnings.filterwarnings('ignore')
batch_size = 16



from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale=1/255)


train_generator = train_datagen.flow_from_directory('Dataset/Train',target_size=(224, 224), batch_size=batch_size,
                                                    classes = ['aom', 'csom', 'earwax', 'normal', 'otitisexterna', 'tympanoskleros'],class_mode='categorical')

test_datagen = ImageDataGenerator(rescale=1/255)


test_generator = test_datagen.flow_from_directory('Dataset/Train', target_size=(224, 224), batch_size=batch_size,
                                                  classes = ['aom', 'csom', 'earwax', 'normal', 'otitisexterna', 'tympanoskleros'],
                                                  class_mode='categorical',shuffle=False)


import tensorflow as tf

model = tf.keras.models.Sequential([

    # The first convolution
    tf.keras.layers.Conv2D(16, (3,3), activation='relu', input_shape=(224, 224, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    # The second convolution
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    # The third convolution
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    # The fourth convolution
    tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    # The fifth convolution
    tf.keras.layers.Conv2D(256, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    # Flatten the results to feed into a dense layer
    tf.keras.layers.Flatten(),
    # 128 neuron in the fully-connected layer
    tf.keras.layers.Dense(512, activation='relu'),
    # 5 output neurons for 3 classes with the softmax activation
    tf.keras.layers.Dense(6, activation='softmax')
])

model.summary()

from tensorflow.keras.optimizers import RMSprop
early = tf.keras.callbacks.EarlyStopping(monitor='val_loss',patience=5)
model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.001),metrics=['accuracy'])

total_sample=train_generator.n

n_epochs = 30

history = model.fit_generator(train_generator,steps_per_epoch=int(total_sample/batch_size),epochs=n_epochs)


model.save('model.h5')



acc = history.history['accuracy']

loss = history.history['loss']

epochs = range(1, len(acc) + 1)

# Train and validation accuracy
plt.plot(epochs, acc, 'b', label=' accurarcy')
plt.title('accurarcy')
plt.legend()

plt.figure()

# Train and validation loss
plt.plot(epochs, loss, 'b', label=' loss')
plt.title('  loss')
plt.legend()
plt.show()


from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
test_steps_per_epoch =  math.ceil(test_generator.samples / test_generator.batch_size)

predictions = model.predict_generator(test_generator, steps=test_steps_per_epoch)
# Get most likely class
predicted_classes = numpy.argmax(predictions, axis=1)

true_classes = test_generator.classes
class_labels = list(test_generator.class_indices.keys())

print('Classification Report')


report = classification_report(true_classes, predicted_classes, target_names=class_labels)
print(report)

print('confusion matrix')

confusion_matrix= confusion_matrix(true_classes, predicted_classes)

print(confusion_matrix)


sns.heatmap(confusion_matrix, annot = True)
plt.show()