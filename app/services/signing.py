import base64
import hmac
from typing import Any

from app.core import Config
from .utils import cast

class SigningService:
    @staticmethod
    def signature(data: Any) -> bytes:
        return hmac.digest(Config.hmac_key, msg=cast(data), digest=Config.hmac_digest)

    @classmethod
    def sign(cls, data: Any) -> str:
        return base64.b64encode(cls.signature(data))

    @classmethod
    def verify(cls, data: Any, signature: str) -> bool:
        try:
            digest = base64.b64decode(signature, validate=True)
            return hmac.compare_digest(cls.signature(data), digest)
        except:
            return False
