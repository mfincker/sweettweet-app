# import os
import numpy as np, pandas as pd
# from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pmdarima.arima.utils import ndiffs
# import matplotlib.pyplot as plt
# plt.rcParams.update({'figure.figsize':(9,7), 'figure.dpi':120})

from statsmodels.tsa.arima_model import ARIMA
from math import floor
import json


json_data = json.load(open('../static/data/sample_glucose.json'))

# print(json_data)

df = pd.read_json(json.dumps(json_data)) # should be able to read a json string
df = df.sort_values(['Timestamp'])

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

forecast_json = forecast.to_json(path_or_buf = None, orient = 'records')
print(forecast_json)

# twilio_phone_number = app.config['TWILIO_PHONE_NUMBER']
# self.client.messages.create(to=agent_phone_number,
#                             from_=twilio_phone_number,
#                             body=message)