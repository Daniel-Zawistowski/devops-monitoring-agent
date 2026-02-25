FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main_agent.py system_monitor.py healthcheck.py ./
CMD ["python", "main_agent.py"]