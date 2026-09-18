from dataclasses import dataclass
from typing import Optional, Dict


@dataclass(frozen=True)
class JwtKeyPair:
    kid: str
    private_key_pem: str
    public_key_pem: str


@dataclass(frozen=True)
class JwtKeySet:
    active: JwtKeyPair
    previous: Optional[JwtKeyPair] = None

    def public_keys_by_kid(self) -> Dict[str, str]:
        out = {self.active.kid: self.active.public_key_pem}
        if self.previous:
            out[self.previous.kid] = self.previous.public_key_pem
        return out