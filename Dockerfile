FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
RUN useradd -m appuser && chown -R appuser /app
USER appuser
COPY --from=builder /root/.local /home/appuser/.local
COPY app/ .
ENV PATH="/home/appuser/.local/bin:${PATH}"
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
