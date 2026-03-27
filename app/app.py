import io
from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from model import ml
import pandas as pd


app = FastAPI()
model = None

@app.post("/fit")
async def fit(data: UploadFile, target_name: str, task_type: str):
    content = await data.read()
    df = pd.read_csv(io.BytesIO(content))

    X = df.drop(columns=[target_name])
    y = df[target_name]

    global model
    model = ml()
    model.fit(X, y, task_type, target_name)

    return model.health()

@app.post('/predict')
async def predict(data: UploadFile):
    content = await data.read()
    df = pd.read_csv(io.BytesIO(content))

    global model
    pred = model.predict(df)

    buffer = io.StringIO()
    pred.to_csv(buffer, index=False)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=predictions.csv'}
    )

@app.get('/status')
def status():
    global model
    return model.health()