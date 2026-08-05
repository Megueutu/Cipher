from dataclasses import dataclass
from src.domain.models.entropy import EntropyScore

@dataclass
class Entropy():
    bits:     float
    analysis: EntropyScore
    