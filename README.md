# UNLEASH - Implementing Recommendation System with a basic CMS 

- CMS Stuffs: Fictions, Authors
- Recommendation based on User following on Author or User like on Fiction. Will use both Collaborative Filtering and Content Based

## Tasks

This Project Focus on Following Task

- App: Develop a web application where user can interact with fiction and author
- ML: Train New model, define the prediction function for the app to inference
- Tasks: Responsible for the Event Distribution Tasks. 
- Workflows: Responsible for Work flow and deploying option

## HOW TO RUN this project

### With docker
- Install Docker
- RUN Docker compose

```
docker compose up
```

### Without Docker

```
pip install -r requirements.txt
# migrate database change
flask db upgrade
flask run
```

# RUN The Training 

celery -A main.celery_app worker -l INFO -P eventlet
celery -A main.celery_app beat -l INFO 