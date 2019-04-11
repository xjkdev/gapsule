import json
import base64
from datetime import datetime, timezone
from typing import Union


def session_encode(obj: Union[list, dict, str]) -> bytes:
    return base64.encodebytes(json.dumps(obj).encode())


def session_decode(data: Union[str, bytes]) -> Union[dict, list, str]:
    if isinstance(data, str):
        data = data.encode()
    return json.loads(base64.decodebytes(data))


def parse_log_time(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S%z")


def format_log_time(dt: datetime = None) -> str:
    if dt is None:
        dt = datetime_now()
    if dt.timetz() is None:
        raise ValueError("Should not use offset-naive datetime")
    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")


def local_timezone() -> timezone:
    return datetime.now(timezone.utc).astimezone().tzinfo


def utc_timezone_now() -> datetime:
    return datetime.now(tz=timezone.utc)


def datetime_now(tz=None) -> datetime:
    if tz is None:
        return datetime.now(timezone.utc).astimezone()
    else:
        return datetime.now(tz=tz)
