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

def union(data1: dict, data2: dict) -> dict:
    makeSingleFinalState(data1)
    makeSingleFinalState(data2)

    initial_state_d1 = data1['initial_state']
    initial_state_d2 = data2['initial_state']

    states_d1 = data1['states'][2:-2].split("','")
    states_d2 = data2['states'][2:-2].split("','")
    states_d1.sort(key=lambda x: int(x[1:]))
    states_d2.sort(key=lambda x: int(x[1:]))

    final_states_d1 = data1['final_states'][2:-2]
    final_states_d2 = data2['final_states'][2:-2]

    transitions_d1 = data1['transitions'].copy()
    transitions_d2 = data2['transitions'].copy()

    alphabet_d1 = data1['input_symbols'][2:-2].split("','")
    alphabet_d2 = data2['input_symbols'][2:-2].split("','")

    # change names of d2's states
    new_states_d2 = []
    new_transitions_d2 = {}
    n = len(states_d1)
    tmp = {}
    for i in states_d2:
        tmp[i] = "q" + str(n)
        n += 1
    for i in states_d2:
        new_states_d2.append(tmp[i])
    for i in transitions_d2.keys():
        new_transitions_d2[tmp[i]] = {}
        for j in transitions_d2[i].keys():
            list_of_transmited_states = transitions_d2[i][j][2:-2].split("','")
            new_transmited_states = []
            for k in list_of_transmited_states:
                new_transmited_states.append(tmp[k])
            transitions_d2[i][j] = "{"
            for k in new_transmited_states:
                transitions_d2[i][j] += "'" + k + "',"
            transitions_d2[i][j] = transitions_d2[i][j][:-1] + "}"
        new_transitions_d2[tmp[i]] = transitions_d2[i]

