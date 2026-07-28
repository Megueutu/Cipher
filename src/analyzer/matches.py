def find_exactly(password: str, path: str, base_category: str) -> tuple[int, dict]:
    matches, counter = {
        "matches"  : [],
        "category" : [],
    }, 0
    
    try:
        with open(path, 'r', encoding='utf-8') as co:
            base = set(co.read().split("\n"))    
            
    except FileNotFoundError:
        return -1
    
    for word in base:
        if password in word:
            counter += 1
            matches["matches"].append(word)
            
    if counter:
        matches["category"].append(base_category)
        
    return counter, matches
