FROM python:3.10.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]