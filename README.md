Скрипт для запуска fast api:
uvicorn app:app --reload --port 8000
streamlit run .\front.py --server.port 8001

RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu130