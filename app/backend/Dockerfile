FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory
COPY app /app

# Set Python path to include the app directory
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Add debug flags
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "debug"] 