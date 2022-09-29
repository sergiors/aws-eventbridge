from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import EventBridgeEvent, event_source
from aws_lambda_powertools.utilities.typing import LambdaContext

logger = Logger(__name__)


@event_source(data_class=EventBridgeEvent)
@logger.inject_lambda_context
def lambda_handler(event: EventBridgeEvent, context: LambdaContext) -> None:
    ...
