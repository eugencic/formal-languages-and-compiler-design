import networkx as nx
import matplotlib.pyplot as plt

lines = open("Variant19.txt", "r").read().split('\n')
inputs = list(lines[0].split(","))
states = list(lines[1].split(","))
start_state = lines[2]
transitions = []
NFA = {}
DFA = {}

for i in range(4, len(lines)):
    transition_line = lines[i].split(" ")
    starting_state = transition_line[0]
    transition_symbol = transition_line[1]
    ending_state = transition_line[2]
    transition = [starting_state, transition_symbol, ending_state]
    transitions.append(transition)

# print(inputs)
# print(states)
# print(transitions)

for transition in transitions:
    if transition[0] not in NFA.keys():
        NFA[transition[0]] = []
    NFA[transition[0]].append([transition[1], transition[2]])

print("NFA: ")
print(NFA)
print('\n')


# {'q0': [['a', 'q1'], ['a', 'q0'], ['b', 'q0']], 'q1': [['b', 'q2'], ['b', 'q1']],
# 'q2': [['b', 'q2']]}


def print_table1():
    print("{:<10}".format('States'), end=' ')
    for input in inputs:
        print("{:<10}".format(input), end=' ')
    for state in states:
        print("\n{:<10}".format(state), end=' ')
        if state in NFA.keys():
            for input in inputs:
                output = ''
                for transition in NFA[state]:
                    if input == transition[0]:
                        output += transition[1]
                print("{:<10}".format(output), end=' ')
    print('\n')


print_table1()

DFA_with_excluded = dict(NFA)
not_excluded = [start_state]


def exclude(state):
    if state in NFA.keys():
        for input in inputs:
            nr_of_equal_inputs = 0
            next_state = ''
            for transition in NFA[state]:
                if input == transition[0]:
                    nr_of_equal_inputs += 1
                    next_state += transition[1]
            if nr_of_equal_inputs == 1:
                if next_state not in not_excluded:
                    not_excluded.append(next_state)
                    exclude(next_state)


exclude(start_state)

excluded = []

for state in states:
    if state not in not_excluded:
        excluded.append(state)
print("Excluded: ")
print(excluded)
print('\n')


# Function that checks for state duplication
def contains_all(keys, new_key):
    contains = False
    for k in keys:
        if ''.join(sorted(k)) == ''.join(sorted(new_key)):
            contains = True
    return contains


def conversion():
    for state in states:
        if state not in excluded:
            if state in NFA.keys():
                # Check for all inputs
                for input in inputs:
                    nr_of_equal_inputs = 0
                    new_state = ''
                    new_destinations = []
                    # Check all transitions of a state
                    for transition in NFA[state]:
                        # Check if the iterative input coincides with some input from the transition
                        if input == transition[0]:
                            nr_of_equal_inputs += 1
                            # Get the name of new state
                            new_state += transition[1]
                            # Get the new state's destinations
                            new_destinations.append(transition[1])
                    # If there are 2 or more equal inputs present
                    if nr_of_equal_inputs > 1:
                        # Check if the state is already present in the table
                        if not contains_all(NFA.keys(), new_state):
                            NFA[new_state] = []
                            for destination in new_destinations:
                                for transition in NFA[destination]:
                                    # Exclude duplicate transitions
                                    if transition not in NFA[new_state]:
                                        NFA[new_state].append(transition)
                            states.append(new_state)
                        elif contains_all(NFA.keys(), new_state):
                            pass


def conversion_with_excluded():
    for state in states:
        if state in DFA_with_excluded.keys():
            # Check for all inputs
            for input in inputs:
                nr_of_equal_inputs = 0
                new_state = ''
                new_destinations = []
                # Check all transitions of a state
                for transition in DFA_with_excluded[state]:
                    # Check if the iterative input coincides with some input from the transition
                    if input == transition[0]:
                        nr_of_equal_inputs += 1
                        # Get the name of new state
                        new_state += transition[1]
                        # Get the new state's destinations
                        new_destinations.append(transition[1])
                # If there are 2 or more equal inputs present
                if nr_of_equal_inputs > 1:
                    # Check if the state is already present in the table
                    if not contains_all(DFA_with_excluded.keys(), new_state):
                        DFA_with_excluded[new_state] = []
                        for destination in new_destinations:
                            for transition in DFA_with_excluded[destination]:
                                # Exclude duplicate transitions
                                if transition not in DFA_with_excluded[new_state]:
                                    DFA_with_excluded[new_state].append(transition)
                        states.append(new_state)
                    elif contains_all(DFA_with_excluded.keys(), new_state):
                        pass


conversion()


conversion_with_excluded()

# print(NFA)
# print(DFA_with_excluded)

for state in excluded:
    if state in NFA.keys():
        NFA.pop(state)


# print(NFA)


def include():
    for state in states:
        if state in NFA.keys():
            for input in inputs:
                nr_of_equal_inputs = 0
                new_state = ''
                for transition in NFA[state]:
                    if input == transition[0]:
                        nr_of_equal_inputs += 1
                        new_state += transition[1]
                if nr_of_equal_inputs == 1:
                    if not contains_all(NFA.keys(), new_state):
                        if new_state in DFA_with_excluded.keys():
                            NFA[new_state] = DFA_with_excluded[new_state]
                        elif new_state not in DFA_with_excluded.keys():
                            NFA[new_state] = []
                        states.append(new_state)
                if nr_of_equal_inputs > 1:
                    if not contains_all(NFA.keys(), new_state):
                        if new_state in DFA_with_excluded.keys():
                            NFA[new_state] = DFA_with_excluded[new_state]
                        elif new_state not in DFA_with_excluded.keys():
                            NFA[new_state] = []
                        states.append(new_state)


include()


# print(NFA)


def combination():
    global list_of_transitions
    for state in states:
        if state not in excluded:
            if state in NFA.keys():
                for input in inputs:
                    list_of_transitions = []
                    nr_of_inputs = 0
                    for transition in NFA[state]:
                        if input == transition[0]:
                            nr_of_inputs += 1
                            list_of_transitions.append(transition[1])
                    if nr_of_inputs > 0:
                        new_transition = ''.join(list_of_transitions)
                        dfa_list = [input, new_transition]
                        if state not in DFA.keys():
                            DFA[state] = []
                            DFA[state].append(dfa_list)
                        else:
                            DFA[state].append(dfa_list)


combination()

print("DFA: ")
print(DFA)
print('\n')


def print_table2():
    print("{:<10}".format('States'), end=' ')
    for input in inputs:
        print("{:<10}".format(input), end=' ')
    for state in NFA.keys():
        print("\n{:<10}".format(state), end=' ')
        if state in NFA.keys():
            for input in inputs:
                output = ''
                for transition in NFA[state]:
                    if input == transition[0]:
                        output += transition[1]
                print("{:<10}".format(output), end=' ')


print_table2()
