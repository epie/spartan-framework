import functions_framework
from cloudevents.http.event import CloudEvent
from app.helpers.logger import get_logger


logger = get_logger("spartan.lazaro.main")

@functions_framework.cloud_event
def main(cloud_event: CloudEvent) -> None:

   logger.info(f"Testing", extra={
      "testing": "test",
      "another": 1234
   })
