import dataclasses
import datetime
import urllib
from dataclasses import dataclass, field
from typing import Generator, Optional, Union

from dataclasses_json import CatchAll, Undefined, config, dataclass_json
from marshmallow import fields

from . import credentials, error_response, request_api


def parse_datetime(value):
    if value is None:
        return None
    elif isinstance(value, str):
        return datetime.datetime.fromisoformat(value)
    elif isinstance(value, datetime.datetime):
        return value
    else:
        raise RuntimeError("unsopported time for a datetime field")


# Response


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponseWrapper:
    status: str


def get_campaigns_orders(
    credentials: credentials.Credentials,
    campaign_id: str,
    order_id: str,
) -> GetOrdersResponseWrapper:
    response = request_api.request_api_raw(
        "GET",
        f"/campaigns/{campaign_id}/orders/{order_id}/delivery/labels",
        credentials,
        None,
        # response_cls=GetOrdersResponseWrapper,
    )
    return response.content
