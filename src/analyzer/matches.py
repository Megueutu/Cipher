import unicodedata
from data.analysis.registry import get_datasets, resolve_path
from domain.scanner import ScanType
from domain.dataset import Category
from difflib import SequenceMatcher
from dataclasses import dataclass
from typing import overload

_CACHE = {}

def _severity_analyzer(severity: int) -> tuple[bool, str]:
    if severity > 100:  return "Protected; very low risk"
    elif severity > 80: return "Protected; low risk"
    elif severity > 50: return "Protected; average risk, should improve"
    elif severity > 30: return "Unprotected; risky password, should improve"
    elif severity > 10: return "Unprotected; very high risk, should improve"
    return "Unprotected; dangerous password, needs to improve"

def _normalize(word: str) -> str:
    return unicodedata.normalize("NFKD", word.lower().strip()).encode("ASCII", "ignore").decode("ASCII")

def load_base(path):
        if path not in _CACHE:
            with open(path) as f:
                _CACHE[path] = set(f.read().split("\n"))
        return _CACHE[path]

def find_exactly(password: str, path: str, scan_type: ScanType) -> tuple[int, dict]:
    matches, counter = {
        "matches"  : [],
        "severity" : [],
    }, 0
    
    try:
        base = load_base(path)
    
    except FileNotFoundError:
        return -1
    
    def apply_match(value: int):
        nonlocal counter
        nonlocal matches
        
        counter += 1
        matches["matches"].append(word)
        matches["severity"].append(value)
    
    def match_analyzer(str1, str2) -> float:
        smal = min(len(str1), len(str2))
        
        def sequence_match() -> int:
            nonlocal str1
            nonlocal str2
            
            if abs(len(str1) - len(str2)) > 3: return 0
            
            matcher = SequenceMatcher(None, str1, str2)
            match = matcher.find_longest_match(0, len(str1), 0, len(str2))
            
            nonlocal smal
            limit_n = 4
            
            if smal < limit_n: return match.size if match.size == smal else 0
            if match.size < limit_n: return 0
            
            return 0 if match.size < smal * 0.8 else match.size

        return round(sequence_match() / smal * 10, 2)
    
    nor_password = _normalize(password)
    for word in base:
        nor_word = _normalize(word)
        
        if password == word:
            apply_match(100)
        
        elif password.lower() == word.lower().strip():
            apply_match(90 * (len(password) * 0.08))
        
        elif nor_password == nor_word:
            apply_match(80 * (len(password) * 0.08))
        
        elif nor_password in nor_word or nor_word in nor_password:
            apply_match(60 * (len(password) * 0.08))
        
        elif len(password) > 4 and ScanType.value == "sequence": 
            score = match_analyzer(password, word)
            score_nor = match_analyzer(nor_password, nor_word)
            
            if score: apply_match(score * 1.2)
            elif score_nor: apply_match(score_nor)
        
    if matches["severity"] != []:
        severity = sum(matches["severity"]) / len(matches["severity"])
        matches["severity"] = severity
    
    return counter, matches

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