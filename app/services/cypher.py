import base64
import logging
from collections.abc import Callable
from functools import partial
from typing import Any

from .utils import (
    cast,
    uncast,
)


class CypherService:
    Encoder: Callable[[bytes], str]  = base64.b64encode
    Decoder: Callable[[str], bytes] = partial(base64.b64decode, validate=True)

    @classmethod
    def encrypt(cls, data: Any) -> str:
        logging.warning(f"Received data to encrypt '{data}'")
        raw = cast(data, sort=False)
        logging.warning(f"Encoding data '{raw}'")
        return cls.Encoder(raw)

    @classmethod
    def decrypt(cls, data: str) -> Any:
        logging.warning(f"Decrypting data {data}")
        try:
            decoded = cls.Decoder(data)
            return uncast(decoded)
        except Exception as _:
            logging.warning(f"Failed to decrypt, returning initial data {data}")
            return data

    @classmethod
    def encrypt_message(cls, data: Any) -> Any:
        if isinstance(data, dict):
            return {k: cls.encrypt(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [cls.encrypt(d) for d in data]
        return cls.encrypt(data)

    @classmethod
    def decrypt_message(cls, data: Any) -> Any:
        if isinstance(data, dict):
            return {k: cls.decrypt(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [cls.decrypt(d) for d in data]
        return cls.decrypt(data)
