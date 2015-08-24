import re, collections


def tokenizer(raw_str): # break raw (user) input to meaningful chunks
    pos = 0
    while pos < len(raw_str):
        if re.match(r'[+*/]', raw_str[pos]):
            yield ('OP', raw_str[pos])
        elif re.match(r'\w', raw_str[pos]):
            variable = raw_str[pos]
            var_pos = pos + 1
            while var_pos < len(raw_str) and re.match(r'[\w]', raw_str[var_pos]):
                variable += raw_str[var_pos]
                var_pos += 1
            pos = var_pos - 1
            yield ('VAR', variable)
        elif raw_str[pos] == ')':
            yield (')', raw_str[pos])
        elif raw_str[pos] == '(':
            yield ('(', raw_str[pos])
        else:
            print("Error: invalid character detected:", raw_str[pos])
            exit()
        pos += 1


def populateVectors(vect_tokens): # populate the variables with all T/F combinations
    dict = collections.OrderedDict()
    length = len(vect_tokens)
    for i in range(length):
        vect = []
        for j in range(2**i):
            vect += [False for num in range(2**(length-(i+1)))]
            vect += [True for num in range(2**(length-(i+1)))]
        dict[vect_tokens[i][1]] = vect #extract variable name and populate it
    return dict


def _cmp_prc(lhs,rhs): # compare precedence
    precedence = {'+' : 0 , '*' : 1, '/': 2}
    return precedence[lhs] - precedence[rhs]


def to_RPN(tokens): # convert using Shunting Yard algorithm to Reverse Polish notation
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


def _perform_op(op, *args): # execute the operation on each element of the vector
    if len(args) == 2: # binary operation
        vect1, vect2 = args
        assert len(vect1) == len(vect2)
        result = []
        for index in range(len(vect1)):
            result.append(op(vect1[index],vect2[index]))
        return result
    elif len(args) == 1: # unary operation
        vect = args[0]
        return [op(x) for x in vect]
    else: raise RuntimeError # invalid operation


def compute_tt(RPN_tokens,dict): # compute truth table result vector
    calc_stack = []
    for tokenType,tokenVal in RPN_tokens:
        if tokenType == 'OP':
            if not calc_stack: # validate unary operator
                print("Error: invalid placement of {0} operator".format(tokenVal))
                exit()
            if tokenVal == '/':
                vect = calc_stack.pop()
                negated_vect = _perform_op(lambda x: not x,vect)
                calc_stack.append(negated_vect)
                continue

            if len(calc_stack) < 2: # validate binary operator
                print("Error: invalid placement of {0} operator".format(tokenVal))
                exit()
            vect1, vect2 = calc_stack.pop(), calc_stack.pop()
            result = None
            if tokenVal == '+':
                result = _perform_op(lambda x,y: x or y,vect1,vect2)
            elif tokenVal == '*':
                result = _perform_op(lambda x,y: x and y,vect1,vect2)
            else: raise RuntimeError
            calc_stack.append(result)
            continue
        elif tokenType == 'VAR':
            calc_stack.append(dict[tokenVal])
        else: raise RuntimeError
    return calc_stack[-1]


def compute_vt(RPN_tokens,dict): # compute voltage table result vector
    vtDict = dict.copy() # voltage-table dict will have all active low negated
    for var_name, vect in dict.items(): # negate all the active low vectors
        if re.match(r'(.*)_L',var_name):
            vtDict[var_name] = _perform_op(lambda x: not x,vect)
    return compute_tt(RPN_tokens,vtDict)


def print_table(dict,result,t_val,f_val):
    for var_name in dict.keys():
        print(var_name,end='\t\t')
    else: print()
    for index in range(2**len(dict)):
        for vect in dict.values():
            print(t_val if vect[index] else f_val, end='\t\t')
        else: print(t_val if result[index] else f_val)


def main():
    tokens = [token for token in tokenizer(input("> "))]
    seen = set() # used for extracting unique variable names and preserving order
    variable_names = [x for x in tokens if not (x in seen or seen.add(x) or x[0] != 'VAR')]
    dict = populateVectors(variable_names)
    RPN_tokens = to_RPN(tokens)
    print("Truth Table:")
    tt_result = compute_tt(RPN_tokens,dict) # result vector for truth table
    print_table(dict,tt_result,'1','0')
    print()
    print("Voltage Table:")
    vt_result = compute_vt(RPN_tokens,dict) # result vector for truth table
    print_table(dict,vt_result,'H','L')

if __name__ == "__main__":
    main()
