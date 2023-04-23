import json

with open("samples/phase2-sample/in/input1.json", mode="r") as file:
    data = json.load(file)

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
        number = int(j[-1])
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
        for i in final_partitions:
            if set(i) == set(the_part):
                flag = False
    except:
        pass
    try:
        partition.remove(the_part)
        for i in final_partitions:
            partition.append(i)
    except:
        pass
    for part in partition:
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
                    partitions_for_alphabets[i].append(list(j))

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
            the_part = part

