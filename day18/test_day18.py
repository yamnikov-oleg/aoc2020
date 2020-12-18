import pytest

from day18 import (AddExpr, LiteralExpr, MultExpr, ParenExpr, Parser,
                   Precedence)


@pytest.mark.parametrize("content,tokens", [
    ("1", ["1"]),
    ("(1)", ["(", "1", ")"]),
    ("1 + 2", ["1", "+", "2"]),
    ("1 * 2", ["1", "*", "2"]),
    ("1 + (2 * 3) + (4 * (5 + 6))", [
        "1", "+", "(", "2", "*", "3", ")", "+", "(",
        "4", "*", "(", "5", "+", "6", ")", ")",
    ]),
])
def test_tokenize(content, tokens):
    assert Parser().tokenize(content) == tokens


@pytest.mark.parametrize("precedence,content,expr", [
    (Precedence.FLAT, "1", LiteralExpr(1)),
    (Precedence.FLAT, "(1)", ParenExpr(LiteralExpr(1))),
    (Precedence.FLAT, "1 + 2", AddExpr(LiteralExpr(1), LiteralExpr(2))),
    (Precedence.FLAT, "1 * 2", MultExpr(LiteralExpr(1), LiteralExpr(2))),
    (Precedence.FLAT, "1 * 2 + 3", AddExpr(
        MultExpr(LiteralExpr(1), LiteralExpr(2)),
        LiteralExpr(3),
    )),
    (Precedence.ADDITION_FIRST, "1 * 2 + 3", MultExpr(
        LiteralExpr(1),
        AddExpr(LiteralExpr(2), LiteralExpr(3)),
    )),
    (Precedence.FLAT, "1 + (2 * 3) + (4 * (5 + 6))", AddExpr(
        AddExpr(
            LiteralExpr(1),
            ParenExpr(
                MultExpr(
                    LiteralExpr(2),
                    LiteralExpr(3),
                ),
            ),
        ),
        ParenExpr(
            MultExpr(
                LiteralExpr(4),
                ParenExpr(
                    AddExpr(
                        LiteralExpr(5),
                        LiteralExpr(6),
                    ),
                ),
            ),
        ),
    ))
])
def test_parse_expr(precedence, content, expr):
    parser = Parser(precedence=precedence)
    assert parser.parse_expr(parser.tokenize(content)) == expr


@pytest.mark.parametrize("precedence,line,result", [
    (Precedence.FLAT, "1 + 2 * 3 + 4 * 5 + 6", 71),
    (Precedence.FLAT, "1 + (2 * 3) + (4 * (5 + 6))", 51),
    (Precedence.FLAT, "2 * 3 + (4 * 5)", 26),
    (Precedence.FLAT, "5 + (8 * 3 + 9 + 3 * 4 * 3)", 437),
    (Precedence.FLAT, "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240),
    (Precedence.FLAT, "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632),
    (Precedence.ADDITION_FIRST, "1 + (2 * 3) + (4 * (5 + 6))", 51),
    (Precedence.ADDITION_FIRST, "2 * 3 + (4 * 5)", 46),
    (Precedence.ADDITION_FIRST, "5 + (8 * 3 + 9 + 3 * 4 * 3)", 1445),
    (Precedence.ADDITION_FIRST, "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 669060),
    (Precedence.ADDITION_FIRST, "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 23340),
])
def test_evaluate(precedence, line, result):
    assert Parser(precedence=precedence).evaluate(line) == result
