# -*- coding: utf-8 -*-
"""CustomNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RVdcCe5OvISOw4wgpbAN9p9jTHNLJOeF

# **Implementing Gradient Descent For Neural Network (or Logistic Regression)**
"""

import numpy as np
import sklearn

def sigmoid_numpy(X):
  return 1/(1 + np.exp(-X))

def log_loss(y_true, y_predicted):
  epsilon = 1e-15
  new_y_predicted = [max(i, epsilon) for i in y_predicted]
  new_y_predicted = [min(i, 1 - epsilon) for i in new_y_predicted]
  new_y_predicted = np.array(new_y_predicted)

  return (-np.mean(y_true * np.log(new_y_predicted) + (1 - y_true) *np.log(1 - new_y_predicted)))

class myNeuralNetwork:
  def __init__(self):
    self.weight1 = 1
    self.weight2 = 1
    bias = 0


  def fit(self, X, y, parameter1, parameter2, epochs, loss_threshold):
    '''
    fit(self, X, y, parameter1, parameter2, epochs, loss_threshold)
    '''
    self.weight1, self.weight2, self.bias = self.gradient_descent(X[parameter1], X[parameter2], y, epochs, loss_threshold)

  def predict(self, X_test, parameter1, parameter2):
    weighted_sum = self.weight1 * X_test[parameter1] + self.weight2 * X_test[parameter2] + self.bias
    return sigmoid_numpy(weighted_sum)


  def gradient_descent(self, parameter1, parameter2, y_true, epochs, loss_threshold):
    weight1 = weight2 = 1
    bias = 0
    rate = 0.5
    n = len(parameter1)

    for i in range(epochs):
      weighted_sum = weight1 * parameter1 + weight2 * parameter2 + bias
      y_predicted = sigmoid_numpy(weighted_sum) # Passing it from the sigmoid function for a (0, 1) output.
      loss = log_loss(y_true, y_predicted)

      delta_weight1 = (1/n)*np.dot(np.transpose(parameter1), (y_predicted - y_true))
      delta_weight2 = (1/n)*np.dot(np.transpose(parameter2), (y_predicted - y_true))  
      delta_bias = np.mean(y_predicted - y_true) # Mean of all errors

      weight1 = weight1 - rate * delta_weight1
      weight2 = weight2 - rate * delta_weight2
      bias = bias - rate * delta_bias

      if (i % 10 == 0):
        print (f"Epoch: {i}, weight1: {weight1}, weight2: {weight2}, bias: {bias}, loss: {loss}")

      if loss <= loss_threshold:
        print (f"Broke at: \n Epoch: {i}, weight1: {weight1}, weight2: {weight2}, bias: {bias}, loss: {loss}")
        break

      return weight1, weight2, bias

"""## **Testing the Neural Network**"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import tensorflow as tf
from tensorflow import keras
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
# %matplotlib inline

dataframe = pd.read_csv("insurance_data.csv")
dataframe.head()

"""### **Splitting train and test set**"""

X_train, X_test, y_train, y_test = train_test_split(dataframe[["age", "affordibility"]], dataframe.bought_insurance, test_size = 0.2, random_state = 25)

X_train_scaled = X_train.copy()
X_train_scaled["age"] = X_train_scaled["age"] / 100

X_test_scaled = X_test.copy()
X_test_scaled["age"] = X_test_scaled["age"] / 100

model = keras.Sequential([
    keras.layers.Dense(1, input_shape = (2,), activation = "sigmoid", kernel_initializer = "ones", bias_initializer = "zeros")
])

model.compile(optimizer = "adam", loss = "binary_crossentropy", metrics = ["accuracy"])

model.fit(X_train_scaled, y_train, epochs = 500)

model.evaluate(X_test_scaled, y_test)

model.predict(X_test_scaled)

# y_test

coefficients, intercept = model.get_weights()
coefficients, intercept

# X_test