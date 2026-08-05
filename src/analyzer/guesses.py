import re
from datetime import date

def _calculate_closeness(year: int) -> float:
    cur: int = date.today().year
    dis: int = abs(cur - year)

    pnlty: float = 0.1
    floor: float = 2000
    value: float = floor

    for _ in range(dis):
        value -= pnlty
        pnlty += 0.05

    ceil: int = 30

    return round(max(0, round(value, 4)) * ceil / floor, 2)

def guess_year(password: str) -> int:
    mul: float = 0
    c:   int   = 0

    for n in re.findall(r"\d+", password):
        if len(n) == 4:
            mul = _calculate_closeness(int(n))
            c += 1 * mul

    return c
