from sys import argv
import re
import token_class
import syntax_analyzer as sa

# check the syntax.
code_token = sa.sa(argv[1])

# define funcList as dictionary
# which has fuction name as a "key"
# and List of its values as a "value"
funcList = {}
stack = []
call_sequence = []

# define variables for the funcList parsing
isOuter = True
isFirst = True
componentsList = []
currentFunc = ""
components = ""

for index, token in code_token:
    
    # the given code_token is sytactically guaranteed.
    # parse the token into funcionList.


    if index == token_class.IDENT and isOuter:
        currentFunc = token
        continue

    elif index == token_class.PAREN_LEFT:
        isOuter = False
        
    elif index == token_class.COMMA:
        continue

    elif index == token_class.SEMICOLON:
        componentsList.append(components)
        components = ""
        isFirst = True
        continue

    elif index != token_class.PAREN_RIGHT:
        components += ("" if isFirst else " ") + token
        isFirst = False
        continue
    
    elif index == token_class.PAREN_RIGHT:
        funcList[currentFunc] = componentsList
        currentFunc = ""
        components = ""
        componentsList = []
        isOuter = True
        continue

#print(funcList)

# if it does not have main function, raise exception.
if 'main' not in funcList.keys():
    raise Exception("No starting function.")


def doFunc(name: str, caller=None, lineNumber=None):

    global funcList
    global stack
    global call_sequence

    #remember its stack number.
    stackNumber = 0  
    
    # i : i-th iteration
    # compoenents: the components in the funcList's corresponing index
    for i, components in enumerate(funcList[name]):

        # split the component into tokens ith whitespaces.
        tokens = components.split(' ')

        # when it is variable, add to stack
        if tokens[0] == 'variable':

            # distinguish with whitespaces.
            variables = [i.rstrip() for i in tokens[1:]]

            # if the identifier name is same as the function name,
            # raise exception.
            # check if variables are in functions.
            # any: python internal function
            # checks if the given iterable object is in the given parameter.
            checkVarIsSameAsFunc = any(variable in variables for variable in funcList.keys())

            if checkVarIsSameAsFunc:
                raise Exception(
                    # & works as intersection in sets.
                    f"Duplicate declaration of the identifier or the function name: {list(set(variables) & set(funcList.keys()))}")

            # if the identifier name apprears again in the given function,
            # raise exception.
            # check by set length.
            checkVarIsAtomic = (len(set(variables)) != len(variables))

            if checkVarIsAtomic:
                # count all variables
                # the key is variable name.
                # the value is the counted number of the variable.
                count_var = {i: variables.count(i) for i in variables}

                # if the given variable is counted more than 1,
                # remove the variable in the variables list.
                val = [x for x in count_var if count_var[x] != 1]
                print(f"Duplicate declaration of the identifier: {val}")

                # i is the key (identifier name) of the repeated identifier.
                # remove the var for one time.
                for repeated_identifier in val:
                    variables.remove(repeated_identifier)

            # concatenate indicating string
            localVariables = ["Local variable: " + variable for variable in variables]
            
            if name == 'main':
                stack.append(localVariables)
                
            else:
                returnAddress = f"{caller}: {i + 1}"
                dynamicLink = str(len(sum(stack[0:-1], [])))
                stack.append(
                    ["Return address: " + str(returnAddress), "Dynamic Link: " + str(dynamicLink)] + localVariables)
            stackNumber = len(stack) - 1

        elif tokens[0] == 'call':

            # if function name is not in the funcList,
            # raise exception.
            if tokens[1] not in funcList.keys():
                raise Exception(f"Call to undefined function: {tokens[1]}")

            # append the call sequence
            call_sequence.append(tokens[1])
            call_sequence.append(name)
            # recursively call the function.    
            # tokens[1]: give name as caller name.
            # name : the caller is current name
            # i : to be processed line number.
            doFunc(tokens[1], name, i)

        elif tokens[0] == 'print_ari':

            # traverse call_sequence and print the results.
            func_cnt = len(list(funcList.keys()))
            func_name_index = 0
            for stack_index, component in enumerate(reversed(stack)):
                for token_index, token in enumerate(reversed(component)):
                    if token_index == 0:
                        print(f"{call_sequence[func_name_index]}:{token}")
                    else:
                        print(f"{' ' * len(call_sequence[func_name_index])} {token}")
                func_name_index += 1
            print("")

        else:
            link_cnt = 0
            local_offset = 0
            for j_index, j in enumerate(reversed(stack[0:stackNumber + 1])):
                if f"Local variable: {tokens[0]}" in j:
                    link_cnt = j_index
                    local_offset = j.index(f"Local variable: {tokens[0]}")
                    break

            print(f"{name}: {tokens[0]} => {link_cnt}, {local_offset}\n")

# always start from main.
doFunc('main')
