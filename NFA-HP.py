# Adjacency list implementation

from collections import defaultdict
import string

class NFA:
    def __init__(self):
        self.transitions = defaultdict(lambda: defaultdict(set)) #default to creating another defaultdict with set when missing key is accessed
        # I'll make these different with _ instead of my typical camelcase because they ARE special
        self.start_state = None
        self.accept_states = set()

    # every time transition is accessed with non-existant key, it will now automatically make one
    def add_transition(self, fromState, symbol, toState):
        self.transitions[fromState][str(symbol)].add(toState) # we must convert the symbol to string because numbers don't work

    def set_start_state(self, state):
        self.start_state = state

    def set_accept_state(self,state):
        self.accept_states.add(state)

    # we must also make sure to take in account of states reachable by epsilon ε
    # we don't need the epsilon nodes, those are bullshit, give me the next meaniful node so I can check the symbol with.
    # return the current states after traversing through all available epsilons
    def epsilon_traversal(self, states):
        stack = list(states) # why list? at some point we will call this with a number of current arguments (imagine traversing each line of a tree)
        closure = set(states) # backing up the current list

        while stack:
            currentState = stack.pop()
            for nextState in self.transitions[currentState].get(None, []): # None represents empty move
                if nextState not in closure:
                    closure.add(nextState)
                    stack.append(nextState) # why are we appending them back when we're popping them off? We're doing DFS, and we're skipping through all the epsilon transitions

        return closure

    def is_accepted(self, inputString):
        # check for epsilon states of the starting state
        currentStates = self.epsilon_traversal({self.start_state}) # why curly bracket? We're passing set. If we pass per say, 0, instead of {0}, it might cause iteration issues

        for symbol in inputString: # symbol is the right way to say character in this case
            nextStates = set()
            for state in currentStates:
                if symbol in self.transitions[state]: # check the state, see if the symbol is in there
                    nextStates.update(self.transitions[state][symbol])

            # once we figure out the next states, check for all epsilon traversal
            currentStates = self.epsilon_traversal(nextStates)

        # if any of the current state meets the accept state, then it is accepted, return true
        # bool will check if the set is empty or not. the & operation will return a set with intersection between the two sets
        return bool(currentStates & self.accept_states)





# MAIN
nfa = NFA()
nfa.set_start_state("start")

# Adding transitions
# Decimals
for i in range(9): # 0 to 8
    nfa.add_transition("start", i + 1, "dec")

nfa.add_transition("dec", "_", "_")

for i in range(10): # 0 to 9
    nfa.add_transition("dec", i, "dec")
    nfa.add_transition("_", i, "dec")

# Octals/Hex/Zeroes
nfa.add_transition("start", 0, "0")

# Octals
nfa.add_transition("0", "o", "oct")

for i in range(8): # 0 to 7
    nfa.add_transition("oct", i, "digit")
    nfa.add_transition("digit", i, "digit")
    nfa.add_transition("digit", i, "_")
    nfa.add_transition("_", i, "digit")

nfa.add_transition("oct", "_", "_")
nfa.add_transition("digit", "_", "_")

#Hexadecimals
nfa.add_transition("0", "x", "hex")

for i in range(10): # 0 to 9
    nfa.add_transition("hex", i, "digit")
    nfa.add_transition("digit", i, "digit")
    nfa.add_transition("_", i, "digit")

for char in string.ascii_lowercase:  # Contains "abcdefghijklmnopqrstuvwxyz"
    nfa.add_transition("hex", char, "digit")
    nfa.add_transition("digit", char, "digit")
    nfa.add_transition("_", char, "digit")

for char in string.ascii_uppercase:  # Contains "ABDEFGHIJKLMNOPQRSTUVWXYZ"
    nfa.add_transition("hex", char, "digit")
    nfa.add_transition("digit", char, "digit")
    nfa.add_transition("_", char, "digit")

nfa.add_transition("hex", "_", "_")
nfa.add_transition("digit", "_", "_")

# Zeroes
nfa.add_transition("0", 0, "00")
nfa.add_transition("00", 0, "00")

# Set accept state(s)
nfa.set_accept_state("dec")
nfa.set_accept_state("digit")
nfa.set_accept_state("00")
nfa.set_accept_state("0")

# Test strings
test_strings = ["123", "0", "0x123ABC", "0o013", "0x1_2_3", "0o7_7_7", "00000", "Supercalifragilisticexpialidocious"]
for s in test_strings:
    result = "Accepted" if nfa.is_accepted(s) else "Rejected"
    print(f"String '{s}': {result}")