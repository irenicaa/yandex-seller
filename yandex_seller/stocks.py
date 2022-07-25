import datetime
from dataclasses import dataclass, field
from typing import Generator, Optional, Union

from dataclasses_json import Undefined, config, dataclass_json
from marshmallow import fields

from . import credentials, request_api


def parse_datetime(value):
    if value is None:
        return None
    elif isinstance(value, str):
        return datetime.datetime.fromisoformat(value)
    elif isinstance(value, datetime.datetime):
        return value
    else:
        raise RuntimeError("unsopported time for a datetime field")


# Request


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class StocksRequest:
    warehouseId: Optional[int] = None
    skus: Optional[list[str]] = None


# Response


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetStocksResponseItem:
    type: str
    count: Union[int, str]
    updatedAt: datetime.datetime = field(
        metadata=config(
            decoder=datetime.datetime.fromisoformat,
            mm_field=fields.DateTime(format="iso"),
        ),
    )


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetStocksResponse:
    sku: str
    warehouseId: Union[int, str]
    items: list[GetStocksResponseItem]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetStocksResponseWrapper:
    skus: list[GetStocksResponse]


def get_stocks(
    credentials: credentials.Credentials,
    data: StocksRequest,
) -> GetStocksResponseWrapper:
    return request_api.request_api_json(
        "POST",
        "/stocks",
        credentials,
        data,
        response_cls=GetStocksResponseWrapper,
    )
