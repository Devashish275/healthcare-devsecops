FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=100 --retries 8 -r requirements.txt
COPY app.py .
RUN useradd -u 1000 -m appuser
USER 1000
EXPOSE 5000
CMD ["python", "app.py"]
