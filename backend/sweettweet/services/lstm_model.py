"""
lstm_model.py
- LSTM model that implement forecast function
"""

import pandas as pd
import numpy as np
from keras.models import load_model
import os.path
import json
import tensorflow as tf
import keras.losses
from .utils import rolling_window, inv_norm, weighted_mse
keras.losses.weighted_mse = weighted_mse  # add weighted_mse to keras backend losses

class LstmModel:
    '''
    LSTM model class that implements a single `forecast` function
    predictinge the next 6 timepoints of glucose levels given
    past 12h of glucose and user info.
    '''

    def __init__(self):
        '''
        Initialize model from static weights.
        '''
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        self.model_url = os.path.join(SITE_ROOT, '../static/model', 'lstm_model.h5')
        self.model = load_model(self.model_url)
        self.graph = tf.get_default_graph()
    
    def forecast(self, past_data, user_info, new_bg):
        '''
        Return predicted glucose data along with past data and hypoglycemic
        alarm state based on input past data, user info and new glucose measurement.
        '''

        # read in past glucose data
        data = pd.read_json(json.dumps(past_data))

        # format columns to timestamp
        data.actualTime = [pd.Timestamp(d, unit='ms') for d in data.actualTime]
        data.forecastTime = [pd.Timestamp(d, unit='ms') for d in data.forecastTime]
        data.sort_values(['actualTime', 'forecastTime'], inplace = True)

        # new measurement timestamp
        new_timestamp = pd.date_range(start = max(data.actualTime), periods = 2, freq = '5min')[1]

        # add new measurement to past data
        X_new = pd.DataFrame({'actualTime' : [new_timestamp], 'glucose' : [float(new_bg)]})
        X_new = pd.concat([data[data.actualTime == data.forecastTime
                                ].sort_values(['actualTime', 'forecastTime']
                                ).iloc[-144:, [0,2]],
                               X_new], axis = 0, ignore_index= True)

        # calculate model features
        X_new['Time'] = [float(str(d).split(':')[0]) + float(str(d).split(':')[1])/60 for d in X_new.actualTime.dt.time]
        X_new['Time_norm'] = X_new.Time / 24
        X_new['Night'] = [1 if (d < 7 or d > 21) else 0 for d in X_new.Time] 
        X_new['Glucose_norm'] = 2 * (np.log(X_new.glucose) - np.log(30)) / (np.log(400) - np.log(30)) - 1

        gender = int(user_info['gender'] == 'M') # from userInfo
        insulin = int(user_info['insulinDelivery'] == 'pump') # from userInfo
        bmi = float(user_info['bmi']) # from userInfo
        bmi_norm =2 * (bmi - 12) / (45 - 12) - 1 
        age = float(user_info['age']) # from uerInfo
        age_norm = 2 * (age) / 100 - 1

        glucose_input = X_new.Glucose_norm
        night_input = X_new.Night
        time_input = X_new.Time_norm
        timestamp_input = X_new.actualTime
        gender_input = np.ones_like(time_input) * gender
        insulin_input = np.ones_like(time_input) * insulin
        bmi_input = np.ones_like(time_input) * bmi_norm
        age_input = np.ones_like(time_input) * age_norm
        
        # stack all features for the lstm model
        X = np.dstack((night_input, time_input, glucose_input, 
                   gender_input, insulin_input, bmi_input, age_input))

        # forecast
        with self.graph.as_default():
            Y_pred = self.model.predict(X)

        # inverse glucose normalization
        Y_pred = inv_norm(Y_pred)

        # alarm
        alarm = int(Y_pred[0, -1] < 70)

        # format prediction to send back to client
        actual_time = [new_timestamp] * 7
        forecast_time = pd.date_range(start = new_timestamp, periods = 7, freq = '5min')
        glucose = [inv_norm(X[:, -1, 2][0])] + Y_pred[0,:].tolist()
        glucose_data_tmp = pd.DataFrame({'actualTime' : actual_time, 
                                         'forecastTime' : forecast_time, 
                                         'glucose': glucose})
        
        data = pd.concat([data, glucose_data_tmp], axis = 0, ignore_index=True)
        
        # removing first timepoint to only keep the past 12h
        data = data[data.actualTime > min(data.actualTime)]

        # export data to json
        data_json = data.to_json(path_or_buf = None, orient = 'records')

        return (data_json, alarm)


