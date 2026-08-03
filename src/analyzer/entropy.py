import string
from math import log2
from src.analyzer.matches import scan_matches
from src.domain.dataset import Category
from src.domain.entropy import Entropy
from src.analyzer.translator import translate_password

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

def calculate_entropy(password: str) -> Entropy:
    pool = _calculate_pool(password)
    
    scan, penalty = scan_matches(password=password), list()
    
    for i in [i for i in scan["finds"]]:
        for j in i["matches"]:
            for k in j:
                penalty.append(k["attempts"])
    
    if not sum([i["words_found"] for i in scan["finds"]]) > 0: pool = 1
    
    Entropy(bits=log2(pool**len(password)), top_attempts=max(penalty),
    leet_guesses=translate_password(password=password, counter=True)[1])
    
    return Entropy
