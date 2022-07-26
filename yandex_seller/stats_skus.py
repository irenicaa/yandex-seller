import datetime
from dataclasses import dataclass, field
from typing import Generator, Optional, Union

from dataclasses_json import Undefined, config, dataclass_json
from marshmallow import fields

from . import credentials, error_response, request_api

# Request


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class StatsSkusRequest:
    shopSkus: Optional[list[str]] = None


# Response


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetStatsSkusResponseWarehouseTariff:
    type: str
    percent: float
    amount: float


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetStatsSkusResponseWarehouseStock:
    type: str
    count: int


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetStatsSkusResponseWarehouse:
    id: int
    name: str
    stocks: list[GetStatsSkusResponseWarehouseStock]

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetStatsSkusResponseSkuHiding:
    type: str
    code: str
    message: str
    comment: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetStatsSkusResponseSkuWeightDimensions:
    length: float
    width: float
    height: float
    weight: float


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetStatsSkusResponseSku:
    shopSku: str
    marketSku: int
    name: str
    price: float
    categoryId: int
    categoryName: str
    weightDimensions: GetStatsSkusResponseSkuWeightDimensions
    hidings: Optional[list[GetStatsSkusResponseSkuHiding]] = None
    warehouses: Optional[list[GetStatsSkusResponseWarehouse]] = None
    tariffs:  Optional[list[GetStatsSkusResponseWarehouseTariff]] = None


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetStatsSkusResponseResult:
    shopSkus: list[GetStatsSkusResponseSku]


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetStatsSkusResponseWrapper:
    result: Optional[GetStatsSkusResponseResult] = None


def get_stats_skus(
    credentials: credentials.Credentials,
    campaign_id: str,
    data: StatsSkusRequest,
) -> GetStatsSkusResponseWrapper:
    return request_api.request_api_json(
        "POST",
        f"/campaigns/{campaign_id}/stats/skus",
        credentials,
        data,
        response_cls=GetStatsSkusResponseWrapper,
    )
