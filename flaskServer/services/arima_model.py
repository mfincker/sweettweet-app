# import os
import numpy as np, pandas as pd
# from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pmdarima.arima.utils import ndiffs
# import matplotlib.pyplot as plt
# plt.rcParams.update({'figure.figsize':(9,7), 'figure.dpi':120})

from statsmodels.tsa.arima_model import ARIMA
from math import floor
import json
# from statsmodels.tsa.stattools import acf


# import pmdarima as pm


class ArimaModel:
	client = None

	def __init__(self):
		# Find these values at https://twilio.com/user/account
		d = 2
		p = 0
		q = 1
		n_forecast = 6
		# self.client = Client(account_sid, auth_token)

	def forecast(self, past_data, newBG):

    	# json_data = json.load(open('../static/data/sample_glucose.json'))

		# print(json_data)

		df = pd.read_json(json.dumps(past_data)) # should be able to read a json string
		df = df.sort_values(['Timestamp'])
		# print(df.shape)
		# print(df.Timestamp.iloc[-1])
		newTimestamp = df.Timestamp.iloc[-1] + pd.Timedelta('5min')

		df = df.iloc[1:,:]
		# print(df.shape)
		df = df.append({'Timestamp' : newTimestamp, 'Glucose' : int(newBG)}, ignore_index=True)
		# print(df.shape)
		# print(df.iloc[-1,:])

	# newTimestamp = past_data[-1]['Timestamp'] + 5 * 60
	# # Remove first data point
	# past_data = past_data[1:]
	# past_data.append({'Timestamp' : newTimestamp, 'Glucose' : newBG})

		glucose = df.Glucose

		model = ARIMA(glucose, order = (1,1,1))
		fitted = model.fit(disp = -1)

		n_forecast = 6

		# Forecast
		fc, se, conf= fitted.forecast(n_forecast, alpha = 0.05)
		# index_of_fc = np.arange(len(glucose), len(glucose) + n_periods)



		delta = pd.Timedelta('5min')
		fc_Timestamp = pd.date_range(start = df.Timestamp.iloc[-1], periods = 7, freq = '5 min')[1:]


		forecast = pd.DataFrame({'Glucose' : fc,
								'Timestamp': fc_Timestamp})

		if fc[-1] < 70:
			alarm = 1
		else:
			alarm = 0

		# print('forecast shape: ' + str(forecast.shape[0]))

		forecast_json = forecast.to_json(path_or_buf = None, orient = 'records')
		past_json = df.to_json(path_or_buf = None, orient = 'records')
		# print(forecast_json)

		return (past_json, forecast_json, alarm)
