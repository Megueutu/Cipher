import os, secrets

_cases = ("lower", "upper", "mix")

def gen_password(
    lenght:  int  = 8,
    numbers: bool = True,
    case:    str  = "mix",
    specialChar: bool = False,
) -> str:

def gen_salt(bits: int = 12) -> str:
    return secrets.token_hex(bits)