import json
from typing import Any

def cast(data: Any, sort: bool = True) -> bytes:
    return json.dumps(data, indent=None, sort_keys=sort).encode()

def uncast(data: bytes) -> Any:
    return json.loads(data.decode())
