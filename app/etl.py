import pandas as pd
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_path')
    parser.add_argument('--output_path')
    args = parser.parse_args()

    data = pd.read_csv(args.input_path)

    X = data.drop(['Date', 'Name', 'Volume'], axis=1)
    y = data['Volume']
    data_to_return = X.copy()
    data_to_return['y'] = y
 
    if args.output_path:
        data_to_return.to_csv(args.output_path, index=False)

if __name__ == '__main__':
    main()