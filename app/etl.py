import pandas as pd
import datetime as dt

class ETLmachine():
    def __init__(self):
        self.columns = None

    def split_timeseries_data(self, X, y, test_size: float):
        horizon = X.shape[0] - int(X.shape[0] * test_size)
        X_train, X_val = X.iloc[:horizon], X.iloc[horizon:]
        y_train, y_val = y.iloc[:horizon], y.iloc[horizon:]

        return X_train, y_train, X_val, y_val
    
    def init_data(self, data, target_name):
        X = data.drop(columns=[target_name])
        y = data[target_name]
        self.columns = X.columns.drop(['Date', 'Name'])

        if 'Date' in X.columns:
            X['Date'] = pd.to_datetime(X['Date'])

        return X, y
    
    def make_lags(self, X, lags=[1, 2, 3, 4, 5, 7, 10, 14, 15, 20, 21, 28]):
        df = X.copy()
        for col in self.columns:
            for lag in lags:
                df[f'{col}_l_{lag}'] = df[col].shift(lag)
        
        return df

    def make_windows(self, X, windows=[3, 5, 7, 10, 14, 21, 28, 35, 49]):
        df = X.copy()
        for col in self.columns:
            for window in windows:
                df[f'{col}_w_m_{window}'] = df[col].rolling(window).mean()
                df[f'{col}_w_std_{window}'] = df[col].rolling(window).std()
        
        return df
    
    def make_time_marks(self, X):
        df = X.copy()
        df['Day_of_week'] = df['Date'].dt.dayofweek
        df['Month'] = df['Date'].dt.month
        df['Year'] = df['Date'].dt.year
        
        return df
    
    def make_base(self, data, target_name, test_size):
        X, y = self.init_data(data, target_name)
        X = self.make_lags(X)
        X = self.make_windows(X)
        X = self.make_time_marks(X)
        X_train, y_train, X_val, y_val = self.split_timeseries_data(X, y, test_size)

        return X_train, y_train, X_val, y_val