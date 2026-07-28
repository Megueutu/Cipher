from pathlib import Path

_extensions = (".txt", ".csv", ".parquet", ".json", ".xml")

def _gen_path(name: str) -> dict:
    possibilities = {
        "original" : [name+_extensions[i] for i in range(len(_extensions))],
        "examples" : [name+".example"+_extensions[i] for i in range(len(_extensions))],
    }
    
    return possibilities

def find_path(archive: str) -> str:
    route, possibilities = Path("data/analysis/"), tuple(_gen_path(archive).values())
    
    folders = (
        ("original", possibilities[0]),
        ("examples", possibilities[1]),
    )

    for folder, files in folders:
        for file in files:
            path = route / folder / file
            if path.exists():
                return str(path)
        
    raise FileNotFoundError(f"There are no such file \"{archive}\" in {route}")

AVAILABLE_FILES = ["animals", "books", "keyboard-patterns", "names", "rockyou"]

def get_paths() -> dict:
    return {item: find_path(item) for item in AVAILABLE_FILES}
