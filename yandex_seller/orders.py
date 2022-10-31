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
    itemStatus: Optional[str] = None
    itemCount: Optional[int] = None
    updateDate: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponseItem:
    id: Optional[int] = None
    feedId: Optional[int] = None
    offerId: Optional[str] = None
    feedCategoryId: Optional[str] = None
    offerName: Optional[str] = None
    partnerWarehouseId: Optional[int] = None
    count: Optional[int] = None
    price: Optional[int] = None
    buyerPrice: Optional[int] = None
    buyerPriceBeforeDiscount: Optional[int] = None
    vat: Optional[str] = None
    subsidy: Optional[int] = None
    feeUE: Optional[int] = None
    shopSku: Optional[str] = None
    details: Optional[list[GetOrdersResponseItemDetail]] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponseDeliveryShipmentBox:
    id: Optional[int] = None
    fulfilmentId: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponseDeliveryShipmentItem:
    id: Optional[int] = None
    count: Optional[int] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponseDeliveryShipmentTrack:
    trackCode: Optional[str] = None
    deliveryServiceId: Optional[int] = None

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponseDeliveryShipment:
    id: Optional[int] = None
    shipmentDate: Optional[str] = None
    height: Optional[int] = None
    depth: Optional[int] = None
    width: Optional[int] = None
    weight: Optional[int] = None
    status: Optional[str] = None
    tracks: Optional[list[GetOrdersResponseDeliveryShipmentTrack]] = None
    items: Optional[list[GetOrdersResponseDeliveryShipmentItem]] = None
    boxes: Optional[list[GetOrdersResponseDeliveryShipmentBox]] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponseDeliveryRegionParentParent:
    id: Optional[int] = None
    name: Optional[str] = None
    type: Optional[str] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponseDeliveryRegionParent:
    id: Optional[int] = None
    name: Optional[str] = None
    type: Optional[str] = None
    parent: Optional[GetOrdersResponseDeliveryRegionParentParent] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponseDeliveryRegion:
    id: Optional[int] = None
    name: Optional[str] = None
    type: Optional[str] = None
    parent: Optional[GetOrdersResponseDeliveryRegionParent] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponseDelivery:
    type: Optional[str] = None
    serviceName: Optional[str] = None
    deliveryPartnerType: Optional[str] = None
    region: Optional[GetOrdersResponseDeliveryRegion] = None
    shipments: Optional[list[GetOrdersResponseDeliveryShipment]] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetOrdersResponse:
    id: Optional[int] = None
    status: Optional[str] = None
    substatus: Optional[str] = None
    creationDate: Optional[str] = None
    currency: Optional[str] = None
    itemsTotal: Optional[int] = None
    total: Optional[int] = None
    buyerTotal: Optional[int] = None
    buyerItemsTotal: Optional[int] = None
    buyerTotalBeforeDiscount: Optional[int] = None
    buyerItemsTotalBeforeDiscount: Optional[int] = None
    subsidyTotal: Optional[float] = None
    deliveryTotal: Optional[int] = None
    totalWithSubsidy: Optional[float] = None
    paymentType: Optional[str] = None
    paymentMethod: Optional[str] = None
    feeUE: Optional[int] = None
    fake: Optional[bool] = None
    delivery: Optional[GetOrdersResponseDelivery] = None
    taxSystem: Optional[str] = None
    items: Optional[list[GetOrdersResponseItem]] = None
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
