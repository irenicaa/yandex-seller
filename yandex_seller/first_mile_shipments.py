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
class FirstMileShipmentsRequest:
    dateFrom: Optional[str] = None
    dateTo: Optional[str] = None
    statuses: Optional[list[str]] = None
    orderIds: Optional[list[int]] = None


# Response


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResultShipmentDeliveryService:
    id: Optional[int] = None
    name: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResultShipment:
    id: Optional[int] = None
    planIntervalFrom: Optional[str] = None
    planIntervalTo: Optional[str] = None
    shipmentType: Optional[str] = None
    externalId: Optional[str] = None
    status: Optional[str] = None
    statusDescription: Optional[str] = None
    deliveryService: Optional[SetOrderStatusResponseResultShipmentDeliveryService] = None
    draftCount: Optional[int] = None
    factCount: Optional[int] = None
    plannedCount: Optional[int] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResultPaging:
    nextPageToken: Optional[str] = None

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResult:
    shipments: list[SetOrderStatusResponseResultShipment]
    paging: Optional[SetOrderStatusResponseResultPaging] = None

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResultWrapper:
    result: SetOrderStatusResponseResult
    status: Optional[str] = None


def get_first_mile_data(
    credentials: credentials.Credentials,
    campaign_id: str,
    data: FirstMileShipmentsRequest,
) -> SetOrderStatusResponseResultWrapper:
    return request_api.request_api_json(
        "PUT",
        f"/campaigns/{campaign_id}/first-mile/shipments",
        credentials,
        data,
        response_cls=SetOrderStatusResponseResultWrapper,
    )
