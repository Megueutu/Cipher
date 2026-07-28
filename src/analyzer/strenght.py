import string
from entropy import calculate_entropy

def calculate_strenght(password: str) -> int:
    score = calculate_entropy(password) * verify_len(password)
    
    return score

def verify_len(password: str) -> float:
    lenp = len(password)

    if lenp <= 3: return 0
    elif lenp < 5: return lenp * 0.8
    elif lenp < 8: return lenp * 1.4
    elif lenp < 13: return lenp * 1.8
    return lenp * 2.2