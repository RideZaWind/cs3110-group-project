from collections import defaultdict

def decimal_integer_checker(string:str) -> bool:
    start_state = "start"
    
    transitions = defaultdict(lambda: "")
    transitions.update({("start", str(i)): "decimal digit" for i in range(1, 10)})
    transitions.update({("decimal digit", str(i)): "decimal digit" for i in range(0, 10)})
    transitions.update({("decimal underscore", str(i)): "decimal digit" for i in range(0, 10)})
    transitions.update({
        ("start", "0"): "zero",
        ("zero", "0"): "zero",
        ("decimal digit", "_"): "decimal underscore",
        ("zero", "_"): "zero underscore",
        ("zero underscore", "0"): "zero",
        })
    
    accepting_states = {"zero", "decimal digit"}
    
    current_states = {start_state}
    
    for char in string:
        current_states = {transitions[(state, char)] for state in current_states}
    
    return(len(current_states.intersection(accepting_states)) > 0)


test_strings = ["0_000", "54000", "003", "89583_482"]
for test in test_strings:
    print(decimal_integer_checker(test))