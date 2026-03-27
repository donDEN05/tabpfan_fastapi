FROM pytorch/pytorch:2.5.0-cuda12.4-cudnn9-runtime


RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
        --extra-index-url https://download.pytorch.org/whl/cu130 \
        -r requirements.txt

COPY app/ /app/.

RUN useradd -m -u 1000 mluser && chown -R mluser:mluser /app
USER mluser

EXPOSE 8000

CMD ["python", "-c", "import torch; import tabpfn; print('OK')"]