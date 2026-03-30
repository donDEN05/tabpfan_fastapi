import streamlit as st
import requests
import io


API_URL = st.sideber.text_input('API base URL', value='http://localhost:8000')

st.title('TabPFN using')

def post(method, files=None, data=None):
    url = f'{API_URL}{method}'

    response = requests.post(url, files=files, data=data)
    response.raise_for_status()

    return response

def fit():
    st.subheader('Обучите модель:')

    task_type = st.selectbox('Веберите task type', ['Regression', 'Classification'])
    X_train = st.file_uploader('Загрузите X train', type='csv') # могут быть проблемы при загрузеке файлов
    y_train = st.file_uploader('Загрузите y train', type='csv') # могут быть проблемы при загрузеке файлов

    if st.button('Обучить'):
        files = {'X': (X_train.name, X_train.getvalue(), 'text/csv'),
                'y': (y_train.name, y_train.getvalue(), 'text/csv')}
        data = {'task_type': task_type}

        response = post('/fit', files, data)
        if response:
            st.success('Модель обучена на даныых {X_train.name} и {y_train.name}')

def predict():
    st.subheader('Предсказание:')

    data = st.file_uploader('Загрузите файл', type='csv')

    if st.button('Выполнить'):
        files = {'data': (data.name, data.getvalue(), 'text/csv')}

        response = post('/predict', files=files)
        if response:
            st.download_button(
                label='Скачать predictions',
                data=response.content,
                file_name='predictions.csv',
                mime='text/csv'
            )
            