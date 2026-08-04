from difflib import SequenceMatcher

def guess_year(password: str) -> int:
    c = 0
    
    for i in [str(i) for i in list(range(100, 10000))]:
        if i in password or password in i:
            c += 1
            
    return c

print(guess_year("password"))