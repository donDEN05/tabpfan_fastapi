from tabpfn import TabPFNRegressor, TabPFNClassifier
import pandas as pd
class TABPFNmodel():
    def __init__(self):
        self.device = 'cpu'
        self._weights_path_c = 'w/tabpfn-v2.5-classifier-v2.5_default.ckpt'
        self._weights_path_r = 'w/tabpfn-v2.5-regressor-v2.5_default.ckpt'
        self.model = None
        self._is_fitted = False
        self._target_name = None


    def fit(self, X, y, type: str):
        if type == 'Classification':
            self.model = TabPFNClassifier(model_path=self._weights_path_c, device=self.device, ignore_pretraining_limits=True)
        elif type == 'Regression':
            self.model = TabPFNRegressor(model_path=self._weights_path_r, device=self.device, ignore_pretraining_limits=True)
        else:
            print('Тип не выбран')
        
        self.model.fit(X, y)

        self._target_name = y.columns[0]
        self._is_fitted = True

    
    def predict(self, X):
        pred = self.model.predict(X)
        return pd.DataFrame({f'{self._target_name}_predicted': pred})
        


    def health(self):
        return self._is_fitted, self._target_name