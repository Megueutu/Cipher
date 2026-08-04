from typing import Optional, TypedDict

from src.domain.dataset import Dataset
from src.domain.scanner import ScanType

class ScannerFinds(TypedDict):
    word:      str
    attempts:  int
    dataset:   Dataset
    scan_type: ScanType

class ScannerResult(TypedDict):
    matches:  Optional[list[ScannerFinds]]
    score:    Optional[float]
    attempts: int