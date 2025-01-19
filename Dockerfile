FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN pip install gunicorn
# Increased timeout, reduced workers
CMD ["/usr/local/bin/gunicorn", "--timeout", "300", "--workers", "1", "--bind", "0.0.0.0:8080", "app:app"]
