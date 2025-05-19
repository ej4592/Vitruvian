FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/frontend /app/frontend

EXPOSE 8501

# Enable hot reloading for development
ENV STREAMLIT_SERVER_WATCH_DIRS=true
ENV STREAMLIT_SERVER_HEADLESS=true

CMD ["streamlit", "run", "frontend/app.py", "--server.address", "0.0.0.0", "--server.port", "8501"] 