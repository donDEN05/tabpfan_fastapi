FROM python:3.14.2-slim

WORKDIR /project

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8000

WORKDIR /project/app

CMD uvicorn app:app --reload --host 0.0.0.0 --port 8000