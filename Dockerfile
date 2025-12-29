FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=enterprise_synthetic_data_hub.api.app:app

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip && \
    pip install -e .[dev]

EXPOSE 5000
CMD ["bash"]
