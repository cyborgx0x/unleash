FROM python:latest
ENV PYTHONUNBUFFERED 1
RUN mkdir /code

COPY app /code/app
ADD main.py /code/main.py
ADD configuration.py /code/configuration.py
ADD requirements.txt /code/
ADD .env /code/.env

WORKDIR /code
RUN pip install -r requirements.txt

CMD [ "gunicorn --bind 0.0.0.0:8000 main:app --log-file" ] 
