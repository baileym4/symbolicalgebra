"""
Symbolic Algebra
"""

import doctest


class Symbol:
    """Represents symbol object for math operations"""

    # put these values in here so that all subclasses inherit the given behavior
    def __add__(self, other):
        return Add(self, other)

    def __radd__(self, other):
        return Add(other, self)

    def __sub__(self, other):
        return Sub(self, other)

    def __rsub__(self, other):
        return Sub(other, self)

    def __mul__(self, other):
        return Mul(self, other)

    def __rmul__(self, other):
        return Mul(other, self)

    def __truediv__(self, other):
        return Div(self, other)

    def __rtruediv__(self, other):
        return Div(other, self)

    def __pow__(self, other):
        return Pow(self, other)

    def __rpow__(self, other):
        return Pow(other, self)

    precedence = float("inf")
    wrap_right_at_same_precedence = False

    def simplify(self):
        return self


class Var(Symbol):
    """
    Represents Variable symbols for math to be written out
    """

    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Var('{self.name}')"

    def eval(self, mapping):
        if self.name in mapping:
            return mapping[self.name]
        else:
            raise NameError

    def __eq__(self, other):
        if type(self) == Var:
            if type(other) == Var:
                return self.name == other.name
        return False

    def deriv(self, var):
        if self.name == var:
            return Num(1)
        return Num(0)

    precedence = float("inf")
    wrap_right_at_same_precedence = False


class Num(Symbol):
    """
    Represents numbers in symbolic algebra
    """

    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return f"Num({self.n})"

    precedence = float("inf")
    wrap_right_at_same_precedence = False

    def eval(self, mapping):
        return self.n

    def __eq__(self, other):
        if type(other) == Num:
            if type(self) == Num:
                return self.n == other.n
        return False

    def deriv(self, var):
        # so that this is a symbol object
        return Num(0)


class BinOp(Symbol):
    """
    Represents Binary operations for symbolic algebra
    """

    def __init__(self, left, right):
        if isinstance(left, (int, float)):
            self.left = Num(left)
        elif isinstance(left, str):
            self.left = Var(left)
        else:
            self.left = left
        if isinstance(right, (int, float)):
            self.right = Num(right)
        elif isinstance(right, str):
            self.right = Var(right)
        else:
            self.right = right

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.left)}, {repr(self.right)})"

    def __str__(self):
        # necessary variables
        left_val = self.left
        right_val = self.right
        right_s = str(self.right)
        left_s = str(self.left)

        if self.precedence > left_val.precedence:
            left_s = f"({left_s})"

        if self.precedence > right_val.precedence:
            right_s = f"({right_s})"

        elif right_val.precedence == self.precedence:
            if self.wrap_right_at_same_precedence:
                right_s = f"({right_s})"

        elif left_val.precedence == self.precedence:
            if self.wrap_left_at_same_precedence:
                left_s = f"({left_s})"

        # return correct str
        return f"{left_s} {self.symbol} {right_s}"

    def eval(self, mapping):
        return self.answer(mapping)

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if type(self.left) == type(other.left):
            if type(self.right) == type(other.right):
                if self.right == other.right:
                    if self.left == other.left:
                        return True
        return False


class Add(BinOp):
    """
    Handles addition in symbolic algebra
    """

    symbol = "+"
    precedence = 1
    wrap_right_at_same_precedence = False
    wrap_left_at_same_precedence = False

    def answer(self, mapping):
        return self.left.eval(mapping) + self.right.eval(mapping)

    def deriv(self, var):
        return self.left.deriv(var) + self.right.deriv(var)

    def simplify(self):
        simple_left, simple_right = self.left.simplify(), self.right.simplify()

        # check condition on adding zero
        if isinstance(simple_left, Num) and simple_left.n == 0:
            return simple_right
        if isinstance(simple_right, Num) and simple_right.n == 0:
            return simple_left
        # see if numbers and return sum
        if isinstance(simple_left, Num) and isinstance(simple_right, Num):
            return Num(simple_left.n + simple_right.n)
        # else just return the sum of the two things
        return Add(simple_left, simple_right)


class Sub(BinOp):
    """
    Handles subtraction in symbolic algebra
    """

    symbol = "-"
    precedence = 1
    wrap_right_at_same_precedence = True
    wrap_left_at_same_precedence = False

    def answer(self, mapping):
        return self.left.eval(mapping) - self.right.eval(mapping)

    def deriv(self, var):
        return self.left.deriv(var) - self.right.deriv(var)

    def simplify(self):
        simple_left, simple_right = self.left.simplify(), self.right.simplify()

        # check condition on subtracting zero
        if isinstance(simple_right, Num) and simple_right.n == 0:
            return simple_left
        # check for just subtracting nums
        if isinstance(simple_left, Num) and isinstance(simple_right, Num):
            return Num(simple_left.n - simple_right.n)
        # else just return the difference of the two numbers
        return Sub(simple_left, simple_right)


