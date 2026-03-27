import pandas as pd
from tabpfn import TabPFNRegressor, load_fitted_tabpfn_model
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_path', default='E:/tabular/proc.csv')
    parser.add_argument('model_path', default='app/weights')
    parser.add_argument('output_path', default='model_output.csv')

    args = parser.parse_args()

    data = pd.read_csv(args.data_path)

    reg = load_fitted_tabpfn_model('E:/tabular/model.tabpfn_fit', device='cpu')
    X = data.drop(['y'], axis=1)
    y = data['y']
    
    pred = reg.predict(X)

    answer = pd.DataFrame()

    answer = X.copy()
    answer['y_pred'] = pred

    answer.to_csv(args.output_path, index=False)

if __name__ == '__main__':
    main()
