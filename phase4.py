def is_NFA(data: dict) -> bool:
    """Returns true if the FA is an NFA"""
    transitions = data["transitions"].copy()
    for i in transitions.values():
        for j in i.values():
            if j[0] == "{":
                return True
    
    return False

def convertDFAtoNFA(data: dict) -> None:
    if not is_NFA(data):
        for i in data["transitions"].keys():
            for j in data["transitions"][i].keys():
                data["transitions"][i][j] = "{'" + str(data["transitions"][i][j]) + "'}"

    return None

