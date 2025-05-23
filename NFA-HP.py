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
    # we don't need the epsilon nodes, give me the next meaniful node so I can check the symbol with.
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


def buildNFA():
    userNFA = NFA()

    userNFA.set_start_state("start")
    print("Start state is set to \'start\'")
    while True:
        userInput = input("Input an NFA node separated by space, ie \"0 x hex\", otherwise 'end' to stop building:\n")

        if userInput == "end":
            while True:
                userInput = input("Set an accept state, 'end' to stop: ")
                userNFA.set_accept_state(userInput)

                if userInput == "end":
                    # I should make an NFA tree print function at some point
                    while True:
                        String = input("Input a test string, 'end' to stop: ")

                        if String == "end":
                            print("Testing complete.")
                            exit()  # Exit the program

                        result = "Accepted" if userNFA.is_accepted(String) else "Rejected"
                        print(f"String '{String}': {result}")

        parts = userInput.split()

        if len(parts) != 3: # vanguard to make sure there's 3 inputs
            print("Error: Please provide exactly 3 values separated by spaces.")
            continue

        userNFA.add_transition(parts[0], parts[1], parts[2])
        print(f"Added transition: {parts[0]} --{parts[1]}--> {parts[2]}")


# MAIN
nfa = NFA()
nfa.set_start_state("start")

# Adding transitions
# Decimals
for i in range(9): # 0 to 8
    nfa.add_transition("start", i + 1, "dec")

nfa.add_transition("dec", "_", "_dec")

for i in range(10): # 0 to 9
    nfa.add_transition("dec", i, "dec")
    nfa.add_transition("_dec", i, "dec")

# Octals/Hex/Zeroes
nfa.add_transition("start", 0, "0")

# Octals
nfa.add_transition("0", "o", "oct")
nfa.add_transition("0", "O", "oct")

for i in range(8): # 0 to 7
    nfa.add_transition("oct", i, "digitOct")
    nfa.add_transition("digitOct", i, "digitOct")
    nfa.add_transition("digitOct", i, "_oct")
    nfa.add_transition("_oct", i, "digitOct")

nfa.add_transition("oct", "_", "_oct")
nfa.add_transition("digitOct", "_", "_oct")

#Hexadecimals
nfa.add_transition("0", "x", "hex")
nfa.add_transition("0", "X", "hex")

for i in range(10): # 0 to 9
    nfa.add_transition("hex", i, "digitHex")
    nfa.add_transition("digitHex", i, "digitHex")
    nfa.add_transition("_hex", i, "digitHex")

for char in string.ascii_lowercase[:6]:  # "abcdef"
    nfa.add_transition("hex", char, "digitHex")
    nfa.add_transition("digitHex", char, "digitHex")
    nfa.add_transition("_hex", char, "digitHex")

for char in string.ascii_uppercase[:6]:  # "ABCDEF"
    nfa.add_transition("hex", char, "digitHex")
    nfa.add_transition("digitHex", char, "digitHex")
    nfa.add_transition("_hex", char, "digitHex")

nfa.add_transition("hex", "_", "_hex")
nfa.add_transition("digitHex", "_", "_hex")

# Zeroes
nfa.add_transition("0", 0, "00")
nfa.add_transition("00", 0, "00")
nfa.add_transition("0", "_", "_00")
nfa.add_transition("00", "_", "_00")
nfa.add_transition("_00", 0, "00")

# Set accept state(s)
nfa.set_accept_state("dec")
nfa.set_accept_state("digitHex")
nfa.set_accept_state("digitOct")
nfa.set_accept_state("00")
nfa.set_accept_state("0")

#Floting point extra credit:

# All transitions for Digits 0-9
for i in range(10):
    nfa.add_transition("start", i, "DigitBefore")
    nfa.add_transition("DigitBefore", i, "DigitBefore")
    nfa.add_transition("DecimalPoint", i, "DigitAfter")
    nfa.add_transition("DigitAfter", i, "DigitAfter")
    nfa.add_transition("UnderscoreAfter", i, "DigitAfter")
    nfa.add_transition("e/E", i, "ExponentDigits")
    nfa.add_transition("+/- after e/E", i, "ExponentDigits")
    nfa.add_transition("ExponentDigits", i, "ExponentDigits")
    nfa.add_transition("UnderscoreBefore", i, "DigitBefore")
    nfa.add_transition("UnderscoreExponent", i, "ExponentDigits")

# Edge case: Valid integer ending with a decimal
nfa.add_transition("DigitBefore", ".", "EdgeCase")
nfa.add_transition("EdgeCase", "e", "e/E")
nfa.add_transition("EdgeCase", "E", "e/E")

# Other decimal point and underscore transitions
nfa.add_transition("start", ".", "DecimalPoint")
nfa.add_transition("DigitBefore", ".", "DecimalPoint")
nfa.add_transition("DigitAfter", "_", "UnderscoreAfter")
nfa.add_transition("DigitBefore", "_", "UnderscoreBefore")
nfa.add_transition("ExponentDigits", "_", "UnderscoreExponent")


# Transtitions for exponent part (e/E)
nfa.add_transition("DigitBefore", "e", "e/E")
nfa.add_transition("DigitBefore", "E", "e/E")
nfa.add_transition("DigitAfter", "e", "e/E")
nfa.add_transition("DigitAfter", "E", "e/E")

# Sign after exponent
nfa.add_transition("e/E", "+", "+/- after e/E")
nfa.add_transition("e/E", "-", "+/- after e/E")


# Set accept states
nfa.set_accept_state("DigitAfter")
nfa.set_accept_state("ExponentDigits")
nfa.set_accept_state("EdgeCase")

########## DRIVER ###########

# Interface
userInput = input("Welcome to the NFA program. Type y if you're reading from a file: ")

if userInput == 'y':
    inFile  = input("Type the input file name: ")
    outFile = input("Type the output file name: ")

    with open(inFile, "r") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]

    with open(outFile, "w") as outfile:
        i = 0
        while i < len(lines):
            # Skip comment lines and blank lines
            if lines[i].startswith('#') or lines[i] == '':
                i += 1
                continue

            if i < len(lines):
                # The first line is our test string
                testString = lines[i]
                i += 1

                # Next line should be the expected result
                expectedResult = lines[i] if i < len(lines) else None
                i += 1

                # Run the NFA on the test string
                actualResult = "accepted" if nfa.is_accepted(testString) else "rejected"

                # Store the output to print on both terminal and file
                output = f"String: {testString}\nExpected: {expectedResult}\nActual: {actualResult}\n\n"

                # Print
                print(output)
                outfile.write(output)
else:
    userInput = input("Type y if you want to use the defined NFA, otherwise build your own: ")

    if userInput == 'y':
        while True:
            String = input("Input a test string, 'end' to stop: ")

            if String == "end":
                print("Testing complete.")
                exit()  # Exit the program
            result = "Accepted" if nfa.is_accepted(String) else "Rejected"
            print(f"String '{String}': {result}")
    else:
        buildNFA()