class Mul(BinOp):
    """
    Handles Multiplication for binary operations
    """

    symbol = "*"
    precedence = 2
    wrap_right_at_same_precedence = False
    wrap_left_at_same_precedence = False

    def answer(self, mapping):
        return self.left.eval(mapping) * self.right.eval(mapping)

    def deriv(self, var):
        left_half = self.left * self.right.deriv(var)
        right_half = self.right * self.left.deriv(var)
        return left_half + right_half

    def simplify(self):
        simple_left, simple_right = self.left.simplify(), self.right.simplify()

        # check condition on multiplying by zero
        if simple_left == Num(0) or simple_right == Num(0):
            return Num(0)

        if simple_left == Num(1):
            return simple_right
        if simple_right == Num(1):
            return simple_left
        # if both nums
        if isinstance(simple_left, Num) and isinstance(simple_right, Num):
            return Num(simple_left.n * simple_right.n)
        # else just return the product of the two numbers
        return simple_left * simple_right


class Div(BinOp):
    """
    Handles division for binary operations
    """

    symbol = "/"
    precedence = 2
    wrap_right_at_same_precedence = True
    wrap_left_at_same_precedence = False

    def answer(self, mapping):
        return self.left.eval(mapping) / self.right.eval(mapping)

    def deriv(self, var):
        numerator = self.left
        denominator = self.right
        num_ans_1 = denominator * numerator.deriv(var)
        num_ans_2 = numerator * denominator.deriv(var)
        final = num_ans_1 - num_ans_2
        denom_ans = denominator * denominator
        return final / denom_ans

    def simplify(self):
        simple_left, simple_right = self.left.simplify(), self.right.simplify()

        # check condition on dividing zero by something
        if isinstance(simple_left, Num) and simple_left.n == 0:
            return Num(0)

        # check condition on dividing by 1
        if isinstance(simple_right, Num) and simple_right.n == 1:
            return simple_left
        # if both nums return quotient
        if isinstance(simple_left, Num) and isinstance(simple_right, Num):
            return Num(simple_left.n / simple_right.n)
        # else just return the quotient of the two numbers
        return Div(simple_left, simple_right)


class Pow(BinOp):
    """
    handles exponents
    """

    symbol = "**"
    wrap_left_at_same_precedence = True
    precedence = 3

    def deriv(self, var):
        if not isinstance(self.right, Num):
            raise TypeError
        else:
            return Mul(
                Mul(self.right, Pow(self.left, self.right - 1)),
                self.left.deriv(var),
            )

    def simplify(self):
        # check if zero raised to power
        simple_right, simple_left = self.right.simplify(), self.left.simplify()
        if isinstance(simple_right, Num) and simple_right == Num(0):
            return Num(1)
        if isinstance(simple_right, Num) and simple_right == Num(1):
            return simple_left
        if isinstance(simple_left, Num) and simple_left == Num(0):
            return Num(0)
        # check if power of 1
        if isinstance(simple_left, Num) and isinstance(simple_right, Num):
            return Num(simple_left**simple_right)
        return Pow(simple_left, simple_right)

    def answer(self, mapping):
        return self.left.eval(mapping) ** self.right.eval(mapping)


def expression(inp):
    """
    Takes in a string of opertations with numbers and returns
    a symbolic algebra output
    """
    tokenized = tokenize(inp)
    final_parse = parse(tokenized)
    return final_parse


def tokenize(inp):
    """
    splits up input string into a list of meaningful tokens
    """
    new_str = ""
    for char in inp:
        if char == "(":
            new_str += "( "
        elif char == ")":
            new_str += " )"
        else:
            new_str += char
    final_str = new_str.split()
    return final_str


def parse(tokens):
    """
    puts into desired format using symbol types
    """

    def parse_expression(index):
        operator_dict = {"*": Mul, "+": Add, "-": Sub, "/": Div, "**": Pow}
        current_look = tokens[index]
        try:
            float(current_look)
            # put in float or int depending on the correct type
            try:
                num = int(current_look)
            except:
                num = float(current_look)
            return Num(num), index + 1
        except:
            pass
        if current_look != "(":
            return Var(current_look), index + 1

        else:
            left = parse_expression(index + 1)
            opp_find = tokens[left[1]]
            operator = operator_dict[opp_find]
            right = parse_expression(left[1] + 1)

            return operator(left[0], right[0]), right[1] + 1

    parsed_expression, next_index = parse_expression(0)
    return parsed_expression


if __name__ == "__main__":
    doctest.testmod()
    curr = "(x * (2 + 3))"
    val = tokenize(curr)
    ans_1 = parse(val)
    #print(ans_1)

    test_list = [3,
6,
2,
3,
3,
3,
2,
3,
3,
2,
3,
3,
4,
3,
3,
3,
1,
2,
1,
2,
2,
1,
3,
3,
3,
3,
2,
2,
4,
1,
3,
3]
    total = 0
    for i in test_list:
        total += i
    print(total)
