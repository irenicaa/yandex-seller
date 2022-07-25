from dataclasses import dataclass
from typing import Optional

from dataclasses_json import Undefined, dataclass_json


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ErrorResponseDetail:
    code: Optional[int]
    message: Optional[str]

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ErrorResponse:
    error: ErrorResponseDetail
