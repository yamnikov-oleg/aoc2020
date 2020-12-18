from enum import Enum
import re
from dataclasses import dataclass
from typing import List, Tuple, Union


class Expr:
    """
    A base class for an evaluatable expression.
    """
    def eval(self) -> int:
        raise NotImplementedError("eval")


@dataclass
class LiteralExpr(Expr):
    """
    A number literal. Evaluates to itself.
    """
    value: int

    def eval(self) -> int:
        return self.value


@dataclass
class ParenExpr(Expr):
    """
    A group of parentheses, wrapping around another expression.
    Evaluates to the value of the inner expression.
    """
    inner: Expr

    def eval(self) -> int:
        return self.inner.eval()


@dataclass
class AddExpr(Expr):
    """
    An addition. Evaluates to the sum of the values of the left hand side expression
    and the right hand side expression.
    """
    left_operand: Expr
    right_operand: Expr

    def eval(self) -> int:
        return self.left_operand.eval() + self.right_operand.eval()


@dataclass
class MultExpr(Expr):
    """
    A multiplication. Evaluates to the product of the values of the left hand side expression
    and the right hand side expression.
    """
    left_operand: Expr
    right_operand: Expr

    def eval(self) -> int:
        return self.left_operand.eval() * self.right_operand.eval()


class Precedence(Enum):
    """
    Enumeration for the precedence option of the parser.
    """
    # + and * are parsed evaluated at the same precedence level.
    # As a result, in an expression without parentheses former operations will be
    # nested the later, be it AddExpr or MultExpr.
    FLAT = 'flat'
    # Summations are parsed and evaluated before the multiplications.
    # As a result, in an expression without parentheses AddExpr will be nested
    # in MultExpr, but never the other way around.
    ADDITION_FIRST = 'addition_first'


