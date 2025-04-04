import json
from typing import Any

def cast(data: Any, sort: bool = True) -> bytes:
    """This casts any kind of data into a standard format.
    This is mandatory to be able to distinguish between strings and numbers.
    """
    return json.dumps(data, indent=None, sort_keys=sort).encode()

def uncast(data: bytes) -> Any:
    """This uncasts data casted by the method above.
    """
    return json.loads(data.decode())
