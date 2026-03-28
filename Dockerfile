FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir fastmcp httpx

COPY proxy.py .

ENV NEFESH_API_KEY=""

CMD ["python", "proxy.py"]