@dataclass
class Parser:
    """
    A class to tokenize, parse and evaluate expressions in the text form.
    """

    # Controls the precedence of the operators.
    # Affects how the operations are nested inside the AddExpr and MultExpr trees.
    precedence: Precedence = Precedence.FLAT

    def tokenize(self, line: str) -> List[str]:
        """
        Split the expression string into more parsable string tokens.
        Valid tokens are '(', ')', '+', '*' and 'N', where N is any integer.

        Example:
            Parser().tokenize("1 + 2 * (3 + 4)")
            # => ["1", "+", "2", "*", "(", "3", "+", "4", ")"]
        """
        line = line.strip()

        if not line:
            return []

        token_re = re.compile(r'\d+|\(|\)|\+|\*')
        match = token_re.match(line)
        if not match:
            raise ValueError(f"Invalid expression: {line}")

        if match.start(0) != 0:
            raise ValueError(f"Invalid character: {line}")

        rest = line[match.end(0):]
        tokens = self.tokenize(rest)
        return [match.group(0), *tokens]

    def _parse_operand(self, tokens: List[str]) -> Tuple[Expr, List[str]]:
        """
        Expects a literal or a parenthesized expression. Parses it and returns
        the rest of the tokens.

        Examples:
            parser._parse_operand(["1", "+", "2"])
            # => LiteralExpr(1), ["+", "2"]

            parser._parse_operand(["(", "1", "+", "2", ")", "+", "3"])
            # => ParenExpr(AddExpr(LiteralExpr(1), LiteralExpr(2))), ["+", "3"]
        """
        if not tokens:
            raise ValueError("Expected an operand, found end of line")

        if tokens[0].isdigit():
            return LiteralExpr(int(tokens[0])), tokens[1:]
        elif tokens[0] == '(':
            expr, tokens = self._parse_expr(tokens[1:])
            if not tokens:
                raise ValueError(f"Expected ')', found end of line")
            return ParenExpr(expr), tokens[1:]  # [1:] skips the closing parenthesis
        else:
            raise ValueError(f"Expected operand, found {tokens!r}")

    def _parse_operator(self, tokens: List[str]) -> Tuple[str, List[str]]:
        """
        Expects a plus sign or an asterisk. Returns it as string and the rest of the tokens.

        Examples:
            parser._parse_operator(["+", "2"])
            # => "+", ["2"]
        """
        if not tokens:
            raise ValueError("Expected an operator, found end of line")

        if tokens[0] in ['+', '*']:
            return tokens[0], tokens[1:]
        else:
            raise ValueError(f"Invalid operator: {tokens[0]!r}")

    def _group_operations_flat(self, operations: List[Union[str, Expr]]) -> Expr:
        """
        Given a list of expressions and operators, groups them in a single expression
        by the flat precedence law.

        Examples:
            parser._group_operations_flat([Literal(1), "*", Literal(2), "+", Literal(3)])
            # => AddExpr(MultExpr(Literal(1), Literal(2)), Literal(3))
        """
        if not operations:
            raise ValueError(f"_group_operations_flat called with an empty list")

        # If there is only one items - it's a single operand, return it as is.
        if len(operations) == 1:
            return operations[0]

        lhs = operations[0]
        operator = operations[1]
        rhs = operations[2]
        rest_of_operations = operations[3:]

        # Group the left-most operation...
        if operator == '+':
            expr = AddExpr(lhs, rhs)
        elif operator == '*':
            expr = MultExpr(lhs, rhs)
        else:
            raise ValueError(f"Invalid operator: {operator}")

        # ...and nest it in the operation to the right by using it as an operand.
        return self._group_operations_flat([expr, *rest_of_operations])

    def _group_operations_addition_first(self, operations: List[Union[str, Expr]]) -> Expr:
        """
        Given a list of expressions and operators, groups them in a single expression
        by the "additions first" precedence law.

        Examples:
            parser._group_operations_flat([Literal(1), "*", Literal(2), "+", Literal(3)])
            # => MultExpr(Literal(1), AddExpr(Literal(2), Literal(3)))
        """
        # Group the operation items into "summation groups" - multiplicands, which
        # can be a single operand or a summation.
        # Example:
        # Given operations = [Literal(1), "*", Literal(2), "+", Literal(3)]
        # Produces sum_groups = [[Literal(1)], "*", [Literal(2), "+", Literal(3)]]
        current_sum_group = []
        sum_groups = [current_sum_group]
        while operations:
            operand = operations[0]
            operations = operations[1:]

            current_sum_group.append(operand)

            if not operations:
                break

            operator = operations[0]
            operations = operations[1:]

            if operator == '*':
                sum_groups.append(operator)
                current_sum_group = []
                sum_groups.append(current_sum_group)
                continue
            elif operator == '+':
                current_sum_group.append(operator)
                continue
            else:
                raise ValueError(f"Invalid operator: {operator!r}")

        # Convert each "summation group" into an AddExpr or a single operand
        # Example:
        # Given sum_groups = [[Literal(1)], "*", [Literal(2), "+", Literal(3)]]
        # Produces multiplicands = [Literal(1), "*", AddExpr(Literal(2), Literal(3))]
        multiplicands = [self._group_operations_flat(sum_group) for sum_group in sum_groups]

        # Convert the resulting list of multiplication operations into a single MultExpr.
        return self._group_operations_flat(multiplicands)

    def _group_operations(self, operations: List[Union[str, Expr]]) -> Expr:
        """
        Given a list of expressions and operators, groups them in a single expression
        by the precedence law selected in self.precedence.

        See _group_operations_flat and _group_operations_addition_first.
        """
        if self.precedence == Precedence.FLAT:
            return self._group_operations_flat(operations)
        elif self.precedence == Precedence.ADDITION_FIRST:
            return self._group_operations_addition_first(operations)
        else:
            raise ValueError(f"Invalid precedence value: {self.precedence}")

    def _parse_expr(self, tokens: List[str]) -> Tuple[Expr, List[str]]:
        """
        Parses a compound expression until the end of the line or until an unmatched
        closing parenthesis.
        Returns the expression and the rest of tokens (including the unmatched closing
        parenthesis if there is one).

        Example:
            parser._parse_expr(["(", "1", "+", "2", ")", "+", "3"])
            # => AddExpr(ParenExpr(AddExpr(Literal(1), Literal(2))), Literal(3)), []

            parser._parse_expr(["(", "1", "+", "2", ")", "+", "3", ")", "*", "4"])
            # => AddExpr(ParenExpr(AddExpr(Literal(1), Literal(2))), Literal(3)), [")", "*", "4"]
        """
        left_operand, tokens = self._parse_operand(tokens)
        if not tokens or tokens[0] == ')':
            return left_operand, tokens

        # Collect operand and operators into a single list
        operations: List[Union[str, Expr]] = [left_operand]

        while tokens and tokens[0] != ')':
            operator, tokens = self._parse_operator(tokens)
            operations.append(operator)

            right_operand, tokens = self._parse_operand(tokens)
            operations.append(right_operand)

        return self._group_operations(operations), tokens

    def parse_expr(self, tokens: List[str]) -> Expr:
        """
        Parses the expression given the tokens produced by self.tokenize.

        Example:
            parser._parse_expr(["(", "1", "+", "2", ")", "+", "3"])
            # => AddExpr(ParenExpr(AddExpr(Literal(1), Literal(2))), Literal(3))
        """
        expr, tokens = self._parse_expr(tokens)
        if tokens:
            raise ValueError(f"Expected end of line, found more tokens: {tokens!r}")

        return expr

    def evaluate(self, line: str) -> int:
        return self.parse_expr(self.tokenize(line)).eval()


def main():
    with open('./input.txt') as f:
        lines = [l.strip() for l in f.readlines()]

    values = [Parser().evaluate(line) for line in lines]
    print(f"Sum of results: {sum(values)}")

    values = [Parser(precedence=Precedence.ADDITION_FIRST).evaluate(line) for line in lines]
    print(f"Sum of results (part 2): {sum(values)}")


if __name__ == "__main__":
    main()
