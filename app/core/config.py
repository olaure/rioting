import base64
import hashlib
import logging
import secrets
from pydantic import field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    hmac_key: bytes = b''
    hmac_digest: str = "sha256"
    
    @field_validator('hmac_digest', mode='before')
    @classmethod
    def validate_hmac_digest(cls, v: str) -> str:
        """This validates the provided algorithm is supported.
        """
        if v in hashlib.algorithms_guaranteed:
            return v
        logging.warning(f"Failed to validate provided digest {v}. Falling back to sha256")
        return "sha256"

    @field_validator('hmac_key', mode='before')
    @classmethod
    def validate_hmac_key(cls, v: str) -> bytes:
        """Expecting a base64 encoded key of length at least 32 bytes.
        """
        try:
            decoded = base64.b64decode(v)
            if len(decoded) < 32:
                raise ValueError('incorrect_length')
            return decoded
        except Exception as err:
            logging.warning(f"Failed to validate provided key : {err}. Generating a new one.")
            return secrets.token_bytes(32)

Config = Settings()