import dataclasses
import datetime
import urllib
from dataclasses import dataclass, field
from typing import Generator, Optional, Union

from dataclasses_json import CatchAll, Undefined, config, dataclass_json
from marshmallow import fields

from . import credentials, error_response, request_api

# Response


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class GetReceptionTransferActResult:
    status: str


def get_reception_transfer_act(
    credentials: credentials.Credentials,
    campaign_id: str,
) -> GetReceptionTransferActResult:
    response = request_api.request_api_raw(
        "GET",
        f"/campaigns/{campaign_id}/shipments/reception-transfer-act",
        credentials,
        None,
        # response_cls=GetReceptionTransferActResult,
    )
    return response.content
