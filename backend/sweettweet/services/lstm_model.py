import pandas as pd
import numpy as np
from keras.models import load_model
# from tensorflow.keras.models import load_model
import os.path
import json
import tensorflow as tf

# import keras.backend.tensorflow_backend as tb
# tb._SYMBOLIC_SCOPE.value = True
def weighted_mse(yTrue,yPred):
	from keras import backend as K
	ones = K.ones_like(yTrue[0,:]) #a simple vector with ones shaped as (60,)
	idx = K.cumsum(ones) #similar to a 'range(1,61)'
	idx = K.reverse(idx, axes = 0)
	return K.mean((1/idx)*K.square(yTrue-yPred))

import keras.losses
keras.losses.weighted_mse = weighted_mse

from .utils import rolling_window, inv_norm

class LstmModel:

	def __init__(self):
		SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
		self.model_url = os.path.join(SITE_ROOT, '../static/model', 'lstm_model.h5')
		self.model = load_model(self.model_url)
		self.graph = tf.get_default_graph()
	
	def forecast(self, past_data, user_info, new_bg):
		
		# format past data
		data = pd.read_json(json.dumps(past_data))

		data.actualTime = [pd.Timestamp(d, unit='ms') for d in data.actualTime]
		data.forecastTime = [pd.Timestamp(d, unit='ms') for d in data.forecastTime]
		data.sort_values(['actualTime', 'forecastTime'], inplace = True)

		new_timestamp = pd.date_range(start = max(data.actualTime), periods = 2, freq = '5min')[1]

		# add new measurement to past data
		X_new = pd.DataFrame({'actualTime' : [new_timestamp], 'glucose' : [float(new_bg)]})
		X_new = pd.concat([data[data.actualTime == data.forecastTime
								].sort_values(['actualTime', 'forecastTime']
                            	).iloc[-144:, [0,2]],
                   			X_new], axis = 0, ignore_index= True)

		# calculate features
	
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
		
		X = np.dstack((night_input, time_input, glucose_input, 
		           gender_input, insulin_input, bmi_input, age_input))

		# prediction
		with self.graph.as_default():
			Y_pred = self.model.predict(X)

		# correction based on past error
		Y_pred = inv_norm(Y_pred)
		X_past = inv_norm(X[0, -1, 2])
		error = np.array(data[(data.forecastTime == new_timestamp)
		                     ].sort_values(['actualTime'], ascending = 0).glucose)
		
		Y_corr = Y_pred + 0.7 * (X_past - error)

		# alarm
		alarm = int(Y_corr[0, -1] < 70)

		# format prediction to send back to client
		actual_time = [new_timestamp] * 7
		forecast_time = pd.date_range(start = new_timestamp, periods = 7, freq = '5min')
		glucose = [inv_norm(X[:, -1, 2][0])] + Y_corr[0,:].tolist()
		glucose_data_tmp = pd.DataFrame({'actualTime' : actual_time, 
		                                 'forecastTime' : forecast_time, 
		                                 'glucose': glucose})
		
		data = pd.concat([data, glucose_data_tmp], axis = 0, ignore_index=True)
		
		# removing first timepoints
		data = data[data.actualTime > min(data.actualTime)]
		data_json = data.to_json(path_or_buf = None, orient = 'records')

		return (data_json, alarm)

