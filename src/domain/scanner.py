from dataclasses import dataclass

@dataclass
class Finds():
    sequence:  bool
    pattern:   bool
    blacklist: bool