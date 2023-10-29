FROM python:3.10.11

RUN mkdir /code
WORKDIR /code
COPY app/ /code/app/
COPY migrations/ /code/migrations
COPY ml/ /code/ml
COPY .flaskenv /code/
COPY .flaskenv /code/
COPY celery_tasks.py /code/
COPY cf_author.pickle /code/
COPY cf_fiction.pickle /code/
COPY main.py /code/
COPY requirements.txt /code/
COPY run_celery.py /code/
COPY trainer.py /code/
COPY unleash.db /code/
COPY requirements.txt /code/
RUN pip install -r requirements.txt


WORKDIR /code
EXPOSE 5000
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:5000"]
