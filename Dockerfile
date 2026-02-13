FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY . .

CMD ["uvicorn", "runtime_governance.api.rest:app", "--host", "0.0.0.0", "--port", "8000"]
