FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    software-properties-common \
    && apt-get install -y ffmpeg git \
    && echo "FFmpeg installed successfully. Version:" \
    && ffmpeg -version \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
