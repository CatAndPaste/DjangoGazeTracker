FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    cmake \
    libsm6 \
    libxext6 \
    libxrender1 \
    libfontconfig1 \
    && apt-get clean

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "DjangoGazeTracker.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
