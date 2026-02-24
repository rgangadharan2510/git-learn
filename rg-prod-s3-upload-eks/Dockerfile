FROM python:3.10-slim

WORKDIR /app

# Copy dependency file first (better caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY src/ ./src/
COPY main.py .
COPY data.json .

# Default command
ENTRYPOINT ["python", "main.py"]