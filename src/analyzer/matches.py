from data.analysis.registry import get_datasets, resolve_path
from domain.scanner import ScanType
from domain.dataset import Category
from difflib import SequenceMatcher
from dataclasses import dataclass
from typing import overload
from scanner import scan

_CACHE = {}

def _severity_analyzer(severity: int) -> tuple[bool, str]:
    if severity > 100:  return "Protected; very low risk"
    elif severity > 80: return "Protected; low risk"
    elif severity > 50: return "Protected; average risk, should improve"
    elif severity > 30: return "Unprotected; risky password, should improve"
    elif severity > 10: return "Unprotected; very high risk, should improve"
    return "Unprotected; dangerous password, needs to improve"

def load_base(path):
        if path not in _CACHE:
            with open(path) as f:
                _CACHE[path] = set(f.read().split("\n"))
        return _CACHE[path]

def find_exactly(password: str, path: str, scan_type: ScanType) -> tuple[int, dict]:
    matches = {
        "matches"  : [],
        "severity" : [],
    }
    
    try:
        base = load_base(path)
    
    except FileNotFoundError:
        return -1
    
    scann = scan(password, base, scan_type)

    matches["matches"].append(scann["matches"])
    matches["severity"].append(scann["score"])
    
    return len(scann["matches"]), matches

def scan_matches(password: str, scan_category: Category, scan_type: ScanType) -> dict:
    datasets, finds, severity = get_datasets(scan_category), list(), list()
    
    for dataset in datasets:
        scan = find_exactly(password, resolve_path(dataset), scan_type)
        if tuple(scan[1].values())[0] != []:
            severity.append(scan[1]["severity"])
            finds.append(scan)
    
    pct_severity = round(sum(severity) / len(severity), 2)
    
    answer = {
        "unprotected" : True if finds else False,
        "severity"    : (pct_severity, _severity_analyzer(pct_severity)),
        "finds"       : finds,
    }
    
    return answer

@dataclass
class MatchAnalizer:
    severity: float
    matches:  dict
    
    def __init__(self, password):
        matches = scan_matches(password)
        
        self.severity = matches["severity"]
        self.matches  = matches["finds"]
    
@overload
def scan_matches(password: MatchAnalizer):
    return scan_matches(password)
