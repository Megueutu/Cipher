from typing import TypedDict, Optional, Union
    
class Guesses(TypedDict):
    leet = Optional[int]

class EntropyScore(TypedDict):
    rank = Optional[Union[int, list[int]]]
    guesses = Optional[Guesses]
    