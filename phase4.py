import json

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

    transitions_d2 = new_transitions_d2
    new_alphabet = alphabet_d1 + alphabet_d2
    new_states = states_d1 + new_states_d2
    new_initial_state = "q" + str(len(new_states))
    new_final_state = "q" + str(len(new_states) + 1)
    new_states.append(new_final_state)
    new_states.append(new_initial_state)
    new_transitions = {**transitions_d1, **transitions_d2}
    new_transitions[new_initial_state] = {}
    new_transitions[new_initial_state][""] = "{'" + initial_state_d1 + "','" + tmp[initial_state_d2] + "'}"
    if new_transitions[final_states_d1].get("", False):
        new_transitions[final_states_d1] = new_transitions[final_states_d1][:-1] + ",'" + new_final_state + "'}"
    else:
        new_transitions[final_states_d1][""] = "{'" + new_final_state + "'}"
    if new_transitions[tmp[final_states_d2]].get("", False):
        new_transitions[tmp[final_states_d2]] = new_transitions[tmp[final_states_d2]][:-1] + ",'" + new_final_state + "'}"
    else:
        new_transitions[tmp[final_states_d2]][""] = "{'" + new_final_state + "'}"
    new_transitions[new_final_state] = {}

    output_data = {}
    output_data['states'] = "{"
    for i in new_states:
        output_data['states'] += "'" + i + "',"
    output_data["states"] = output_data["states"][:-1] + "}"

    output_data['input_symbols'] = "{"
    for i in new_alphabet:
        output_data['input_symbols'] += "'" + i + "',"
    output_data["input_symbols"] = output_data["input_symbols"][:-1] + "}"

    output_data['transitions'] = new_transitions
    output_data['initial_state'] = new_initial_state
    output_data['final_states'] = "{'" + new_final_state + "'}"
    
    return output_data


def concatenation(data1: dict, data2: dict) -> dict:
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
    
    transitions_d2 = new_transitions_d2
    new_alphabet = alphabet_d1 + alphabet_d2
    new_states = states_d1 + new_states_d2
    new_final_state = "q" + str(len(new_states))
    new_states.append(new_final_state)
    new_transitions = {**transitions_d1, **transitions_d2}
    new_initial_state = initial_state_d1
    if new_transitions[final_states_d1].get("", False):
        new_transitions[final_states_d1] = new_transitions[final_states_d1][:-1] + ",'" + tmp[initial_state_d2] + "'}"
    else:
        new_transitions[final_states_d1][""] = "{'" + tmp[initial_state_d2] + "'}"
    if new_transitions[tmp[final_states_d2]].get("", False):
        new_transitions[tmp[final_states_d2]] = new_transitions[tmp[final_states_d2]][:-1] + ",'" + new_final_state + "'}"
    else:
        new_transitions[tmp[final_states_d2]][""] = "{'" + new_final_state + "'}"


    output_data = {}
    output_data['states'] = "{"
    for i in new_states:
        output_data['states'] += "'" + i + "',"
    output_data["states"] = output_data["states"][:-1] + "}"

    output_data['input_symbols'] = "{"
    for i in new_alphabet:
        output_data['input_symbols'] += "'" + i + "',"
    output_data["input_symbols"] = output_data["input_symbols"][:-1] + "}"

    output_data['transitions'] = new_transitions
    output_data['initial_state'] = new_initial_state
    output_data['final_states'] = "{'" + new_final_state + "'}"
    
    return output_data


def star(data: dict) -> dict:
    makeSingleFinalState(data)

    initial_state = data['initial_state']
    states = data['states'][2:-2].split("','")
    states.sort(key=lambda x: int(x[1:]))
    final_states = data['final_states'][2:-2]
    transitions = data['transitions'].copy()
    alphabet = data['input_symbols'][2:-2].split("','")

    new_initial_state = "q" + str(len(states))
    new_final_state = "q" + str(len(states) + 1)
    states.append(new_initial_state)
    states.append(new_final_state)
    transitions[new_initial_state] = {}
    transitions[new_initial_state][""] = "{'" + initial_state + "','" + new_final_state + "'}"
    transitions[new_final_state] = {}
    transitions[new_final_state][""] = "{'" + new_initial_state + "'}"
    if transitions[final_states].get("", False):
        transitions[final_states] = transitions[final_states][:-1] + ",'" + new_final_state + "'}"
    else:
        transitions[final_states][""] = "{'" + new_final_state + "'}"

    output_data = {}
    output_data['states'] = "{"
    for i in states:
        output_data['states'] += "'" + i + "',"
    output_data["states"] = output_data["states"][:-1] + "}"

    output_data['input_symbols'] = "{"
    for i in alphabet:
        output_data['input_symbols'] += "'" + i + "',"
    output_data["input_symbols"] = output_data["input_symbols"][:-1] + "}"

    output_data['transitions'] = transitions
    output_data['initial_state'] = new_initial_state
    output_data['final_states'] = "{'" + new_final_state + "'}"
    
    return output_data


def main():
    phase = input("""Enter the operation number:
    (1) Union
    (2) Concatenation
    (3) Star
>>>""")
    if phase == "1":
        path_d1 = input("Enter the path of the first json file: ")
        try:
            with open(f"{path_d1}", mode="r") as file:
                data1 = json.load(file)
        except:
            print("Invalid path!")
            return
        path_d2 = input("Enter the path of the second json file: ")
        try:
            with open(f"{path_d2}", mode="r") as file:
                data2 = json.load(file)
        except:
            print("Invalid path!")
            return
        output = union(data1, data2)
        output_path = input("Enter the output file path: ")
        json_object = json.dumps(output, indent=3)
 
        with open(f"{output_path}", mode="w") as file:
            file.write(json_object)

    elif phase == "2":
        path_d1 = input("Enter the path of the first json file: ")
        try:
            with open(f"{path_d1}", mode="r") as file:
                data1 = json.load(file)
        except:
            print("Invalid path!")
            return
        path_d2 = input("Enter the path of the second json file: ")
        try:
            with open(f"{path_d2}", mode="r") as file:
                data2 = json.load(file)
        except:
            print("Invalid path!")
            return
        output = concatenation(data1, data2)
        output_path = input("Enter the output file path: ")
        json_object = json.dumps(output, indent=3)
 
        with open(f"{output_path}", mode="w") as file:
            file.write(json_object)

    elif phase == "3":
        path = input("Enter the path of the json file: ")
        try:
            with open(f"{path}", mode="r") as file:
                data = json.load(file)
        except:
            print("Invalid path!")
            return
        output = star(data)
        output_path = input("Enter the output file path: ")
        json_object = json.dumps(output, indent=3)
 
        with open(f"{output_path}", mode="w") as file:
            file.write(json_object)

    else:
        print("Invalid input!")

if __name__ == "__main__":
    main()