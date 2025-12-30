FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=enterprise_synthetic_data_hub.api.app:app

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

ARG CORP_CA_PATH=certs/csaa_netskope_combined.pem
ARG SKIP_CORP_CA=0

RUN set -eux; \
    if [ "${SKIP_CORP_CA}" = "1" ]; then \
        echo "Skipping corporate CA install; assuming public TLS works."; \
    else \
        if [ ! -f "${CORP_CA_PATH}" ]; then \
            echo "Corporate CA bundle missing at ${CORP_CA_PATH}. Place it locally before building, or set SKIP_CORP_CA=1 to bypass on personal networks."; \
            exit 1; \
        fi; \
        mkdir -p /usr/local/share/ca-certificates/corp; \
        awk 'BEGIN{c=0} /BEGIN CERTIFICATE/{c++} {print > ("/usr/local/share/ca-certificates/corp/corp-" c ".crt")}' "${CORP_CA_PATH}"; \
        update-ca-certificates; \
    fi

RUN pip install --upgrade pip && \
    pip install -e .[dev]

EXPOSE 5000
CMD ["bash"]
