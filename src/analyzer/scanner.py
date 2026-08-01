import unicodedata
from src.domain.scanner import ScanType
from difflib import SequenceMatcher
from src.analyzer.translator import translate_password

def _normalize(word: str) -> str:
    return unicodedata.normalize("NFKD", word.lower().strip()).encode("ASCII", "ignore").decode("ASCII")

def scan(password: str, base: list, scan_type: ScanType) -> dict:
    acc, words = 0, {}
    nor_password = _normalize(password)
    amp = max(0.5, min(2.0, 7 / len(password)))

    def scan_regular() -> None:
        nonlocal words
        nonlocal acc

        if password.lower() == word.lower():
            acc += 100
            words.add((word, ScanType.REGULAR))

        elif nor_password == nor_word:
            acc += 80 * amp
            words.add((word, ScanType.REGULAR))
    
    def scan_sequence() -> None:
        nonlocal words
        nonlocal acc

        if nor_password in nor_word or nor_word in nor_password:
            acc += 60 * amp
            words.add((word, ScanType.SEQUENCE))

    def scan_pattern() -> None:
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
            words.append(word)

    def scan_alike() -> None:
        nonlocal words
        nonlocal acc

        if (translate_password(nor_password) == translate_password(nor_word)):
            acc += 60 * amp
            words.add((word, ScanType.ALIKE))
    
    for word in base:
        nor_word = _normalize(word)

        scan_regular()
        match scan_type:
            case ScanType.COMPLETE:
                scan_sequence()
                scan_pattern()
                scan_alike()
            
            case ScanType.SEQUENCE:
                scan_sequence()
            
            case ScanType.PATTERN:
                scan_pattern()
            
            case ScanType.ALIKE:
                scan_alike()

    return {
        "score" : acc,
        "matches" : words
    }