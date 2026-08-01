import unicodedata
from domain.scanner import ScanType
from difflib import SequenceMatcher

def _normalize(word: str) -> str:
    return unicodedata.normalize("NFKD", word.lower().strip()).encode("ASCII", "ignore").decode("ASCII")

def scan_sequence(password: str, word: str) -> float:
    return 

def scan_pattern():
    return

def scan_alike():
    return

def scan(base: list, password: str, scan_type: ScanType) -> float:
    acc = 0
    
    for word in base:
        match scan_type:
            case ScanType.COMPLETE:
                acc += scan_sequence(password, word) \
                + scan_pattern(password, word)       \
                + scan_alike(password, word)
            
            case ScanType.SEQUENCE:
                acc += scan_sequence(password, word)
            
            case ScanType.PATTERN:
                acc += scan_pattern(password, word)
            
            case ScanType.ALIKE:
                acc += scan_alike(password, word)