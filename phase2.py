import json

def DFA_Simplifier(data: dict) -> dict:

    states = sorted(data['states'][2:-2].split("','"))
    final_states = sorted(data['final_states'][2:-2].split("','"))
    transitions = data['transitions']
    alphabet = data['input_symbols'][2:-2].split("','")

    # creating graph and using BFS to remove non-reachable states
    n = len(states)
    s = 0
    adjList = [[] for x in range(n)]

    tmp_transitions = sorted(transitions.items())
    for i in range(len(tmp_transitions)):
        for j in tmp_transitions[i][1].values():
            number = int(j[1:])
            if number not in adjList[i] and number != i: 
                adjList[i].append(number)

    visited = [False for i in range(n)]
    queue = []
    queue.insert(0, (s, 0)) # The first member of the tuple is the number of the node and
    visited[s] = True       # the second member is the distance to the source
        
    while len(queue) > 0:
        theNode = queue.pop(-1)
        visited[theNode[0]] = True
        for i in adjList[theNode[0]]:
            if visited[i] == False:
                condition = True
                for j in queue:
                    if i == j[0]:
                        condition = False
                if condition:
                    queue.insert(0, (i, theNode[1] + 1))

    new_states = []
    for i in range(len(states)):
        if visited[i] == True:
            new_states.append(states[i])
    nonReachable_states = [x for x in states if x not in new_states]
    states = new_states

    # using partitioning algorithm to simplify the DFA
    partition = [[x for x in states if x not in final_states], final_states]
    flag = True
    while flag:
        try:
            if partition == copy_partitions:
                flag = False
        except:
            pass
        copy_partitions = partition[:]
        for part in copy_partitions:
            partitions_for_alphabets = {}
            for i in alphabet:
                    partitions_for_alphabets[i] = []
            if len(part) > 1:
                for i in alphabet:
                    tmp = {}
                    for state in part:
                        tmp[state] = transitions[state][i]
                    new_tmp = {}
                    for j in range(len(partition)):
                        new_tmp[j] = set()
                    for j in tmp.keys():
                        for k in range(len(partition)):
                            if tmp[j] in partition[k]:
                                new_tmp[k].add(j)
                                break
                    for j in new_tmp.values():
                        tmp_list = list(j)
                        tmp_list.sort()
                        partitions_for_alphabets[i].append(tmp_list)

                computation_table = [[[] for y in range(len(part))] for x in range(len(alphabet))]
                for i in range(len(alphabet)):
                    the_alphabet = alphabet[i]
                    for j in range(len(part)):
                        the_state = part[j]
                        for k in partitions_for_alphabets[the_alphabet]:
                            if the_state in k:
                                for l in k:
                                    if l != the_state:
                                        computation_table[i][j].append(l)
                                break
                new_patritions = [[] for x in range(len(part))]
                for i in range(len(part)):
                    new_patritions[i].append(part[i])
                for i in range(len(part)):
                    for j in range(len(alphabet)):
                        if j == 0:
                            new_patritions[i] += computation_table[j][i][:]
                        else:
                            for k in computation_table[j - 1][i]:
                                if k not in computation_table[j][i]:
                                    new_patritions[i].remove(k)

                new_patritions = [set(x) for x in new_patritions]
                final_partitions = []
                for i in new_patritions:
                    if i not in final_partitions:
                        final_partitions.append(i)
                final_partitions = [list(x) for x in final_partitions]
                # the_part = part
                partition.remove(part)
                for i in final_partitions:
                    partition.append(i)

    new_states = []
    converted_dict = {}
    new_final_states = []
    for i in range(len(partition)):
        new_states.append(f"q{i}")
    for i in range(len(partition)):
        for j in partition[i]:
            converted_dict[j] = new_states[i]
    for i in final_states:
        if converted_dict[i] not in new_final_states:
            new_final_states.append(converted_dict[i])
    new_data = {}
    # "states": "{'q0','q1','q2','q3','q4','q5'}"
    new_states_string = "{"
    for i in new_states:
        new_states_string += f"'{i}',"
    new_states_string = new_states_string[:-1] + "}"
    new_data["states"] = new_states_string
    new_data["input_symbols"] = data['input_symbols']
    new_transition = {}
    for key in transitions.keys():
        if key not in nonReachable_states:
            new_transition[converted_dict[key]] = transitions[key]
            for i in new_transition[converted_dict[key]].keys():
                new_transition[converted_dict[key]][i] = converted_dict[transitions[key][i]]
    new_data["transitions"] = new_transition
    new_data["initial_state"] = converted_dict[data['initial_state']]
    new_final_states_string = "{"
    for i in new_final_states:
        new_final_states_string += f"'{i}',"
    new_final_states_string = new_final_states_string[:-1] + "}"
    new_data["final_states"] = new_final_states_string

    for i in range(len(partition)):
        print(f"q{i} --> {partition[i]}") 

    return new_data


def main():
    path = input("Enter the path of the json file: ")
    try:
        with open(f"{path}", mode="r") as file:
            data = json.load(file)
    except:
        print("Invalid path!")
        return
    output = DFA_Simplifier(data)
    output_path = input("Enter the output file path: ")
    json_object = json.dumps(output, indent=3)

    with open(f"{output_path}", mode="w") as file:
        file.write(json_object)

if __name__ == "__main__":
    main()