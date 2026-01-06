FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=enterprise_synthetic_data_hub.api.app:app

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

ARG PIP_CONF_PATH=
ARG PIP_INDEX_URL
ARG PIP_EXTRA_INDEX_URL
ARG PIP_TRUSTED_HOST

ENV PIP_INDEX_URL=${PIP_INDEX_URL}
ENV PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL}
ENV PIP_TRUSTED_HOST=${PIP_TRUSTED_HOST}

RUN set -eux; \
    if [ -n "${PIP_CONF_PATH}" ]; then \
        if [ -f "${PIP_CONF_PATH}" ]; then \
            cp "${PIP_CONF_PATH}" /etc/pip.conf; \
            echo "Using pip config from ${PIP_CONF_PATH}"; \
        else \
            echo "PIP_CONF_PATH was provided but no file found at ${PIP_CONF_PATH}"; \
            exit 1; \
        fi; \
    else \
        echo "No pip.conf provided at build time; relying on defaults and any pip-related env vars."; \
    fi

RUN pip install --upgrade pip && \
    pip install -e .[dev]

EXPOSE 5000
CMD ["bash"]
