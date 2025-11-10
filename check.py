import numpy as np
from sklearn.metrics import mean_squared_error

mse = mean_squared_error(y_test, preds)
rmse = np.sqrt(mse)
