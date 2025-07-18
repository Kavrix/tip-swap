FROM python:3.10-alpine
LABEL maintainer="Kavrix(farsider350)"

LABEL build_date="2025-07-19"
RUN apk update && apk upgrade
RUN apk add --no-cache git make build-base linux-headers
WORKDIR /tip-swap
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "index.py"]
