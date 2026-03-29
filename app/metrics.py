from sklearn.metrics import r2_score, mean_absolute_error, mean_absolute_percentage_error, mean_squared_error


class Calculate_metrics():
    def __init__(self):
        self.status = None

    
    def main_calculations_r(self, y_true, y_predict):
        r2 = r2_score(y_true, y_predict)
        mae = mean_absolute_error(y_true, y_predict)
        mape = mean_absolute_percentage_error(y_true, y_predict)
        mse = mean_squared_error(y_true, y_predict)

        return r2, mae, mape, mse