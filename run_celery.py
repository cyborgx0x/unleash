from celery import Celery


def celery_init_app(app) -> Celery:
    celery_app = Celery(app.name, include=["app.tasks"])
    celery_app.config_from_object(app.config["CELERY"])

    celery_app.autodiscover_tasks(lambda: [app.name], force=True)

    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
