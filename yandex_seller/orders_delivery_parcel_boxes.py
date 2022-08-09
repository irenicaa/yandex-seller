import dataclasses
import datetime
import urllib
from dataclasses import dataclass, field
from typing import Generator, Optional, Union

from dataclasses_json import CatchAll, Undefined, config, dataclass_json
from marshmallow import fields

from . import credentials, error_response, request_api

# Request


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OrderDeliveryParcelBoxesItems:
    id: Optional[int]
    count: Optional[int]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OrderDeliveryParcelBoxes:
    fulfilmentId: Optional[str]
    weight: Optional[int]
    width: Optional[int]
    height: Optional[int]
    depth: Optional[int]
    items: Optional[list[OrderDeliveryParcelBoxesItems]]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OrderDeliveryParcel:
    boxes: Optional[list[OrderDeliveryParcelBoxes]]


# Response


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderDeliveryParcelBoxesResponseResultBox:
    id: int
    fulfilmentId: str
    weight: int
    width: int
    height: int
    depth: int


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderDeliveryParcelBoxesResponseResult:
    boxes: list[SetOrderDeliveryParcelBoxesResponseResultBox]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderDeliveryParcelBoxesResponseResultWrapper:
    status: str
    result: SetOrderDeliveryParcelBoxesResponseResult


def set_order_boxes(
    credentials: credentials.Credentials,
    campaign_id: str,
    order_id: int,
    data: OrderDeliveryParcelBoxesItems,
) -> SetOrderDeliveryParcelBoxesResponseResultWrapper:
    print(f"/campaigns/{campaign_id}/orders/{order_id}/status")
    return request_api.request_api_json(
        "PUT",
        f"/campaigns/{campaign_id}/orders/{order_id}/status",
        credentials,
        data,
        response_cls=SetOrderDeliveryParcelBoxesResponseResultWrapper,
    )
