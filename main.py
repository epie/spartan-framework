import base64

import functions_framework
from cloudevents.http import CloudEvent

from handlers.pubsub import my_processor

class SpartanPubSubHandler:
    def __init__(self, processor):
        self.processor = processor

    def handle(self, cloud_event: CloudEvent):
        data = cloud_event.data
        pubsub_message = data.get("message", {})
        payload = None
        if "data" in pubsub_message:
            payload = base64.b64decode(pubsub_message["data"]).decode("utf-8")

        self.processor(payload)

handler = SpartanPubSubHandler(my_processor)


@functions_framework.cloud_event
def hello_pubsub(cloud_event: CloudEvent):
    handler.handle(cloud_event)
