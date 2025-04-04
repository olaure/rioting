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
        """This method casts data to bytes that are then encoded
        """
        raw = cast(data, sort=False)
        return cls.Encoder(raw)

    @classmethod
    def decrypt(cls, data: str) -> Any:
        """This method expects the data to have been encrypted by the above method.
        The decryption is to decode and uncast the data from bytes.
        """
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
