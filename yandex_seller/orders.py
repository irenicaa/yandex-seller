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

# Request


# @dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class OrdersRequest:
    campaignId: Optional[int] = None
    fromDate: Optional[str] = None
    toDate: Optional[str] = None
    page: Optional[str] = None
    status: Optional[str] = None
    substatus: Optional[str] = None
    fake: Optional[bool] = False
    supplierShipmentDateFrom: Optional[str] = None
    supplierShipmentDateTo: Optional[str] = None
    hasCis: Optional[bool] = False


# Response


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponsePager:
    total: Optional[int] = None
    to: Optional[int] = None
    from_: Optional[int] = field(
        default=None,
        metadata=config(field_name="from"),
    )
    currentPage: Optional[int] = None
    pagesCount: Optional[int] = None
    pageSize: Optional[int] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponseItemDetail:
    itemStatus: str
    itemCount: int
    updateDate: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponseItem:
    id: int
    feedId: int
    offerId: str
    feedCategoryId: str
    offerName: str
    partnerWarehouseId: int
    count: int
    price: int
    buyerPrice: int
    buyerPriceBeforeDiscount: int
    vat: str
    subsidy: int
    feeUE: int
    shopSku: str
    details: Optional[list[GetOrdersResponseItemDetail]] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponseDeliveryShipmentBox:
    id: int
    fulfilmentId: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponseDeliveryShipmentItem:
    id: int
    count: int


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponseDeliveryShipmentTrack:
    trackCode: str
    deliveryServiceId: int

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponseDeliveryShipment:
    id: int
    shipmentDate: str
    height: int
    depth: int
    width: int
    weight: int
    status: str
    tracks: list[GetOrdersResponseDeliveryShipmentTrack]
    items: list[GetOrdersResponseDeliveryShipmentItem]
    boxes: list[GetOrdersResponseDeliveryShipmentBox]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponseDeliveryRegionParentParent:
    id: int
    name: str
    type: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponseDeliveryRegionParent:
    id: int
    name: str
    type: str
    parent: GetOrdersResponseDeliveryRegionParentParent


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponseDeliveryRegion:
    id: int
    name: str
    type: str
    parent: GetOrdersResponseDeliveryRegionParent


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponseDelivery:
    type: str
    serviceName: str
    deliveryPartnerType: str
    region: GetOrdersResponseDeliveryRegion
    shipments: list[GetOrdersResponseDeliveryShipment]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponse:
    id: int
    status: str
    substatus: str
    creationDate: str
    currency: str
    itemsTotal: int
    total: int
    buyerTotal: int
    buyerItemsTotal: int
    buyerTotalBeforeDiscount: int
    buyerItemsTotalBeforeDiscount: int
    subsidyTotal: float
    deliveryTotal: int
    totalWithSubsidy: float
    paymentType: str
    paymentMethod: str
    feeUE: int
    fake: bool
    delivery: GetOrdersResponseDelivery
    taxSystem:str
    items: list[GetOrdersResponseItem]
    notes: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponseWrapper:
    orders: Optional[list[GetOrdersResponse]] = None
    pager: Optional[GetOrdersResponsePager] = None


def get_campaigns_orders(
    credentials: credentials.Credentials,
    campaign_id: str,
    data: OrdersRequest,
) -> GetOrdersResponseWrapper:
    data_get = {}
    raw_data = dataclasses.asdict(data)
    for key, value in raw_data.items():
        if value is not None:
            data_get[key] = value

    data_for_request = urllib.parse.urlencode(data_get)
    return request_api.request_api_json(
        "GET",
        f"/campaigns/{campaign_id}/orders?{data_for_request}",
        credentials,
        None,
        response_cls=GetOrdersResponseWrapper,
    )


def get_campaigns_orders_iterative(
    credentials: credentials.Credentials,
    campaign_id: str,
    data: OrdersRequest,
) -> Generator[GetOrdersResponse, None, None]:
    while True:
        returns = get_campaigns_orders(credentials, campaign_id, data)
        if returns.orders == []:
            break

        yield returns

        data.page += 1
