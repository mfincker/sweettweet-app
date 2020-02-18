"""
utils.py
- provides utility functions for the prediction models
"""

from keras import backend as K
import numpy as np
import pandas as pd



def f_beta(p, r, beta = 2):
	'''
	Return f_beta score given a precision and recall score
	'''
	return ((1+beta * beta) * (p * r)) / ((beta * beta * p) + r)


def weighted_mse(yTrue,yPred):
	'''
	Custom mean-squared error that emphasizes the weights for 
	later predictions during multi-step forecasting.
	'''
	ones = K.ones_like(yTrue[0,:]) #a simple vector with ones shaped as (forecast_step,)
	idx = K.cumsum(ones) #similar to a 'range(1,forecast_step + 1)'
	idx = K.reverse(idx, axes = 0) 
	return K.mean((1/idx)*K.square(yTrue-yPred))

def inv_norm(x):
	'''
	Given a normalized glucose measurements, return true glucose level
	'''
	return np.exp(np.log(30) + (x+1)*(np.log(400) - np.log(30))/2)

def rolling_window(a, window):
	'''
	Given an array a and a window size window, 
	return a numpy array with stacked sliding windows from array a of
	size window.

	Ex: a = [0, 1, 2, 3]
		rolling_window(a, 3) -> [[0, 1, 2],
								 [1, 2, 3]]
	'''
	shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
	strides = a.strides + (a.strides[-1],)
	return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def alarm_metric(a_true, a_pred):  
	'''
	Returned a modified precision and recall score for the alarm prediction
	task that counts an alarm prediction as positive if it happens
	withing 15 min of a real hypoglycemic event
	'''
	a_pred_padded = np.pad(a_pred, pad_width = ((0, 0),(3,3)), constant_values = 0) # pad array to acount for +/- 15 min
	a_true_padded = np.pad(a_true, pad_width = ((0, 0),(3,3)), constant_values = 0)
	
	r = rolling_window(a_pred_padded, 7)
	a_pred_all = (np.sum(r, axis = 2) >= 1).astype(int).flatten()

	t = rolling_window(a_true_padded, 7)
	a_true_all = (np.sum(t, axis = 2) >= 1).astype(int).flatten()

	TP_p = np.sum(np.logical_and(a_pred, a_true_all)) # true positive for precision
	FP = np.sum(a_true) - np.sum(np.logical_and(a_pred, a_true_all)) # false positive
	TP_r = np.sum(np.logical_and(a_pred_all, a_true)) # true positive for recall
	FN = np.sum(a_pred) - np.sum(np.logical_and(a_pred_all, a_true)) # false negative
	return (TP_p, FN, TP_r, FP)

def glu_to_alarm(y_true, y_pred):
	'''
	Convert glucose levels to alarm.

	Alarm state is positive if glucose at time 
	t and t-1 is < 70 and >70 at time t-2.
	'''
	hypo_real = (y_true < 70).astype(int)
	hypo_pred = (y_pred < 70).astype(int)

	a_pred = np.array([hypo_pred[0]] + [True if (hypo_pred[i] == True and hypo_pred[i-1] == False) 
											  else False 
											  for i in range(1, len(hypo_pred))], ndmin = 2)

	a_true = np.array([hypo_real[0]] + [True if (hypo_real[i] == True and hypo_real[i-1] == False) 
											  else False 
											  for i in range(1, len(hypo_real))], ndmin = 2)
	return (a_true, a_pred)



