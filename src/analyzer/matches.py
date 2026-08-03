from data.registry import get_datasets, resolve_path
from src.domain.scanner import ScanType
from src.domain.dataset import Category, Dataset
from src.analyzer.scanner import scan
from dataclasses import dataclass
from typing import overload

_CACHE = {}

def _severity_analyzer(severity: int) -> tuple[bool, str]:
    if severity   <= 0: return "No risk detected"
    elif severity >  0: return "Very low risk"
    elif severity > 20: return "Low risk"
    elif severity > 50: return "Average risk, should improve"
    elif severity > 80: return "Risky password, should improve"
    elif severity > 90: return "Very high risk, should improve"
    return "Unprotected; dangerous password, needs to improve"

def load_base(path):
        if path not in _CACHE:
            with open(path, encoding="utf-8") as f:
                _CACHE[path] = set(f.read().split("\n"))
        return _CACHE[path]

def find_exactly(password: str, dataset: Dataset, scan_type: ScanType) -> tuple[int, dict]:
    matches = {
        "matches"  : [],
        "severity" : [],
    }
    
    try:
        base = load_base(resolve_path(dataset))
    
    except FileNotFoundError:
        return -1
    
    scann = scan(password, base, scan_type, dataset)

    matches["matches"].append(scann["matches"])
    matches["severity"].append(scann["score"])

    return len(scann["matches"]) if not scann["matches"] is None else 0, matches

def scan_matches(password: str, scan_category: Category = None, scan_type: ScanType = ScanType.COMPLETE) -> dict:
    datasets, finds, severity = get_datasets(scan_category), list(), list()

    if datasets == []:
        raise TypeError(f"No datasets were founded with this category: {scan_category}")

    for dataset in datasets:
        scan = find_exactly(password, dataset, scan_type)
        format_scan = {
            "words_found" : scan[0],
            "matches"     : scan[1]["matches"],
            "severity"    : f"{round(sum(scan[1]["severity"]), 2)}%"
        }

        if format_scan["words_found"] > 0:
            severity.append(scan[1]["severity"])
            finds.append(format_scan)

    severity = [i for sub in severity for i in sub]
    pct_severity = round(sum(severity) / max(len(severity), 1), 2)

    answer = {
        "unprotected" : True if sum(k["words_found"] for k in finds) else False,
        "severity"    : (f"{pct_severity}%", _severity_analyzer(pct_severity)),
        "finds"       : finds if finds != [] else None,
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
    
# def scan_matches(password: MatchAnalizer):
#     return scan_matches(password)