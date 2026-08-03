import string
from math import log2
from src.analyzer.matches import scan_matches
from src.domain.dataset import Category

# https://www.okta.com/identity-101/password-entropy/ -> https://www.pleacher.com/mp/mlessons/algebra/entropy.html

_base = {
    # tuple : pool
    "lowercase"   : (string.ascii_lowercase, len(string.ascii_lowercase)),
    "uppercase"   : (string.ascii_uppercase, len(string.ascii_uppercase)),
    "numbers"     : (string.digits, len(string.digits)),
    "punctuation" : (string.punctuation, len(string.punctuation)),
    "whitespace"  : (string.whitespace, len(string.whitespace)),
    "ascii"       : (''.join(map(chr, range(32))), 32)
}

def _calculate_pool(password: str) -> int:
    pool = set()
    
    for i in range(len(password)):
        for string, seq in _base.values():
            if password[i] in string:
                pool.add((seq, string))
    
    return sum([i[0] for i in list(pool)])

def calculate_entropy(password: str) -> float:
    pool = _calculate_pool(password)
    
    scan = scan_matches(password=password, scan_category=Category.BLACKLIST)
    print(scan)
    
    if sum([i["words_found"] for i in scan["finds"]]) > 0: pool = 1
    
    return log2(pool**len(password))

def check_entropy(bits: int) -> str:
    if   bits <  28: return "Very Weak; might keep out family members"
    elif bits <  36: return "Weak; should keep out most people, often good for desktop login passwords"
    elif bits <  60: return "Reasonable; fairly secure passwords for network and company passwords"
    elif bits < 128: return "Strong; can be good for guarding financial information"
    else: return "Very Strong; often overkill"
