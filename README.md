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

- Clone the repo
- Install All dependencies
- You are set! Currently this project is not require anything special. But it soons be changed in the future!


# RUN The Training 

celery -A run_celery:celery worker --loglevel=info
