from dataclasses import dataclass

@dataclass
class Entropy():
    top_attempts: int
    leet_guesses: int
    bits:         float