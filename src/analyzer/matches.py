from pathlib import Path
from typing  import Optional

from data.registry import get_datasets, resolve_path
from src.domain.scanner   import ScanType
from src.domain.dataset   import Category, Dataset
from src.analyzer.scanner import scan
from src.domain.models.matches import ScanMatches, FormatScan, Matches

_CACHE = {}

def _severity_analyzer(severity: float) -> str:
    if   severity <=  0: return "No risk detected"
    elif severity <= 10: return "Very low risk"
    elif severity <= 20: return "Low risk"
    elif severity <= 30: return "Moderately low risk"
    elif severity <= 40: return "Moderate risk"
    elif severity <= 50: return "Moderately high risk, should improve"
    elif severity <= 60: return "Average risk, should improve"
    elif severity <= 70: return "High risk, should improve"
    elif severity <= 80: return "Risky password, needs to improve"
    elif severity <= 90: return "Very high risk, needs to improve"
    return "Unprotected; dangerous password, needs to improve"

def load_base(path: Path) -> list[str]:
    if path not in _CACHE:
        with open(path, encoding="utf-8") as file:
            _CACHE[path] = [line.strip() for line in file if line.strip()]
            
    return _CACHE[path]

def find_exactly(password: str, dataset: Dataset, scan_type: ScanType | list[ScanType], prioritize: Optional[ScanType | set[ScanType]] = None) -> tuple[int, dict]:
    matches: Matches = {
        "matches"  : [],
        "severity" : [],
    }
    
    try:
        base = load_base(path=resolve_path(dataset))
    
    except FileNotFoundError:
        return -1
    
    scann = scan(password=password, base=base, scan_type=scan_type, dataset=dataset, prioritize=prioritize)

    matches["matches"].append(scann["matches"])
    matches["severity"].append(scann["score"])

    return len(scann["matches"]) if not scann["matches"] is None else 0, matches

def scan_matches(password: str,
    dataset: Optional[Dataset | list[Dataset]] = None, path: Optional[Path | str] = None,
    scan_category: Optional[Category] = None, scan_type: ScanType | list[ScanType] = ScanType.COMPLETE,
    prioritize: Optional[ScanType | set[ScanType]] = None, statistic: bool = False) -> ScanMatches | tuple[ScanMatches, list[Dataset]]:
    
    if password is None: raise ValueError("No password were given as a parameter")

    finds:    list[FormatScan] = list()
    severity: list[float] = list()
    
    if not path is None and isinstance(path, (str, Path)):
        raise TypeError("Path need to be a Path or str")
        
    if path and type(path) is str:
        Path.parser(path)
    
    datasets: list[Dataset] 
    if dataset is None: datasets = get_datasets(scan_category)
    elif type(dataset) == type(list()): datasets == dataset
    else: datasets = [dataset]
    
    if not datasets:
        if scan_category:
            raise TypeError(f"No datasets were founded with this category: {scan_category}")
        raise ValueError(f"No datasets were given as a parameter")

    for dataset in datasets:
        scan:  tuple[int, dict] = find_exactly(password=password, dataset=dataset, scan_type=scan_type, prioritize=prioritize)
        format_scan: FormatScan = {
            "words_found" : scan[0],
            "matches"     : scan[1]["matches"],
            "severity"    : {round(sum(scan[1]["severity"]), 2)}
        }
        
        if format_scan["words_found"] > 0:
            severity.append(scan[1]["severity"])
            finds.append(format_scan)

    severity: list[float] = [i for sub in severity for i in sub]
    pctg_severity:  float = round(sum(severity) / max(len(severity), 1), 2)

    answer: ScanMatches = {
        "unprotected" : True if sum(k["words_found"] for k in finds) else False,
        "severity"    : {"percentage" : pctg_severity, "analysis" : _severity_analyzer(pctg_severity)},
        "finds"       : finds if finds else None,
    }
    
    return (answer, datasets) if statistic else answer
