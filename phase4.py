def is_NFA(data: dict) -> bool:
    """Returns true if the FA is an NFA"""
    transitions = data["transitions"].copy()
    for i in transitions.values():
        for j in i.values():
            if j[0] == "{":
                return True
    
    return False