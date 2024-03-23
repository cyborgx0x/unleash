from app import app, db
from app.models import Author, Fiction, User

from run_celery import celery_init_app


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Fiction": Fiction, "User": User, "Author": Author}

app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://redis:6379/0",
        # broker_url="amqp://guest:guest@127.0.0.1:5672/",
        result_backend="redis://redis:6379/0",
        task_ignore_result=True,
    ),
)
celery_app = celery_init_app(app)
celery_app.conf.beat_schedule = {
    "add-every-hour": {"task": "app.tasks.train_recommendation", "schedule": 3600},
}

if __name__ == "__main__":
    print("starting flask")
    app.run()
