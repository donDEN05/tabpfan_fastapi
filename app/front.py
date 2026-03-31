import streamlit as st
import requests


API_URL = st.sidebar.text_input('API base URL', value='http://localhost:8000')

st.title('TabPFN using')

def post(method, files=None, params=None):
    url = f'{API_URL}{method}'

    response = requests.post(url, files=files, params=params)
    response.raise_for_status()

    return response

def fit():
    st.subheader('Обучите модель:')

    task_type = st.selectbox('Веберите task type', ['Regression', 'Classification'])
    X_train = st.file_uploader('Загрузите X train', type='csv')
    y_train = st.file_uploader('Загрузите y train', type='csv')

    if st.button('Обучить'):
        files = {'X': (X_train.name, X_train.getvalue(), 'text/csv'),
                'y': (y_train.name, y_train.getvalue(), 'text/csv')}
        params = {'task_type': task_type}

        response = post('/fit', files=files, params=params)
        if response:
            st.success(f'Модель обучена на даныых {X_train.name} и {y_train.name}')

def predict():
    st.subheader('Предсказание:')

    data = st.file_uploader('Загрузите файл', type='csv')

    if st.button('Выполнить'):
        files = {'data': (data.name, data.getvalue(), 'text/csv')}

        response = post('/predict', files=files)
        if response:
            st.success('Значения сгенерированы.')
            st.download_button(
                label='Скачать predictions',
                data=response.content,
                file_name='predictions.csv',
                mime='text/csv'
            )

def calculate_metrics():
    st.subheader('Подсчет метрик:')

    y_true = st.file_uploader('Загрузите y_true', type='csv')
    y_pred = st.file_uploader('Загрузите y_pred', type='csv')

    if st.button('Посчитать'):
        files = {
            'y_true': (y_true.name, y_true.getvalue(), 'text/csv'),
            'y_pred': (y_pred.name, y_pred.getvalue(), 'text/csv')
        }
        response = post('/calculate_metrics_regression', files)

        if response:
            st.success('Метрики посчитаны')
            st.success(response.content)
            
def make_etl():
    st.subheader('Сделать базовый ETL:')
    

task = st.selectbox('Выберите задачу:', ['fit', 'predict', 'calculate metrics'])

if task == 'fit':
    fit()
elif task == 'predict':
    predict()
elif task == 'calculate metrics':
    calculate_metrics()