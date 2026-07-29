import secrets
from generators.salt import gen_salt
from string import printable
from math import log

def _ddcf(base: str) -> float:
    len(base)

def hash_password(password: str, amp_f: str, bits = 12) -> tuple[str, str]:
    salt = gen_salt()
    hashed = []
    
    for i in password:
        orig_index = printable.index(i)
        amp = log(_ddcf(amp_f), orig_index)
    
    