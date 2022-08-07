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
class OrderStatus:
    status: Optional[str] = None
    substatus: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetStatusRequest:
    order: Optional[OrderStatus] = None


# Response


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResultOrderDeliveryShipmentBoxItem:
    id: int
    count: int


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResultOrderDeliveryShipmentBox:
    id: int
    height: int
    depth: int
    width: int
    weight: int
    items: list[SetOrderStatusResponseResultOrderDeliveryShipmentBoxItem]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResultOrderDeliveryShipment:
    id: int
    shipmentDate: str
    shipmentTime: str
    boxes: list[SetOrderStatusResponseResultOrderDeliveryShipmentBox]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResultOrderDeliveryRegionParentParent:
    id: int
    name: str
    type: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResultOrderDeliveryRegionParent:
    id: int
    name: str
    type: str
    parent: SetOrderStatusResponseResultOrderDeliveryRegionParentParent


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResultOrderDeliveryRegion:
    id: int
    name: str
    type: str
    parent: SetOrderStatusResponseResultOrderDeliveryRegionParent



@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResultOrderDeliveryDates:
    fromDate: Optional[str] = None
    toDate: Optional[str] = None
    fromTime: Optional[str] = None
    toTime: Optional[str] = None

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResultOrderDelivery:
    deliveryPartnerType: str
    id: str
    outletCode: str
    price: float
    serviceName: str
    type: str
    vat: str
    outletId: int
    dates: SetOrderStatusResponseResultOrderDeliveryDates
    region: SetOrderStatusResponseResultOrderDeliveryRegion
    shipments: list[SetOrderStatusResponseResultOrderDeliveryShipment]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResultOrder:
    cancelRequested: bool
    creationDate: str #TODO
    currency: str
    fake: bool
    id: int
    itemsTotal: float
    paymentType: str
    paymentMethod: str
    status: str
    substatus: str
    taxSystem: str
    total: float
    subsidyTotal: float
    delivery: SetOrderStatusResponseResultOrderDelivery
    notes: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResult:
    order: SetOrderStatusResponseResultOrder


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseWrapper:
    status: Optional[str]
    result: Optional[SetOrderStatusResponseResult]


def set_order_status(
    credentials: credentials.Credentials,
    campaign_id: str,
    order_id: int,
    data: SetStatusRequest,
) -> SetOrderStatusResponseWrapper:
    print(f"/campaigns/{campaign_id}/orders/{order_id}/status")
    return request_api.request_api_json(
        "PUT",
        f"/campaigns/{campaign_id}/orders/{order_id}/status",
        credentials,
        data,
        response_cls=SetOrderStatusResponseWrapper,
    )
