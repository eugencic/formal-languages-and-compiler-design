import re as regexp
import networkx as nx
import matplotlib.pyplot as plt
import pylab

grammar = """
VN={S, A, B, D},
VT={a, b},
P={
1. S -> aA
2. A -> bS
3. A -> aB
4. B -> bC
5. C -> aA
6. C -> b
}"""


def parse_string(input_str):
    str = input_str.split()
    str = "".join(str).split("P={")[1]
    if str[-1] == '}':
        str = str[:-1]
    str = regexp.split("[0-9]+\.", str)
    return list(filter(len, str))


P = parse_string(grammar)
# print(P)
# ['S->aA', 'A->bS', 'A->aB', 'B->bC', 'C->aA', 'C->b']

# Defining states
states = {}
for key in P:
    temp_split = key.split("->")
    curr_graph = temp_split[0]
    point_to = temp_split[1]
    empty_symbol = "$"
    if curr_graph not in states.keys():
        states[curr_graph] = []
    if len(point_to) < 2:
        point_to = point_to + empty_symbol
        states[curr_graph].append([point_to[0], point_to[1]])
    else:
        states[curr_graph].append([point_to[0], point_to[1]])

# print(states)
# {'S': [['a', 'A']], 'A': [['b', 'S'], ['a', 'B']], 'B': [['b', 'C']], 'C': [['a', 'A'], ['b', '$']]}


def verify(source_state, j):
    # a - source state input, b - accepted state
    for a, b in source_state:
        # Compares one input symbol with existing inputs in state
        if char_list[j] == a:
            # verify if the last input symbol coincides with terminal state
            if b == '$' and j == (len(char_list) - 1):
                print("Valid word")
                exit()
            else:
                # verifies the next input symbol in the next state
                return verify(states[b], j + 1)
    print("Not valid input")


def draw_graph():
    graph = nx.DiGraph()
    graph.add_edges_from([('q0', 'q1'), ('q1', 'q0'), ('q1', 'q2'), ('q2', 'q3'), ('q3', 'q1'), ('q3', '$')])
    val_map = {'q0': 1, '$': 2}
    values = [val_map.get(node, 3) for node in graph.nodes()]
    back_edge = [('q1', 'q0')]
    edge_colors = ['black' if not edge in back_edge else 'red' for edge in graph.edges()]
    pos = nx.spring_layout(graph)
    nx.draw_networkx_labels(graph, pos)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=dict([
        (('q0', 'q1'), 'a'), (('q1', 'q0'), 'b'), (('q1', 'q2'), 'a'),
        (('q2', 'q3'), 'b'), (('q3', 'q1'), 'a'), (('q3', '$'), 'b')]))
    nx.draw_networkx_edges(graph, pos, arrows=True, connectionstyle="arc3,rad=0.3")
    nx.draw(graph, pos, node_color=values, node_size=1500, edge_color=edge_colors,
            edge_cmap=plt.cm.Reds, connectionstyle="arc3,rad=0.3")
    plt.title(label='FA')
    plt.show()


draw_graph()
word = input("Type a word to be checked:\n")
char_list = list(word)
verify(states['S'], 0)
