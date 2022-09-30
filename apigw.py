import json

import boto3
import requests
import shortuuid
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from botocore.exceptions import ClientError
from pydantic import ValidationError
from requests import Response

from data_classes.user import User

tracer = Tracer()
logger = Logger()
app = APIGatewayHttpResolver()

events = boto3.client('events')


def put_event(event: dict, detail_type: str, source: str, *, event_client):
    try:
        event_client.put_events(
            Entries=[
                {
                    'Source': source,
                    'DetailType': detail_type,
                    'Detail': json.dumps(event),
                },
            ]
        )
    except ClientError:
        pass


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
        put_event(
            user.dict(),
            source='apigw',
            detail_type='User Created',
            event_client=events,
        )
        return user.dict()


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
