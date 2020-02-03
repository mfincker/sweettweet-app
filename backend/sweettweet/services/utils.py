from keras import backend as K
import numpy as np
import altair as alt
import pandas as pd



def f_beta(p, r, beta = 2):
	return ((1+beta * beta) * (p * r)) / ((beta * beta * p) + r)


def weighted_mse(yTrue,yPred):
	ones = K.ones_like(yTrue[0,:]) #a simple vector with ones shaped as (60,)
	idx = K.cumsum(ones) #similar to a 'range(1,61)'
	idx = K.reverse(idx, axes = 0)
	return K.mean((1/idx)*K.square(yTrue-yPred))

def inv_norm(x):
	return np.exp(np.log(30) + (x+1)*(np.log(400) - np.log(30))/2)

def rolling_window(a, window):
	# a = np.array(a)
	shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
	strides = a.strides + (a.strides[-1],)
	return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def alarm_metric(a_true, a_pred):  
	a_pred_padded = np.pad(a_pred, pad_width = ((0, 0),(3,3)), constant_values = 0)
	a_true_padded = np.pad(a_true, pad_width = ((0, 0),(3,3)), constant_values = 0)
	
	r = rolling_window(a_pred_padded, 7)
	a_pred_all = (np.sum(r, axis = 2) >= 1).astype(int).flatten()

	t = rolling_window(a_true_padded, 7)
	a_true_all = (np.sum(t, axis = 2) >= 1).astype(int).flatten()

	TP_p = np.sum(np.logical_and(a_pred, a_true_all))
	FP = np.sum(a_true) - np.sum(np.logical_and(a_pred, a_true_all))
	TP_r = np.sum(np.logical_and(a_pred_all, a_true))
	FN = np.sum(a_pred) - np.sum(np.logical_and(a_pred_all, a_true))
	return (TP_p, FN, TP_r, FP)

def glu_to_alarm(y_true, y_pred):
	hypo_real = (y_true < 70).astype(int)
	hypo_pred = (y_pred < 70).astype(int)

	a_pred = np.array([hypo_pred[0]] + [True if (hypo_pred[i] == True and hypo_pred[i-1] == False) 
											  else False 
											  for i in range(1, len(hypo_pred))], ndmin = 2)

	a_true = np.array([hypo_real[0]] + [True if (hypo_real[i] == True and hypo_real[i-1] == False) 
											  else False 
											  for i in range(1, len(hypo_real))], ndmin = 2)
	return (a_true, a_pred)

def glu_plot(*args):
    p = []
    colors = ['red', 'blue', 'green', 'black']
    i = 0
    for a in args:
        df = pd.DataFrame({'glucose' : a})
        s = alt.Chart(df.reset_index()).mark_line(color = colors[i]).encode(
            x = 'index', y = 'glucose')
        p.append(s)
        i += 1
        
    P = p[0]
    if len(p) > 1:
        for s in p[1:]:
            P += s
            
    return P


