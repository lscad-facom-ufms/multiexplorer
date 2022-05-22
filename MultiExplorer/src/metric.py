import numpy as np
# from sklearn import metrics

def mean_absolute_percentage_error(y_true, y_pred, sample_weight=None):
    # TODO gambiarra para treinar com log(y)
    y_true = np.exp(y_true)
    y_pred = np.exp(y_pred)
    #epsilon = tratamento de divisao por zero 
    epsilon = np.finfo(np.float64).eps
    mape = np.abs(y_pred - y_true) / np.maximum(np.abs(y_true), epsilon)
    return np.average(mape, weights=sample_weight)
# neg_mean_absolute_percentage_scorer = metrics.make_scorer(mean_absolute_percentage_error, greater_is_better=False) 

""" class mean_absolute_percentage_error(object):
    def __init__(self, y_true, y_pred, sample_weight=None):
        self.y_true= y_true
        self.y_pred = y_pred
        y_true = np.exp(y_true)
        y_pred = np.exp(y_pred)
        #epsilon = tratamento de divisao por zero 
        epsilon = np.finfo(np.float64).eps
        mape = np.abs(y_pred - y_true) / np.maximum(np.abs(y_true), epsilon)
        return np.average(mape, weights=sample_weight)
 """