import functions_framework
from cloudevents.http.event import CloudEvent
from app.helpers.logger import get_logger

logger = get_logger("hello_pubsub")

@functions_framework.cloud_event
def hello_pubsub(cloud_event: CloudEvent) -> None:
   logger.info(f"Received event with ID: {cloud_event['id']} and data {cloud_event.data}")
