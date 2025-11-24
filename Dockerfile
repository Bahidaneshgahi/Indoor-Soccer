FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY indoor_soccer_bot.py .

CMD ["python", "indoor_soccer_bot.py"]