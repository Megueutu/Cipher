from dataclasses import dataclass

@dataclass
class PasswordAnalysis():
    password: str
    length: int
    matches: dict
    strength: int
    malicious_injection: bool

# password
# length
# entropy
# pool
# dictionary_matches
# patterns_found
# repetitions
# leet_matches
# score
# strength