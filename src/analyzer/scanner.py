import unicodedata
from src.domain.scanner import ScanType
from src.domain.dataset import Dataset
from difflib import SequenceMatcher
from src.analyzer.translator import translate_password

def _normalize(word: str) -> str:
    return unicodedata.normalize("NFKD", word.lower().strip()).encode("ASCII", "ignore").decode("ASCII")

def scan(password: str, base: list, scan_type: ScanType, dataset: Dataset) -> dict:
    acc, words = 0, list()
    nor_password = _normalize(password)
    amp = max(0.5, min(2.0, 7 / len(password)))

    result = {
        "score" : None,
        "matches" : None
    }

    def scan_regular(word: str, nor_word: str) -> None:
        nonlocal dataset
        nonlocal words
        nonlocal acc

        if password.lower() == word.lower():
            acc += 100
            words.append({"word" : word, "scan_type" : ScanType.REGULAR.value, "dataset" : dataset.filename})

        elif nor_password == nor_word:
            acc += 80 * amp
            words.append({"word" : word, "scan_type" : ScanType.REGULAR.value, "dataset" : dataset.filename})
    
    def scan_sequence(word: str, nor_word: str) -> None:
        nonlocal dataset
        nonlocal words
        nonlocal acc

        if nor_password in nor_word or nor_word in nor_password:
            acc += 60 * amp
            words.append({"word" : word, "scan_type" : ScanType.SEQUENCE.value, "dataset" : dataset.filename})

    def scan_pattern(word: str, nor_word: str) -> None:
        nonlocal dataset
        nonlocal words
        nonlocal acc

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
            words.append({"word" : word, "scan_type" : ScanType.PATTERN.value, "dataset" : dataset.filename})

    def scan_alike(word: str, nor_word: str) -> None:
        nonlocal dataset
        nonlocal words
        nonlocal acc

        if (translate_password(nor_password) == translate_password(nor_word)):
            acc += 60 * amp
            words.append({"word" : word, "scan_type" : ScanType.ALIKE.value, "dataset" : dataset.filename})
    
    for word in base:
        nor_word = _normalize(word)

        scan_regular(word, nor_word)
        match scan_type:
            case ScanType.COMPLETE:
                scan_sequence(word, nor_word)
                scan_pattern(word, nor_word)
                scan_alike(word, nor_word)
            
            case ScanType.SEQUENCE:
                scan_sequence(word, nor_word)
            
            case ScanType.PATTERN:
                scan_pattern(word, nor_word)
            
            case ScanType.ALIKE:
                scan_alike(word, nor_word)

    result["score"], result["matches"] = acc, words if words != set() else None

    return result