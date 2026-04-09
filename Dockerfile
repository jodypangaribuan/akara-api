FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libjpeg-dev zlib1g-dev \
    libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev libxcb1 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --default-timeout=1000 --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt && \
    sed -i 's/kwargs.pop("encoder")/kwargs.pop("encoder", None)/g' /usr/local/lib/python3.11/site-packages/surya/model/recognition/config.py && \
    sed -i 's/kwargs.pop("decoder")/kwargs.pop("decoder", None)/g' /usr/local/lib/python3.11/site-packages/surya/model/recognition/config.py

COPY . .

EXPOSE 29999

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "29999"]
