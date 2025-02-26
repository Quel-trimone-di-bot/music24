# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y ffmpeg

# Copy bot files
COPY requirements.txt .
COPY bot.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "bot.py"]
