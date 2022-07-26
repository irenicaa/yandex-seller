from dataclasses import dataclass
from typing import Optional, Union

from dataclasses_json import Undefined, dataclass_json


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ErrorResponseDetail:
    code: Optional[Union[int, str]]
    message: Optional[str]

@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class ErrorResponse:
    error: Optional[ErrorResponseDetail] = None
    errors: Optional[list[ErrorResponseDetail]] = None
