# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 11:46:26 2024

@author: tejas
"""

import numpy as np
import pickle

# loading the saved model
loaded_model = pickle.load(open(r"C:\Users/tejas/OneDrive/Desktop/fraud_detection/RF_model.sav", 'rb'))
loaded_model2 = pickle.load(open(r'C:\Users/tejas/OneDrive/Desktop/fraud_detection/KNN_model.sav', 'rb'))


input_data = (743,1,339682.130,339682.130,0.0,0.000,339682.130,0)

# changing the input_data to numpy array
input_data_as_numpy_array = np.asarray(input_data)

# reshape the array as we are predicting for one instance
input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

prediction = loaded_model.predict(input_data_reshaped)
print(prediction)

if (prediction[0] == 0):
  print('THE TRANSACTIONS ARE NOT FRAUD')
else:
  print('THE TRANSACTIONS ARE FRAUD')