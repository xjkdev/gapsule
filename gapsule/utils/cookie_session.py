import json
import base64

from typing import Union


def session_encode(obj: Union[list, dict, str]) -> bytes:
    return base64.encodebytes(json.dumps(obj).encode())


def session_decode(data: Union[str, bytes]) -> Union[dict, list, str]:
    if isinstance(data, str):
        data = data.encode()
    return json.loads(base64.decodebytes(data))
