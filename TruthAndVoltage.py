import re
import collections


def tokenizer(raw_str):
    pos = 0
    while pos < len(raw_str):
        if re.match(r'[+*/]', raw_str[pos]):
            yield ("OP", raw_str[pos])
        elif re.match(r'\w', raw_str[pos]):
            variable = raw_str[pos]
            var_pos = pos + 1
            while var_pos < len(raw_str) and re.match(r'[\w]', raw_str[var_pos]):
                variable += raw_str[var_pos]
                var_pos += 1
            pos = var_pos - 1
            yield ("VAR", variable)
        elif raw_str[pos] == ')':
            yield (')', raw_str[pos])
        elif raw_str[pos] == '(':
            yield ('(', raw_str[pos])
        else:
            print("Error: invalid character detected:", raw_str[pos])
            exit()
        pos += 1


def populateVectors(variable_names):
    dict = collections.OrderedDict()
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


def _cmp_prc(lhs,rhs): # compare precedence
    precedence = {'+' : 0 , '*' : 1, '/': 2}
    return precedence[lhs] - precedence[rhs]

def to_RPN(tokens):
    RPN_tokens = []
    opStack =[]
    for tokenType, tokenVal in tokens:
        if tokenType == "VAR":
            RPN_tokens.append((tokenType, tokenVal))
        elif tokenType == "OP":
            while len(opStack):
                topType, topVal = opStack[-1]
                if topType == '(' or topType == ')': break
                if tokenVal != '/' and _cmp_prc(tokenVal,topVal) <= 0:
                    RPN_tokens.append(opStack.pop())
                else: break
            opStack.append((tokenType, tokenVal))
        elif tokenType == '(':
            opStack.append((tokenType, tokenVal))
        elif tokenType == ')':
            while len(opStack):
                topType, topVal = opStack[-1]
                if topType == '(': break
                RPN_tokens.append(opStack.pop())
            try:
                topType, topVal = opStack[-1]
                if topType != '(': raise RuntimeError
            except RuntimeError:
                print("Error: mismatch(1) in parenthesis.")
                exit()
            opStack.pop()
    while len(opStack) > 0:
        topType, topVal = opStack[-1]
        if topType == ')' or topType == '(':
            print("Error: mismatch(2) in parenthesis.")
            exit()
        RPN_tokens.append(opStack.pop())
    return RPN_tokens


tokens = [token for token in tokenizer(input("> "))]
seen = set()
variable_names = [x for x in tokens if not (x in seen or seen.add(x) or x[0] != 'VAR')]
variable_vectors = populateVectors(variable_names)

for token in to_RPN(tokens):
    print(token[1], end=' ')
print()
