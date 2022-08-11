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
class ActConfirmDataRequest:
    externalShipmentId: Optional[str] = None
    orderIds: Optional[list[int]] = None


# Response


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class SetOrderStatusResponseResult:
    status: Optional[str] = None


def get_act_confirm(
    credentials: credentials.Credentials,
    campaign_id: str,
    shipment_id: str,
    data: ActConfirmDataRequest,
) -> SetOrderStatusResponseResult:
    return request_api.request_api_json(
        "POST",
        f"/campaigns/{campaign_id}/first-mile/shipments/{shipment_id}/confirm",
        credentials,
        data,
        response_cls=SetOrderStatusResponseResult,
    )
