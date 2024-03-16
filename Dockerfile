FROM python:3.10.11

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /code/app/
COPY migrations/ /code/migrations/
COPY ml/ /code/ml/
COPY .flaskenv celery_tasks.py cf_author.pickle cf_fiction.pickle main.py run_celery.py trainer.py unleash.db /code/

EXPOSE 5000

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:5000"]
