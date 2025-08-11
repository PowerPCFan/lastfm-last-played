# FROM python:3.12.4-alpine
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

COPY . .

# CMD ["gunicorn", "app.main:app", "--bind", "0.0.0.0:5000", "--workers", "4"]
CMD ["gunicorn", "--chdir", "app", "main:app", "--bind", "0.0.0.0:5000", "--workers", "4"]
