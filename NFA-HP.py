# Adjacency list implementation

from collections import defaultdict

class NFA:
    def __init__(self):
        self.transitions = defaultdict(lambda: defaultdict(set)) #default to creating another defaultdict with set when missing key is accessed
        # I'll make these different with _ instead of my typical camelcase because they ARE special
        self.start_state = None
        self.accept_states = set()

    # every time transition is accessed with non-existant key, it will now automatically make one
    def add_transition(self, fromState, symbol, toState):
        self.transitions[fromState][str(symbol)].add(toState)

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
nfa.set_start_state(0)

# Adding transitions
for i in range(9): # 0 to 8
    nfa.add_transition(0, i + 1, 1)

for i in range(10): # 0 to 9
    nfa.add_transition(1, i, 1)
    nfa.add_transition(2, i, 1)

nfa.add_transition(1, "_", 2)
nfa.add_transition(0, 0, 3)
nfa.add_transition(3, 0, 3)

# Set accept state(s)
nfa.set_accept_state(1)
nfa.set_accept_state(2)
nfa.set_accept_state(3)

# Test strings
test_strings = ["42", "0", "123", "1_000", "0123"]
for s in test_strings:
    result = "Accepted" if nfa.is_accepted(s) else "Rejected"
    print(f"String '{s}': {result}")