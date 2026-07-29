import os, secrets

_cases = ("lower", "upper", "mix")

def gen_password(
    lenght:  int  = 8,
    numbers: bool = True,
    case:    str  = "mix",
    specialChar: bool = False,
) -> str:
    
    if case not in _cases: raise ValueError(f"Case needs to be one of these types: {_cases}")
    
