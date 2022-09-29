import requests
import shortuuid
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError
from requests import Response

from data_classes.user import User

tracer = Tracer()
logger = Logger()
app = APIGatewayHttpResolver()


@app.get('/')
@tracer.capture_method
def get_todos():
    todos: Response = requests.get("https://jsonplaceholder.typicode.com/todos")
    todos.raise_for_status()

    return {"todos": todos.json()[:10]}


@app.post('/')
@tracer.capture_method
def create_user():
    try:
        user = User(id=shortuuid.uuid(), **app.current_event.json_body)
    except ValidationError as exc:
        raise BadRequestError(exc.errors())
    else:
        return user.dict()


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
