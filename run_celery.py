from celery import Celery

# Create a Celery instance
celery = Celery('recommendation_training')

# Load the Celery configuration from the celeryconfig.py file
celery.config_from_object('celeryconfig')

if __name__ == '__main__':
    celery.start()
