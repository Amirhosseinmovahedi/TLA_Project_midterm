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

