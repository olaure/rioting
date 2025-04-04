import base64
import hmac
import logging
import secrets
from typing import Any

from .utils import cast

# TODO move this to settings and at init
HMAC_KEY = secrets.token_bytes(32)
HMAC_DIGEST="sha256"

class SigningService:
    @staticmethod
    def signature(data: Any) -> bytes:
        return hmac.digest(HMAC_KEY, msg=cast(data), digest=HMAC_DIGEST)

    @classmethod
    def sign(cls, data: Any) -> str:
        logging.warning(f"Signing data {data}")
        return base64.b64encode(cls.signature(data))

    @classmethod
    def verify(cls, data: Any, signature: str) -> bool:
        logging.warning(f'[verify] Received {data} with signature {signature}')
        try:
            digest = base64.b64decode(signature, validate=True)
            logging.warning("Digest successfully decoded")
            return hmac.compare_digest(cls.signature(data), digest)
        except:
            return False
