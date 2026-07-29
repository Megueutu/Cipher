import secrets

def gen_salt(bits: int = 4) -> str:
    return secrets.token_hex(bits)
