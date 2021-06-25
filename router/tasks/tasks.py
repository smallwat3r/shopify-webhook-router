# pylint: disable=unused-argument,no-self-use
from celery.utils.log import get_task_logger

from router.extensions import celery

logger = get_task_logger(__name__)


class BaseTask(celery.Task):
    def on_success(self, retval, task_id, args, kwargs):
        logger.info(f"Task {task_id} has succeeded.")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(f"Task {task_id} has failed. Execution info: {einfo}.")

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        logger.warning(f"Retrying task {task_id}...")


class Processor(BaseTask):

    name = "webhook_processor"

    def run(self):
        logger.info("Processing webhook.")


celery.tasks.register(Processor())
