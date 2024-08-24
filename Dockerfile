FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk2.0-dev \
    libboost-python-dev \
    libboost-thread-dev \
    libsm6 \
    libxext6 \
    libxrender1 \
    libfontconfig1 \
    libgl1-mesa-glx \
    && apt-get clean

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "DjangoGazeTracker.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
