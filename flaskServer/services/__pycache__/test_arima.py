# import os
import numpy as np, pandas as pd
# from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pmdarima.arima.utils import ndiffs
# import matplotlib.pyplot as plt
# plt.rcParams.update({'figure.figsize':(9,7), 'figure.dpi':120})

from statsmodels.tsa.arima_model import ARIMA
from math import floor


json_data = json.load('../static/data/sample_glucose.json'

print(json_data)

# df = pd.read_json(json.dumps(json_data)) # should be able to read a json string

# model = ARIMA(, order=(1,1,1))
# model_fit = model.fit(disp=0)

# n_forecast = 6
# fc = model.predict(n_periods=n_periods)
# index_of_fc = np.arange(len(df.value), len(df.value) + n_periods)

# f

# twilio_phone_number = app.config['TWILIO_PHONE_NUMBER']
# self.client.messages.create(to=agent_phone_number,
#                             from_=twilio_phone_number,
#                             body=message)