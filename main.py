def is_opcode(token: str):
    return token in ['+', '-', "*", "/"]


def is_operand(token: str):
    return token in list("qwertyuiopasdfghjklzxcvbnm")


def is_bracket(token: str):
    return token in ["(", ")"]


def token_type(token):
    if is_opcode(token):
        return 'opcode'
    elif is_bracket(token):
        return token
    else:
        return 'operand'


def tokenizer(expr: str):
    """简单预处理输入表达式，简单检查表达式是否合法"""
    expr = expr.replace(' ', '')
    # simple tokenizer
    tokens = list(expr)
    # sanitizer
    last_token_type = None
    bracket_pair = 0
    for i in tokens:
        if not is_bracket(last_token_type) and last_token_type == token_type(i):
            return False
        last_token_type = token_type(i)
        if i == "(":
            bracket_pair += 1
        if i == ")":
            bracket_pair -= 1
        if bracket_pair < 0:
            return False
    if bracket_pair > 0:
        return False

    return tokens


def prior_than(token1, token2):
    """判断是否token1比token2优先"""
    return token1 in ["*", "/"] and token2 in ["+", "-"]


def infix_to_prefix(tokens: list[str]):
    tokens.reverse()
    opcode_stack = []  # 符号栈
    operand_stack = []  # 操作数栈
    for i in tokens:
        if is_operand(i):
            operand_stack.append(i)
        elif is_opcode(i):
            # 如果符号栈有token且优先级比当前token高
            if len(opcode_stack) > 0 and prior_than(opcode_stack[-1], i):
                t = opcode_stack.pop()
                operand_stack.append(t)
                opcode_stack.append(i)
            else:
                opcode_stack.append(i)
        elif i == "(":
            t = opcode_stack.pop()
            while t != ")":
                operand_stack.append(t)
                t = opcode_stack.pop()
        elif i == ")":
            opcode_stack.append(i)

    while len(opcode_stack) > 0:
        t = opcode_stack.pop()
        operand_stack.append(t)
    operand_stack.reverse()
    return operand_stack


if __name__ == '__main__':
    expression = input("> ")
    tok = tokenizer(expression)
    if tok is False:
        print("Invalid expression format.")
        exit(1)
    else:
        print(infix_to_prefix(tok))
