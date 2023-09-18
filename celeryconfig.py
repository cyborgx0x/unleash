from celery import Celery
from datetime import timedelta

# Define the Celery app and configure it
app = Celery('recommendation_training', broker='redis://localhost:6379/0', include=['your_training_module'])

# Configure task settings (e.g., serialization)
app.conf.task_serializer = 'pickle'
app.conf.result_serializer = 'pickle'
app.conf.accept_content = ['pickle']

# Schedule the task to run daily
app.conf.beat_schedule = {
    'train-recommendation-model': {
        'task': 'your_training_module.train_recommendation_model',
        'schedule': timedelta(days=1),  # Run daily
    },
}
