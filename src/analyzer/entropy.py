import string
from math import log2

# https://www.okta.com/identity-101/password-entropy/ -> https://www.pleacher.com/mp/mlessons/algebra/entropy.html

_base = {
    # tuple : pool
    "lowercase" : (string.ascii_lowercase, len(string.ascii_lowercase)),
    "uppercase" : (string.ascii_uppercase, len(string.ascii_uppercase)),
    "numbers"   : (string.digits, len(string.digits)),
    "punctuation" : (string.punctuation, len(string.punctuation)),
    "whitespace": (string.whitespace, len(string.whitespace)),
    "ascii": (''.join(map(chr, range(32))), 32)
}

def calculate_pool(password: str) -> int:
    pool = set()
    
    for i in range(len(password)):
        for k, seq in _base.values():
            if password[i] in seq:
                pool.add(k)
    
    pool, pool_sum = list(pool), 0
    for i in range(len(pool)):
        pool_sum += pool[i][1]

    return pool_sum

def calculate_entropy(password: str) -> float:
    pool = calculate_pool(password)
    
    return log2(pool**len(password))

def check_entropy(bits: int) -> str:
    if bits < 28: return "Very Weak; might keep out family members"
    elif bits < 36: return "Weak; should keep out most people, often good for desktop login passwords"
    elif bits < 60: return "Reasonable; fairly secure passwords for network and company passwords"
    elif bits < 128: return "Strong; can be good for guarding financial information"
    else: return "Very Strong; often overkill"
