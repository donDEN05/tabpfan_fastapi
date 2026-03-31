import io
from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from model import TABPFNmodel
import pandas as pd
import zipfile
from etl import ETLmachine
from metrics import Calculate_metrics


app = FastAPI()
MODEL = None
etl = ETLmachine()
metrics = Calculate_metrics()


@app.post("/fit")
async def fit(X: UploadFile, y: UploadFile, task_type: str):
    content_x = await X.read()
    X = pd.read_csv(io.BytesIO(content_x))

    content_y = await y.read()
    y = pd.read_csv(io.BytesIO(content_y))

    global MODEL
    MODEL = TABPFNmodel()
    MODEL.fit(X, y, task_type)

    return MODEL.health()


@app.post('/predict')
async def predict(data: UploadFile):
    content = await data.read()
    df = pd.read_csv(io.BytesIO(content))

    global MODEL
    pred = MODEL.predict(df)

    buffer = io.StringIO()
    pred.to_csv(buffer, index=False)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=predictions.csv'}
    )


@app.post('/make_base_etl')
async def make_base_etl(data: UploadFile, target_name: str, test_size: float):
    content = await data.read()
    df = pd.read_csv(io.BytesIO(content))

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_data:
        global etl
        X_train, y_train, X_val, y_val = etl.make_base(df, target_name, test_size)

        x_t_buffer = io.StringIO()
        x_v_buffer = io.StringIO()
        y_t_buffer = io.StringIO()
        y_v_buffer = io.StringIO()

        X_train.to_csv(x_t_buffer, index=False)
        zip_data.writestr('X_train.csv', x_t_buffer.getvalue())

        y_train.to_csv(y_t_buffer, index=False)
        zip_data.writestr('y_train.csv', y_t_buffer.getvalue())

        X_val.to_csv(x_v_buffer, index=False)
        zip_data.writestr('X_val.csv', x_v_buffer.getvalue())

        y_val.to_csv(y_v_buffer, index=False)
        zip_data.writestr('y_val.csv', y_v_buffer.getvalue())

    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type='application/zip',
        headers={'Content-Disposition': 'attachment; filename=dataset.zip'}
    )

@app.post('/calculate_metrics_regression')
async def calculate_metrics_regression(y_true: UploadFile, y_pred: UploadFile):
    content_true = await y_true.read()
    y_t = pd.read_csv(io.BytesIO(content_true))

    content_pred = await y_pred.read()
    y_p = pd.read_csv(io.BytesIO(content_pred))

    global metrics
    r2, mae, mape, mse = metrics.main_calculations_r(y_t, y_p)

    return {'r2': r2, 'mae': mae, 'mape': mape, 'mse': mse}


@app.get('/status')
def status():
    return MODEL.health()
