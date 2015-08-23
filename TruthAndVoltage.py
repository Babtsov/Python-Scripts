import re
import pprint

OP = 'OP'       # operator
VAR = 'VAR'     # variable
L_PAR = "L_PAR" # left parenthesis
R_PAR = "R_PAR" # right parenthesis


def tokenizer(raw_str):
    pos = 0
    while pos < len(raw_str):
        if re.match(r'[+*/]', raw_str[pos]):
            yield (OP, raw_str[pos])
        elif re.match(r'\w', raw_str[pos]):
            variable = raw_str[pos]
            var_pos = pos + 1
            while var_pos < len(raw_str) and re.match(r'[\w]', raw_str[var_pos]):
                variable += raw_str[var_pos]
                var_pos += 1
            pos = var_pos - 1
            yield (VAR, variable)
        elif raw_str[pos] == ')':
            yield (R_PAR, raw_str[pos])
        elif raw_str[pos] == '(':
            yield (L_PAR, raw_str[pos])
        else:
            print("Error: invalid token detected: ",raw_str[pos])
            exit()
        pos += 1


def populateVectors(variable_names):
    dict = {}
    length = len(variable_names)
    for i in range(length):
        vect = []
        for j in range(2**i):
            vect += [0 for num in range(2**(length-(i+1)))]
            vect += [1 for num in range(2**(length-(i+1)))]
        dict[variable_names[i]] = vect
    return dict


def perform_operation(op, *args):
    result = []
    if len(args) == 2: # binary operation
        vect1, vect2 = args
        assert len(vect1) == len(vect2)
        for index in range(len(vect1)):
            result.append(op(vect1[index],vect2[index]))
    elif len(args) == 1: # unary operation
        vect = args[0]
        for index in range(len(vect)):
            result.append(op(vect[index]))
    else: #invalid operation
        raise RuntimeError
    return result

tokens = [token for token in tokenizer(input("> "))]
variable_names = {token[1] for token in tokens if token[0] == VAR}
variable_vectors = populateVectors(list(variable_names))
print(tokens)
print(variable_names)
pprint.pprint(variable_vectors)
