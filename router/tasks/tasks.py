# pylint: disable=unused-argument,no-self-use,missing-function-docstring
import json

from celery.utils.log import get_task_logger

from router.extensions import celery
from router.event import dispatch, Event

logger = get_task_logger(__name__)


class BaseTask(celery.Task):
    """Base Celery task."""

    def on_success(self, retval, task_id, args, kwargs):
        logger.info(f"Task {task_id} has succeeded.")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(f"Task {task_id} has failed. Execution info: {einfo}.")

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logger.warning(f"Retrying task {task_id}...")


class Processor(BaseTask):
    """Celery task to process a webhook."""

    name = "webhook_processor"

    def run(self, data: dict, topic: str, shop: str, version: str, webhook_id: str, test: bool):
        logger.info(f"Processing webhook {webhook_id} {topic}")
        event = Event(json.loads(data), topic, shop, version, webhook_id, test)
        try:
            dispatch(event)
        except NotImplementedError as err:
            logger.error(err)


celery.tasks.register(Processor())
