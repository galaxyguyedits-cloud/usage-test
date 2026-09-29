"""Stack and classic stack applications.

A LIFO stack backed by a Python list, used for balanced-bracket
checking, evaluating Reverse Polish Notation, converting infix to
postfix (shunting-yard), and a min-stack with O(1) minimum queries.
All stack operations are O(1) amortised.
"""


class Stack:
    def __init__(self):
        self._items = []

    def push(self, x):
        self._items.append(x)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        return self._items[-1] if self._items else None

    def __len__(self):
        return len(self._items)


class MinStack(Stack):
    """Stack that also tracks the current minimum in O(1)."""

    def __init__(self):
        super().__init__()
        self._mins = []

    def push(self, x):
        super().push(x)
        self._mins.append(x if not self._mins else min(x, self._mins[-1]))

    def pop(self):
        self._mins.pop()
        return super().pop()

    def min(self):
        return self._mins[-1]


def balanced(expr):
    pairs = {")": "(", "]": "[", "}": "{"}
    s = Stack()
    for ch in expr:
        if ch in "([{":
            s.push(ch)
        elif ch in pairs:
            if s.peek() != pairs[ch]:
                return False
            s.pop()
    return len(s) == 0


def eval_rpn(tokens):
    ops = {"+": lambda a, b: a + b, "-": lambda a, b: a - b,
           "*": lambda a, b: a * b, "/": lambda a, b: int(a / b)}
    s = Stack()
    for t in tokens:
        if t in ops:
            b, a = s.pop(), s.pop()
            s.push(ops[t](a, b))
        else:
            s.push(int(t))
    return s.pop()


def infix_to_postfix(tokens):
    prec = {"+": 1, "-": 1, "*": 2, "/": 2}
    out, s = [], Stack()
    for t in tokens:
        if t in prec:
            while s.peek() in prec and prec[s.peek()] >= prec[t]:
                out.append(s.pop())
            s.push(t)
        elif t == "(":
            s.push(t)
        elif t == ")":
            while s.peek() != "(":
                out.append(s.pop())
            s.pop()
        else:
            out.append(t)
    while len(s):
        out.append(s.pop())
    return out


if __name__ == "__main__":
    assert balanced("{[()()]}") and not balanced("([)]") and not balanced("((")
    assert eval_rpn(["2", "1", "+", "3", "*"]) == 9
    assert eval_rpn(["4", "13", "5", "/", "+"]) == 6
    pf = infix_to_postfix("3 + 4 * ( 2 - 1 )".split())
    assert pf == ["3", "4", "2", "1", "-", "*", "+"]
    assert eval_rpn(pf) == 7
    ms = MinStack()
    for v in [5, 3, 7, 2]:
        ms.push(v)
    assert ms.min() == 2 and ms.pop() == 2 and ms.min() == 3
    print("algo_47 stack: all tests passed")
