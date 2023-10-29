from celery import shared_task

from trainer import *


@shared_task
def train_recommendation():
    train()
    return "Train Complete"
