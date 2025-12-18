# -------- ETAP 1: builder --------
FROM python:3.14-slim AS builder

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/src ./src
COPY app/tests ./tests

# -------- ETAP 2: test --------
FROM builder AS test

RUN pytest tests

# -------- ETAP 3: final --------
FROM python:3.14-slim AS final

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/src ./src

EXPOSE 5000

CMD ["python", "src/main.py"]
