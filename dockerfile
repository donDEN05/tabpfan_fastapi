FROM python:3.14.2-slim

WORKDIR /project

COPY . .

RUN pip3 install -r requirements.txt

EXPOSE 8000
EXPOSE 8001

WORKDIR /project/app
RUN uvicorn app:app --reload --port 8000
CMD streamlit run .\front.py --server.port 8001