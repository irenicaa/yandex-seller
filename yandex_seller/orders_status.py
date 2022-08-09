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
    id: Optional[int] = None
    count: Optional[int] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResultOrderDeliveryShipmentBox:
    id: Optional[int] = None
    height: Optional[int] = None
    depth: Optional[int] = None
    width: Optional[int] = None
    weight: Optional[int] = None
    items: Optional[list[SetOrderStatusResponseResultOrderDeliveryShipmentBoxItem]] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResultOrderDeliveryShipment:
    id: Optional[int] = None
    shipmentDate: Optional[str] = None
    shipmentTime: Optional[str] = None
    boxes: Optional[list[SetOrderStatusResponseResultOrderDeliveryShipmentBox]] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResultOrderDeliveryRegionParentParent:
    id: Optional[int] = None
    name: Optional[str] = None
    type: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResultOrderDeliveryRegionParent:
    id: Optional[int] = None
    name: Optional[str] = None
    type: Optional[str] = None
    parent: Optional[SetOrderStatusResponseResultOrderDeliveryRegionParentParent] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResultOrderDeliveryRegion:
    id: Optional[int] = None
    name: Optional[str] = None
    type: Optional[str] = None
    parent: Optional[SetOrderStatusResponseResultOrderDeliveryRegionParent] = None



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
    deliveryPartnerType: Optional[str] = None
    id: Optional[str] = None
    outletCode: Optional[str] = None
    price: Optional[float] = None
    serviceName: Optional[str] = None
    type: Optional[str] = None
    vat: Optional[str] = None
    outletId: Optional[int] = None
    dates: Optional[SetOrderStatusResponseResultOrderDeliveryDates] = None
    region: Optional[SetOrderStatusResponseResultOrderDeliveryRegion] = None
    shipments: Optional[list[SetOrderStatusResponseResultOrderDeliveryShipment]] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResult:
    id: Optional[int] = None
    status: Optional[str] = None
    substatus: Optional[str] = None
    creationDate: Optional[str] = None #TODO
    currency: Optional[str] = None
    cancelRequested: Optional[bool] = None
    itemsTotal: Optional[float] = None
    total: Optional[float] = None
    buyerTotal: Optional[int] = None
    buyerItemsTotal: Optional[int] = None
    buyerTotalBeforeDiscount: Optional[int] = None
    buyerItemsTotalBeforeDiscount: Optional[int] = None
    deliveryTotal: Optional[int] = None
    subsidyTotal: Optional[float] = None
    totalWithSubsidy: Optional[float] = None
    paymentType: Optional[str] = None
    paymentMethod: Optional[str] = None
    fake: Optional[bool] = None
    feeUE: Optional[int] = None
    delivery: Optional[SetOrderStatusResponseResultOrderDelivery] = None
    notes: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResultWrapper:
    order: Optional[SetOrderStatusResponseResult] = None


def set_order_status(
    credentials: credentials.Credentials,
    campaign_id: str,
    order_id: int,
    data: SetStatusRequest,
) -> SetOrderStatusResponseResultWrapper:
    return request_api.request_api_json(
        "PUT",
        f"/campaigns/{campaign_id}/orders/{order_id}/status",
        credentials,
        data,
        response_cls=SetOrderStatusResponseResultWrapper,
    )
