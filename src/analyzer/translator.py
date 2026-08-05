from __future__ import annotations

_MULTI: list[tuple[str, tuple[str, ...]]] = [
    ("/-\\", ("a",)),
    ("/_\\", ("a",)),
    ("(_+", ("g",)),
    ("|_|", ("u",)),
    ("||_", ("u",)),
    ("\\|/", ("m",)),
    ("/\\\\", ("m",)),
    ("/\\/", ("n",)),
    ("\\/\\/", ("w",)),
    ("|-|", ("h",)),
    ("[)", ("d",)),
    ("|)", ("d",)),
    ("|<", ("k",)),
    ("|{", ("k",)),
    ("()", ("o",)),
    ("[]", ("o",)),
    ("{}", ("o",)),
    ("|*", ("p",)),
    ("|>", ("p",)),
    ("|o", ("q",)),
    ("><", ("x",)),
    ("`/", ("y",)),
    ("'/", ("y",)),
    ("|/", ("y",)),
    ("`)", ("j",)),
    ("_|", ("j",)),
    ("_/", ("j",)),
    ("|_", ("l",)),
    ("/\\", ("a",)),
    ("|3", ("b",)),
    ("13", ("b",)),
    ("[-", ("e",)),
    ("ph", ("f",)),
    ("|-", ("f",)),
    ("|=", ("f",)),
    ("||", ("h", "n")),
    ("|\\", ("n",)),
    ("|2", ("r",)),
    ("12", ("r",)),
    ("\\/", ("v",)),
]

_SINGLE: dict[str, tuple[str, ...]] = {
    "@": ("a",),
    "4": ("a",),
    "8": ("b",),
    "6": ("b",),
    "(": ("c",),
    "<": ("c",),
    "3": ("e",),
    "9": ("g",),
    "#": ("h",),
    "1": ("i", "l"),
    "!": ("i",),
    "|": ("i", "l"),
    "£": ("l",),
    "0": ("o",),
    "$": ("s",),
    "5": ("s",),
    "7": ("t",),
    "+": ("t",),
    "2": ("z",),
}

_ALL_PATTERNS: list[tuple[str, tuple[str, ...]]] = sorted(
    list(_MULTI) + list(_SINGLE.items()),
    key=lambda item: -len(item[0]),
)

def translate_password(password: str, counter: bool = False) -> str | tuple[str, int]:
    result: list[str] = list()
    c, i, n = 0, 0, len(password)
    while i < n:
        for pattern, letters in _ALL_PATTERNS:
            L: int = len(pattern)
            if password[i:i + L] == pattern:
                result.append(letters[0])
                c += 1
                i += L
                break
        else:
            result.append(password[i])
            c += 1
            i += 1
    return ("".join(result), c) if counter else "".join(result)

def translate_candidates(password: str, limit: int = 200) -> list[str]:
    n: int = len(password)
    results: list[str] = list()

    def dfs(i: int, built: list[str]) -> None:
        if len(results) >= limit:
            return
        if i == n:
            results.append("".join(built))
            return
        matched: bool = False
        for pattern, letters in _ALL_PATTERNS:
            L = len(pattern)
            if password[i:i + L] == pattern:
                matched = True
                for letter in letters:
                    built.append(letter)
                    dfs(i + L, built)
                    built.pop()
                    if len(results) >= limit:
                        return
        if not matched:
            built.append(password[i])
            dfs(i + 1, built)
            built.pop()

    dfs(0, [])
    return results
