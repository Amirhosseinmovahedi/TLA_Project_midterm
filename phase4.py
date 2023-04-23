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

def makeSingleFinalState(data: dict) -> None:
    states = data['states'][2:-2].split("','")
    states.sort(key=lambda x: int(x[1:]))
    new_final_state = "q" + str(int(states[-1][1:]) + 1)
    final_states = data['final_states'][2:-2].split("','")
    if not is_NFA(data):
        convertDFAtoNFA(data)
    if len(final_states) > 1:
        data["states"] = data["states"][:-1] + ",'" + new_final_state + "'}"
        data['final_states'] = "{'" + str(new_final_state) + "'}"
        for i in final_states:
            if data["transitions"][i].get("", False):
                data["transitions"][i][""] = data["transitions"][i][-1] + ",'" + new_final_state + "'}"
            else:
                data["transitions"][i][""] = "{'" + new_final_state + "'}"
        data['transitions'][new_final_state] = {}

