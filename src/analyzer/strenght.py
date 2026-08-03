from entropy import calculate_entropy
from matches import scan_matches, MatchAnalizer
from dataclasses import dataclass

@dataclass
class PasswordAnalizer:
    password: str
    lenght: int
    entropy: bool
    matcher: MatchAnalizer

    def __init__(self, password):
        self.password = password
        self.lenght   = len(password)
        self.matcher  = scan_matches(password)
        self.entropy  = calculate_entropy(password)

def calculate_strenght(password: PasswordAnalizer) -> tuple[float, str]:
    return 0

def verify_len(password: str) -> float:
    lenp = len(password)

    if lenp   <= 3: return 0
    elif lenp <  5: return lenp * 0.8
    elif lenp <  8: return lenp * 1.4
    elif lenp < 13: return lenp * 1.8
    return lenp * 2.2