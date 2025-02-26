FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt .
COPY bot.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "bot.py"]
