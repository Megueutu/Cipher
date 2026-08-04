import unicodedata
from src.analyzer.translator import translate_password, translate_candidates
from src.domain.scanner import ScanType
from src.domain.dataset import Dataset, Category
from difflib import SequenceMatcher
from typing import Callable

def _normalize(word: str) -> str:
    return unicodedata.normalize("NFKD", word.lower().strip()).encode("ASCII", "ignore").decode("ASCII")

def scan(password: str, base: list, dataset: Dataset,
    scan_type: ScanType | list[ScanType] = ScanType.COMPLETE, prioritize: ScanType | set[ScanType] = None) -> dict:
    
    if prioritize is ScanType.COMPLETE: raise TypeError("ScanType prioritizer cannot be COMPLETE")
    
    acc, attempts, words = 0, 0, list()
    nor_password = _normalize(password)
    amp = max(0.5, min(2.0, 7 / len(password)))

    result = {
        "score"    : None,
        "matches"  : None,
        "attempts" : 0,
    }
    
    def global_attempts() -> None:
        nonlocal result
        result["attempts"] += 1

    def internal_attempts() -> int:
        nonlocal attempts
        return attempts

    def scan_regular(word: str, nor_word: str) -> bool:
        nonlocal dataset
        nonlocal words
        nonlocal acc

        global_attempts()

        if password.lower() == word.lower():
            acc += 100
            words.append({"word" : word, "scan_type" : ScanType.REGULAR.value, "dataset" : dataset.filename, "attempts" : internal_attempts()})
            return True

        elif nor_password == nor_word:
            acc += 80 * amp
            words.append({"word" : word, "scan_type" : ScanType.REGULAR.value, "dataset" : dataset.filename, "attempts" : internal_attempts()})
            return True

        return False
    
    def scan_sequence(word: str, nor_word: str) -> bool:
        nonlocal attempts
        nonlocal dataset
        nonlocal words
        nonlocal acc
        
        global_attempts()

        if nor_password in nor_word or nor_word in nor_password:
            acc += 60 * amp
            words.append({"word" : word, "scan_type" : ScanType.SEQUENCE.value, "dataset" : dataset.filename, "attempts" : internal_attempts()})
            return True
        
        return False

    def scan_pattern(word: str, nor_word: str) -> bool:
        nonlocal attempts
        nonlocal dataset
        nonlocal words
        nonlocal acc
        
        global_attempts()

        def match_analyzer(str1: str, str2: str) -> float:
            smal = min(len(str1), len(str2))

            if smal == 0: return 0
            if abs(len(str1) - len(str2)) > 3: return 0

            matcher = SequenceMatcher(None, str1, str2)
            match = matcher.find_longest_match(0, len(str1), 0, len(str2))

            limit_n = 4

            if smal < limit_n: 
                if match.size != smal: return 0.0

            else:
                if match.size < limit_n: return 0.0
                if match.size < smal * 0.8: return 0.0

            return match.size / smal

        score = max(match_analyzer(password.lower(), word.lower()), match_analyzer(nor_password, nor_word))

        if score > 0:
            acc += score * 60 * amp
            words.append({"word" : word, "scan_type" : ScanType.PATTERN.value, "dataset" : dataset.filename, "attempts" : internal_attempts()})
            return True
        
        return False

    def scan_alike(word: str, nor_word: str) -> bool:
        nonlocal attempts
        nonlocal dataset
        nonlocal words
        nonlocal acc

        global_attempts()
        
        if translate_password(nor_word) in translate_candidates(nor_password):
            acc += 60 * amp
            words.append({"word" : word, "scan_type" : ScanType.ALIKE.value, "dataset" : dataset.filename, "attempts" : internal_attempts()})
            return True
        
        return False
    
    def _scann_order(scanners: dict[ScanType, Callable]) -> list[Callable]:
        priorities: list[Callable] = list()
        for i in list(prioritize) if type(prioritize) is set else [prioritize]:
            if i in [scan_type] if type(scan_type) is ScanType else scan_type:
                priorities.append(scanners[i])
        
        return priorities
    
    scanners: dict[ScanType, Callable[[str, str], bool]] = {
        ScanType.SEQUENCE : scan_sequence,
        ScanType.PATTERN  : scan_pattern,
        ScanType.ALIKE    : scan_alike,
    }
    
    defs: list[Callable[[str, str], bool]] = _scann_order(scanners=scanners)
    
    if prioritize: 
        scanners = _scann_order(scanners=scanners)
    
    for word in base:
        nor_word = _normalize(word)
        attempts += 1

        if scan_regular(word, nor_word): continue
        for fun in defs:
            if fun(word, nor_word): break

    result["score"], result["matches"] = acc, words if words != set() else None

    return result