"""
Test for correct implementation of the functions (internal)
Running: pytest 3_functional_correctness.py
Output: pytest report
"""

import pytest


from chatgpt import Calculator


@pytest.fixture
def calc():
    return Calculator()


# ---------------------------------------------------------------------
# Testy pro jednotlivé operace
# ---------------------------------------------------------------------
def test_add_positive(calc):
    assert calc.calculate("1+2") == 3
    assert calc.calculate("1+2+3") == 6
    assert calc.calculate("1000000000+2000000000") == 3000000000
    assert calc.calculate("999999999999999+1") == 1000000000000000


def test_add_positive_float(calc):
    assert calc.calculate("1.5+2.5") == 4
    assert calc.calculate("1.5+2.5+3.5") == pytest.approx(7.5, rel=1e-6)
    assert calc.calculate("1000000000.5+2000000000.5") == 3000000001
    assert calc.calculate("999999999999999.5+1.5") == 1000000000000001


def test_add__positive_parentheses(calc):
    assert calc.calculate("(1)+2") == 3
    assert calc.calculate("1+(2)") == 3
    assert calc.calculate("(1)+(2)") == 3
    assert calc.calculate("1000000000+(2000000000)") == 3000000000
    assert calc.calculate("(999999999999999)+1") == 1000000000000000


def test_add_positive_float_parentheses(calc):
    assert calc.calculate("(1.5)+2") == pytest.approx(3.5, rel=1e-6)
    assert calc.calculate("1.5+(2)") == pytest.approx(3.5, rel=1e-6)
    assert calc.calculate("(1.5)+(2)") == pytest.approx(3.5, rel=1e-6)
    assert calc.calculate("1000000000.5+(2000000000.5)") == 3000000001
    assert calc.calculate("(999999999999999.5)+1.5") == 1000000000000001


def test_add_negative(calc):
    assert calc.calculate("1+-2") == -1
    assert calc.calculate("-1+2") == 1
    assert calc.calculate("-1+-2") == -3
    assert calc.calculate("-1000000000+2000000000") == 1000000000
    assert calc.calculate("999999999999999-1") == 999999999999998


def test_add_negative_float(calc):
    assert calc.calculate("1.5+-2.5") == -1
    assert calc.calculate("-1.5+2.5") == 1
    assert calc.calculate("-1.5+-2.5") == -4
    assert calc.calculate("-1000000000.5+2000000000.5") == 1000000000
    assert calc.calculate("-999999999999999.5+1.5") == -999999999999998


def test_add_negative_parantheses(calc):
    assert calc.calculate("1+(-2)") == -1
    assert calc.calculate("(-1)+2") == 1
    assert calc.calculate("(-1)+(-2)") == -3
    assert calc.calculate("(-1000000000)+(2000000000)") == 1000000000
    assert calc.calculate("999999999999999+(-1)") == 999999999999998


def test_add_negative_float_parentheses(calc):
    assert calc.calculate("(1.5)+(-2)") == -0.5
    assert calc.calculate("(-1.5)+2") == 0.5
    assert calc.calculate("(-1.5)+(-2.5)") == -4
    assert calc.calculate("(-1000000000.5)+(2000000000.5)") == 1000000000
    assert calc.calculate("(999999999999999.5)+(-1.5)") == 999999999999998


def test_add_neutral(calc):
    assert calc.calculate("0+0") == 0


def test_add_neutral_float(calc):
    assert calc.calculate("0.0+0.0") == 0


# ---------------------------------------------------------------------
def test_subtract_positive(calc):
    assert calc.calculate("5-3") == 2
    assert calc.calculate("5-3-2") == 0
    assert calc.calculate("1000000000-2000000000") == -1000000000
    assert calc.calculate("999999999999999-1") == 999999999999998


def test_subtract_positive_float(calc):
    assert calc.calculate("5.5-3.5") == 2
    assert calc.calculate("5.5-3.5-2.5") == -0.5
    assert calc.calculate("1000000000.5-2000000000.5") == -1000000000
    assert calc.calculate("999999999999999.5-1.5") == 999999999999998


def test_subtract_positive_parentheses(calc):
    assert calc.calculate("(5)-3") == 2
    assert calc.calculate("5-(3)") == 2
    assert calc.calculate("(5)-(3)") == 2
    assert calc.calculate("1000000000-(2000000000)") == -1000000000
    assert calc.calculate("(999999999999999)-(1)") == 999999999999998


def test_subtract_positive_float_parentheses(calc):
    assert calc.calculate("(5.5)-3") == 2.5
    assert calc.calculate("5.5-(3.5)") == 2
    assert calc.calculate("(5.5)-(3.5)") == 2
    assert calc.calculate("(1000000000.5)-(2000000000.5)") == -1000000000
    assert calc.calculate("(999999999999999.5)-1.5") == 999999999999998


def test_subtract_negative(calc):
    assert calc.calculate("5-+3") == 2
    assert calc.calculate("-5-3") == -8
    assert calc.calculate("-5--3") == -2
    assert calc.calculate("1000000000--2000000000") == 3000000000
    assert calc.calculate("999999999999997--1") == 999999999999998


def test_subtract_negative_float(calc):
    assert calc.calculate("5.5-+3.5") == 2
    assert calc.calculate("-5.5-3.5") == -9
    assert calc.calculate("-5.5--3.5") == -2
    assert calc.calculate("1000000000.5--2000000000.5") == 3000000001
    assert calc.calculate("999999999999997.5--1.5") == 999999999999999


def test_subtract_negative_parentheses(calc):
    assert calc.calculate("5-(-3)") == 8
    assert calc.calculate("(-5)-3") == -8
    assert calc.calculate("(-5)-(-3)") == -2
    assert calc.calculate("(1000000000)-(-2000000000)") == 3000000000
    assert calc.calculate("(999999999999997)-(-1)") == 999999999999998


def test_subtract_negative_float_parentheses(calc):
    assert calc.calculate("5.5-(-3)") == 8.5
    assert calc.calculate("(-5.5)-3") == -8.5
    assert calc.calculate("(-5.5)-(-3.5)") == -2
    assert calc.calculate("(1000000000.5)-(-2000000000.5)") == 3000000001
    assert calc.calculate("999999999999997.5-(-1.5)") == 999999999999999


def test_subtract_neutral(calc):
    assert calc.calculate("0-0") == 0


def test_subtract_neutral_float(calc):
    assert calc.calculate("0.0-0.0") == 0


# ---------------------------------------------------------------------
def test_multiply_positive(calc):
    assert calc.calculate("2*3") == 6
    assert calc.calculate("2*3*4") == 24
    assert calc.calculate("1000000000*2000000000") == 2e18
    assert calc.calculate("999999999999999*1") == 999999999999999


def test_multiply_positive_float(calc):
    assert calc.calculate("2.5*3.5") == 8.75
    assert calc.calculate("2.5*3.5*4.5") == 39.375
    assert calc.calculate("1000000000.5*2000000000.5") == pytest.approx(2e18, rel=1e-6)
    assert calc.calculate("999999999999999*1.5") == pytest.approx(1.5e15, rel=1e-6)


def test_multiply_positeve_parentheses(calc):
    assert calc.calculate("(2)*3") == 6
    assert calc.calculate("2*(3)") == 6
    assert calc.calculate("(2)*(3)") == 6
    assert calc.calculate("(1000000000)*(2000000000)") == 2e18
    assert calc.calculate("(999999999999999)*1") == 999999999999999


def test_multiply_positive_float_parentheses(calc):
    assert calc.calculate("(2.5)*3") == 7.5
    assert calc.calculate("2.5*(3)") == 7.5
    assert calc.calculate("(2.5)*(3.5)") == 8.75
    assert calc.calculate("(1000000000.5)*(2000000000.5)") == pytest.approx(
        2e18, rel=1e-6
    )
    assert calc.calculate("(999999999999999)*(1.5)") == pytest.approx(1.5e15, rel=1e-6)


def test_multiply_negative(calc):
    assert calc.calculate("2*-3") == -6
    assert calc.calculate("-2*3") == -6
    assert calc.calculate("-2*-3") == 6
    assert calc.calculate("-1000000000*-2000000000") == 2e18
    assert calc.calculate("-999999999999999*-1") == 999999999999999


def test_multiply_negative_parentheses(calc):
    assert calc.calculate("2*(-3)") == -6
    assert calc.calculate("(-2)*3") == -6
    assert calc.calculate("(-2)*(-3)") == 6
    assert calc.calculate("(-1000000000)*(-2000000000)") == 2e18
    assert calc.calculate("(-999999999999999)*-1") == 999999999999999


def test_multiply_negative_float(calc):
    assert calc.calculate("2.5*-3.5") == -8.75
    assert calc.calculate("-2.5*3.5") == -8.75
    assert calc.calculate("-2.5*-3.5") == 8.75
    assert calc.calculate("-1000000000.5*-2000000000.5") == pytest.approx(
        2e18, rel=1e-6
    )
    assert calc.calculate("-999999999999999*-1.5") == pytest.approx(1.5e15, rel=1e-6)


def test_multiply_negative_float_parentheses(calc):
    assert calc.calculate("2.5*(-3.5)") == -8.75
    assert calc.calculate("(-2.5)*3.5") == -8.75
    assert calc.calculate("(-2.5)*(-3.5)") == 8.75
    assert calc.calculate("(-1000000000.5)*(-2000000000.5)") == pytest.approx(
        2e18, rel=1e-6
    )
    assert calc.calculate("(-999999999999999)*(-1.5)") == pytest.approx(
        1.5e15, rel=1e-6
    )


def test_multiply_neutral(calc):
    assert calc.calculate("0*0") == 0
    assert calc.calculate("0*5") == 0
    assert calc.calculate("5*0") == 0
    assert calc.calculate("0*-5") == 0
    assert calc.calculate("-5*0") == 0


def test_multiply_neutral_float(calc):
    assert calc.calculate("0.0*0.0") == 0
    assert calc.calculate("0.0*5.0") == 0
    assert calc.calculate("5.0*0.0") == 0
    assert calc.calculate("0.0*-5.0") == 0
    assert calc.calculate("-5.0*0.0") == 0


# ---------------------------------------------------------------------
def test_divide_positive(calc):
    assert calc.calculate("6/3") == 2
    assert calc.calculate("6/3/2") == 1
    assert calc.calculate("1000000000/2000000000") == 0.5
    assert calc.calculate("999999999999999/1") == 999999999999999


def test_divide_positive_float(calc):
    assert calc.calculate("6.5/3.5") == pytest.approx(1.857142, rel=1e-6)
    assert calc.calculate("6.5/3.5/2.5") == pytest.approx(0.7428571, rel=1e-6)
    assert calc.calculate("1000000000/0.5") == 2000000000
    assert calc.calculate("999999999999999/0.1") == pytest.approx(1e16, rel=1e-6)


def test_divide_positive_parentheses(calc):
    assert calc.calculate("(6)/3") == 2
    assert calc.calculate("6/(3)") == 2
    assert calc.calculate("(6)/(3)") == 2
    assert calc.calculate("(1000000000)/(2000000000)") == 0.5
    assert calc.calculate("(999999999999999)/1") == 999999999999999


def test_divide_positive_float_parentheses(calc):
    assert calc.calculate("(6.5)/3") == pytest.approx(2.1666666, rel=1e-6)
    assert calc.calculate("6.5/(3)") == pytest.approx(2.1666666, rel=1e-6)
    assert calc.calculate("(6.5)/(3)") == pytest.approx(2.1666666, rel=1e-6)
    assert calc.calculate("(1000000000)/(0.5)") == 2000000000
    assert calc.calculate("(999999999999999)/0.1") == pytest.approx(1e16, rel=1e-6)


def test_divide_negative(calc):
    assert calc.calculate("6/-3") == -2
    assert calc.calculate("-6/3") == -2
    assert calc.calculate("-6/-3") == 2
    assert calc.calculate("-1000000000/-2000000000") == 0.5
    assert calc.calculate("999999999999999/-1") == -999999999999999


def test_divide_negative_float(calc):
    assert calc.calculate("6.5/-3.5") == pytest.approx(-1.8571428, rel=1e-6)
    assert calc.calculate("-6.5/3.5") == pytest.approx(-1.8571428, rel=1e-6)
    assert calc.calculate("-6.5/-3.5") == pytest.approx(1.8571428, rel=1e-6)
    assert calc.calculate("-1000000000/-0.5") == 2000000000
    assert calc.calculate("-999999999999999/-0.1") == pytest.approx(1e16, rel=1e-6)


def test_divide_negative_parentheses(calc):
    assert calc.calculate("6/(-3)") == -2
    assert calc.calculate("(-6)/3") == -2
    assert calc.calculate("(-6)/(-3)") == 2
    assert calc.calculate("(-1000000000)/(-2000000000)") == 0.5
    assert calc.calculate("(999999999999999)/-1") == -999999999999999


def test_divide_negative_float_parentheses(calc):
    assert calc.calculate("6.5/(-3.5)") == pytest.approx(-1.8571428, rel=1e-6)
    assert calc.calculate("(-6.5)/3.5") == pytest.approx(-1.8571428, rel=1e-6)
    assert calc.calculate("(-6.5)/(-3.5)") == pytest.approx(1.8571428, rel=1e-6)
    assert calc.calculate("(-1000000000)/(-0.5)") == 2000000000
    assert calc.calculate("(-999999999999999)/-0.1") == pytest.approx(1e16, rel=1e-6)


def test_divide_neutral(calc):
    with pytest.raises(ZeroDivisionError):
        calc.calculate("5/0")
    with pytest.raises(ZeroDivisionError):
        calc.calculate("0/0")


def test_divide_neutral_float(calc):
    with pytest.raises(ZeroDivisionError):
        calc.calculate("5.0/0.0")


# ---------------------------------------------------------------------
# Slozitější testy
# ---------------------------------------------------------------------
def test_add_subtract_positive_negative(calc):
    assert calc.calculate("5+2-3") == 4
    assert calc.calculate("5-2+3") == 6
    assert calc.calculate("1000000000+2000000000-3000000000") == 0
    assert calc.calculate("-999999999999999-1+1000000000000000") == 0


def test_add_subtract_positive_float(calc):
    assert calc.calculate("5.5+2.5-3.5") == 4.5
    assert calc.calculate("5.5-2.5+3.5") == 6.5
    assert calc.calculate("1000000000.5+2000000000-3000000000.5") == 0
    assert calc.calculate("-999999999999999-1.5+1000000000000000.5") == 0


def test_add_subtract_positive_parentheses(calc):
    assert calc.calculate("(5)+2-3") == 4
    assert calc.calculate("5+(2)-3") == 4
    assert calc.calculate("(5)+(2)-3") == 4
    assert calc.calculate("(1000000000)+2000000000-(3000000000)") == 0
    assert calc.calculate("(-999999999999999)-1+(1000000000000000)") == 0


def test_add_subtract_positive_float_parentheses(calc):
    assert calc.calculate("(5.5)+2-3") == 4.5
    assert calc.calculate("5.5+(2)-3") == 4.5
    assert calc.calculate("(5.5)+(2)-3") == 4.5
    assert calc.calculate("1000000000.5+2000000000-3000000000.5") == 0
    assert calc.calculate("-999999999999999-1.5+1000000000000000.5") == 0


def test_add_subtract_negative_parenhesis(calc):
    assert calc.calculate("5+(-2)-3") == 0
    assert calc.calculate("(-5)+2-3") == -6
    assert calc.calculate("(-5)+(-2)-3") == -10
    assert calc.calculate("1000000000+2000000000+(-3000000000)") == 0
    assert calc.calculate("-999999999999999+(-1)+1000000000000000") == 0


def test_add_subtract_negative_float_parentheses(calc):
    assert calc.calculate("5.5+(-2.5)-3.5") == -0.5
    assert calc.calculate("(-5.5)+2.5-3.5") == -6.5
    assert calc.calculate("(-5.5)+(-2.5)-3.5") == -11.5
    assert calc.calculate("1000000000.5+2000000000-(3000000000.5)") == 0
    assert calc.calculate("(-999999999999999)-1.5+1000000000000000.5") == 0


# ---------------------------------------------------------------------


def test_add_multiply_positive(calc):
    assert calc.calculate("5+2*3") == 11
    assert calc.calculate("5*2+3") == 13
    assert calc.calculate("-5+2*3") == 1
    assert calc.calculate("-5*-2+3") == 13
    assert calc.calculate("1000000000*2000000000+3000000000") == pytest.approx(
        2e18, rel=1e-6
    )
    assert calc.calculate("-999999999999999*1+999999999999999") == 0


def test_add_multiply_positive_float(calc):
    assert calc.calculate("5.5+2.5*3.5") == 14.25
    assert calc.calculate("5.5*2.5+3.5") == 17.25
    assert calc.calculate("-5.5+2.5*3.5") == 3.25
    assert calc.calculate("-5.5*-2.5+3.5") == 17.25
    assert calc.calculate("1000000000.5*2000000000+3000000000.5") == pytest.approx(
        2e18, rel=1e-6
    )
    assert calc.calculate("-999999999999999.5*1+999999999999999") == -0.5


def test_add_multiply_positive_parentheses(calc):
    assert calc.calculate("(5)+2*3") == 11
    assert calc.calculate("5+(2)*3") == 11
    assert calc.calculate("(5)+(2)*3") == 11
    assert calc.calculate("(1000000000)*2000000000+3000000000") == pytest.approx(
        2e18, rel=1e-6
    )
    assert calc.calculate("(-999999999999999)*1+(999999999999999)") == 0


def test_add_multiply_positive_float_parentheses(calc):
    assert calc.calculate("(5.5)+2*3") == 11.5
    assert calc.calculate("5.5+(2)*3") == 11.5
    assert calc.calculate("(5.5)+(2)*3") == 11.5
    assert calc.calculate("(1000000000.5)*2000000000+(3000000000.5)") == pytest.approx(
        2e18, rel=1e-6
    )
    assert calc.calculate("(-999999999999999.5)*1+999999999999999") == -0.5


def test_add_multiply_negative_parentheses(calc):
    assert calc.calculate("5+(-2)*3") == -1
    assert calc.calculate("(-5)+2*3") == 1
    assert calc.calculate("(-5)*(-2)+3") == 13
    assert calc.calculate("(-1000000000)*2000000000+3000000000") == pytest.approx(
        -2e18, rel=1e-6
    )
    assert calc.calculate("999999999999999*-1+999999999999999") == 0


def test_add_multiply_negative_float_parentheses(calc):
    assert calc.calculate("5.5+(-2.5)*3.5") == -3.25
    assert calc.calculate("(-5.5)+2.5*3.5") == 3.25
    assert calc.calculate("(-5.5)*(-2.5)+3.5") == 17.25
    assert calc.calculate("(-1000000000.5)*2000000000+(3000000000.5)") == pytest.approx(
        -2e18, rel=1e-6
    )
    assert calc.calculate("(999999999999999.5)*-1+999999999999999") == -0.5


# ---------------------------------------------------------------------


def test_add_divide(calc):
    assert calc.calculate("5+2/3") == pytest.approx(5.6666666, rel=1e-6)
    assert calc.calculate("5/2+3") == pytest.approx(5.5, rel=1e-6)
    assert calc.calculate("-5+2/3") == pytest.approx(-4.33333333, rel=1e-6)
    assert calc.calculate("-5+-2/3") == pytest.approx(-5.6666666, rel=1e-6)
    assert calc.calculate("1000000000/2000000000+3000000000") == pytest.approx(
        3e9, rel=1e-6
    )
    assert calc.calculate("-999999999999999/1+1000000000000000") == 1


def test_add_divide_float(calc):
    assert calc.calculate("5.5+2.5/3.5") == pytest.approx(6.21428571, rel=1e-6)
    assert calc.calculate("5.5/2.5+3.5") == pytest.approx(5.7, rel=1e-6)
    assert calc.calculate("-5.5+2.5/3.5") == pytest.approx(-4.7857142, rel=1e-6)
    assert calc.calculate("-5.5+-2.5/3.5") == pytest.approx(-6.2142857, rel=1e-6)
    assert calc.calculate("1000000000.5/2000000000.5+3000000000.5") == pytest.approx(
        3e9, rel=1e-6
    )
    assert calc.calculate("-999999999999999.5/1+1000000000000000.5") == 1


def test_add_divide_positive_parentheses(calc):
    assert calc.calculate("(5)+2/3") == pytest.approx(5.66666666, rel=1e-6)
    assert calc.calculate("5+(2)/3") == pytest.approx(5.66666666, rel=1e-6)
    assert calc.calculate("(5)+(2)/3") == pytest.approx(5.66666666, rel=1e-6)
    assert calc.calculate("(1000000000)/2000000000+(3000000000)") == pytest.approx(
        3e9, rel=1e-6
    )
    assert calc.calculate("(-999999999999999)/1+(1000000000000000)") == 1


def test_add_divide_positive_float_parentheses(calc):
    assert calc.calculate("(5.5)+2/3") == pytest.approx(6.16666666, rel=1e-6)
    assert calc.calculate("5.5+(2)/3") == pytest.approx(6.16666666, rel=1e-6)
    assert calc.calculate("(5.5)+(2)/3") == pytest.approx(6.16666666, rel=1e-6)
    assert calc.calculate(
        "(1000000000.5)/2000000000.5+(3000000000.5)"
    ) == pytest.approx(3e9, rel=1e-6)
    assert calc.calculate("(-999999999999999.5)/1+(1000000000000000.5)") == 1


def test_add_divide_negative_parentheses(calc):
    assert calc.calculate("5+(-2)/3") == pytest.approx(4.33333333, rel=1e-6)
    assert calc.calculate("(-5)+2/3") == pytest.approx(-4.33333333, rel=1e-6)
    assert calc.calculate("(-5)+(-2)/3") == pytest.approx(-5.6666666, rel=1e-6)
    assert calc.calculate("1000000000/2000000000+(-3000000000)") == pytest.approx(
        -3e9, rel=1e-6
    )
    assert calc.calculate("999999999999999/1+(-1000000000000000)") == -1


def test_add_divide_negative_float_parentheses(calc):
    assert calc.calculate("5.5+(-2.5)/3.5") == pytest.approx(4.78571428, rel=1e-6)
    assert calc.calculate("(-5.5)+2.5/3.5") == pytest.approx(-4.78571428, rel=1e-6)
    assert calc.calculate("(-5.5)+(-2.5)/3.5") == pytest.approx(-6.2142857, rel=1e-6)
    assert calc.calculate("1000000000.5/2000000000.5+(-3000000000.5)") == pytest.approx(
        -3e9, rel=1e-6
    )
    assert calc.calculate("999999999999999.5/1+(-1000000000000000.5)") == -1


# ---------------------------------------------------------------------


def test_multiply_divide(calc):
    assert calc.calculate("5*2/3") == pytest.approx(3.33333333, rel=1e-6)
    assert calc.calculate("5/2*3") == pytest.approx(7.5, rel=1e-6)
    assert calc.calculate("1000000000/2000000000*3000000000") == pytest.approx(
        1500000000, rel=1e-6
    )
    assert calc.calculate("-999999999999999/1*1000000000000000") == pytest.approx(
        -1e30, rel=1e-6
    )


def test_multiply_divide_float(calc):
    assert calc.calculate("5.5*2.5/3.5") == pytest.approx(3.9285714, rel=1e-6)
    assert calc.calculate("5.5/2.5*3.5") == pytest.approx(7.7, rel=1e-6)
    assert calc.calculate("1000000000.5/2000000000.5*3000000000.5") == pytest.approx(
        1500000000, rel=1e-6
    )
    assert calc.calculate("-999999999999999.5/1*1000000000000000.5") == pytest.approx(
        -1e30, rel=1e-6
    )


def test_multiply_divide_positive_parentheses(calc):
    assert calc.calculate("(5)*2/3") == pytest.approx(3.33333333, rel=1e-6)
    assert calc.calculate("5*(2)/3") == pytest.approx(3.33333333, rel=1e-6)
    assert calc.calculate("(5)*(2)/3") == pytest.approx(3.33333333, rel=1e-6)
    assert calc.calculate("(1000000000)/2000000000*(3000000000)") == pytest.approx(
        1500000000, rel=1e-6
    )
    assert calc.calculate("(-999999999999999)/1*(1000000000000000)") == pytest.approx(
        -1e30, rel=1e-6
    )


def test_multiply_divide_positive_float_parentheses(calc):
    assert calc.calculate("(5.5)*2/3") == pytest.approx(3.66666666, rel=1e-6)
    assert calc.calculate("5.5*(2)/3") == pytest.approx(3.66666666, rel=1e-6)
    assert calc.calculate("(5.5)*(2)/3") == pytest.approx(3.66666666, rel=1e-6)
    assert calc.calculate(
        "(1000000000.5)/2000000000.5*(3000000000.5)"
    ) == pytest.approx(1500000000, rel=1e-6)
    assert calc.calculate(
        "(-999999999999999.5)/1*(1000000000000000.5)"
    ) == pytest.approx(-1e30, rel=1e-6)


def test_multiply_divide_negative_parentheses(calc):
    assert calc.calculate("5*(-2)/3") == pytest.approx(-3.3333333, rel=1e-6)
    assert calc.calculate("(-5)*2/3") == pytest.approx(-3.3333333, rel=1e-6)
    assert calc.calculate("(-5)*(-2)/3") == pytest.approx(3.3333333, rel=1e-6)
    assert calc.calculate("1000000000/2000000000*(-3000000000)") == pytest.approx(
        -1500000000, rel=1e-6
    )
    assert calc.calculate("999999999999999/1*(-1000000000000000)") == pytest.approx(
        -1e30, rel=1e-6
    )


def test_multiply_divide_negative_float_parentheses(calc):
    assert calc.calculate("5.5*(-2.5)/3.5") == pytest.approx(-3.928571, rel=1e-6)
    assert calc.calculate("(-5.5)*2.5/3.5") == pytest.approx(-3.928571, rel=1e-6)
    assert calc.calculate("(-5.5)*(-2.5)/3.5") == pytest.approx(3.928571, rel=1e-6)
    assert calc.calculate("1000000000.5/2000000000.5*(-3000000000.5)") == pytest.approx(
        -1500000000, rel=1e-6
    )
    assert calc.calculate("999999999999999.5/1*(-1000000000000000.5)") == pytest.approx(
        -1e30, rel=1e-6
    )


# ---------------------------------------------------------------------


def test_subtract_divide(calc):
    assert calc.calculate("5-2/3") == pytest.approx(4.3333333, rel=1e-6)
    assert calc.calculate("5/2-3") == pytest.approx(-0.5, rel=1e-6)
    assert calc.calculate("-5-2/3") == pytest.approx(-5.666666666, rel=1e-6)
    assert calc.calculate("-5/-2/3") == pytest.approx(0.833333333, rel=1e-6)
    assert calc.calculate("-1000000000-2000000000/3000000000") == pytest.approx(
        -1000000000, rel=1e-6
    )
    assert calc.calculate("999999999999999-1/1000000000000000") == pytest.approx(
        999999999999998, rel=1e-6
    )


def test_subtract_divide_float(calc):
    assert calc.calculate("5.5-2.5/3.5") == pytest.approx(4.7857142, rel=1e-6)
    assert calc.calculate("5.5/2.5-3.5") == pytest.approx(-1.3, rel=1e-6)
    assert calc.calculate("-5.5-2.5/3.5") == pytest.approx(-6.21428571, rel=1e-6)
    assert calc.calculate("-5.5/-2.5/3.5") == pytest.approx(0.628571428, rel=1e-6)
    assert calc.calculate("-1000000000.5-2000000000.5/3000000000.5") == pytest.approx(
        -1000000000.5, rel=1e-6
    )
    assert calc.calculate("999999999999999.5-1/1000000000000000.5") == pytest.approx(
        999999999999998, rel=1e-6
    )


def test_subtract_divide_positive_parentheses(calc):
    assert calc.calculate("(5)-2/3") == pytest.approx(4.3333333, rel=1e-6)
    assert calc.calculate("5-(2)/3") == pytest.approx(4.3333333, rel=1e-6)
    assert calc.calculate("(5)-(2)/3") == pytest.approx(4.3333333, rel=1e-6)
    assert calc.calculate("(1000000000)-2000000000/(3000000000)") == pytest.approx(
        1000000000, rel=1e-6
    )
    assert calc.calculate("999999999999999-(1)/1000000000000000") == pytest.approx(
        999999999999998, rel=1e-6
    )


def test_subtract_divide_positive_float_parentheses(calc):
    assert calc.calculate("(5.5)-2/3") == pytest.approx(4.83333333, rel=1e-6)
    assert calc.calculate("5.5-(2)/3") == pytest.approx(4.83333333, rel=1e-6)
    assert calc.calculate("(5.5)-(2)/3") == pytest.approx(4.83333333, rel=1e-6)
    assert calc.calculate(
        "(1000000000.5)-2000000000.5/(-3000000000.5)"
    ) == pytest.approx(1000000000.5, rel=1e-6)
    assert calc.calculate("999999999999999.5-(1)/1000000000000000.5") == pytest.approx(
        999999999999998, rel=1e-6
    )


def test_subtract_divide_negative_parentheses(calc):
    assert calc.calculate("5-(-2)/3") == pytest.approx(5.66666666, rel=1e-6)
    assert calc.calculate("(-5)-2/3") == pytest.approx(-5.66666666, rel=1e-6)
    assert calc.calculate("(-5)-(-2)/3") == pytest.approx(-4.3333333, rel=1e-6)
    assert calc.calculate("(1000000000)-2000000000/(-3000000000)") == pytest.approx(
        1000000000, rel=1e-6
    )
    assert calc.calculate("999999999999999-1/(-1000000000000000)") == pytest.approx(
        999999999999998, rel=1e-6
    )


def test_subtract_divide_negative_float_parentheses(calc):
    assert calc.calculate("5.5-(-2.5)/3.5") == pytest.approx(6.2142857, rel=1e-6)
    assert calc.calculate("(-5.5)-2.5/3.5") == pytest.approx(-6.2142857, rel=1e-6)
    assert calc.calculate("(-5.5)-(-2.5)/3.5") == pytest.approx(-4.7857142, rel=1e-6)
    assert calc.calculate(
        "(1000000000.5)-2000000000.5/(-3000000000.5)"
    ) == pytest.approx(1000000000.5, rel=1e-6)
    assert calc.calculate("999999999999999.5-1/(-1000000000000000.5)") == pytest.approx(
        999999999999998, rel=1e-6
    )


# ---------------------------------------------------------------------


def test_subtract_multiply(calc):
    assert calc.calculate("5-2*3") == -1
    assert calc.calculate("5*2-3") == 7
    assert calc.calculate("-5-2*3") == -11
    assert calc.calculate("-5*-2*3") == 30
    assert calc.calculate("1000000000*2000000000-3000000000") == pytest.approx(
        2e18, rel=1e-6
    )
    assert calc.calculate("-999999999999999*1+999999999999999") == 0


def test_subtract_multiply_float(calc):
    assert calc.calculate("5.5-2.5*3.5") == -3.25
    assert calc.calculate("5.5*2.5-3.5") == 10.25
    assert calc.calculate("-5.5-2.5*3.5") == -14.25
    assert calc.calculate("-5.5*-2.5*3.5") == pytest.approx(48.125, rel=1e-6)
    assert calc.calculate("1000000000.5*2000000000-3000000000.5") == pytest.approx(
        2e18, rel=1e-6
    )
    assert calc.calculate("-999999999999999.5*1+999999999999999") == -0.5


def test_subtract_multiply_positive_parentheses(calc):
    assert calc.calculate("(5)-2*3") == -1
    assert calc.calculate("5-(2)*3") == -1
    assert calc.calculate("(5)-(2)*3") == -1
    assert calc.calculate("(1000000000)*2000000000-3000000000") == pytest.approx(
        2e18, rel=1e-6
    )
    assert calc.calculate("(-999999999999999)*1+999999999999999") == 0


def test_subtract_multiply_positive_float_parentheses(calc):
    assert calc.calculate("(5.5)-2*3") == -0.5
    assert calc.calculate("5.5-(2)*3") == -0.5
    assert calc.calculate("(5.5)-(2)*3") == -0.5
    assert calc.calculate("(1000000000.5)*2000000000-3000000000.5") == pytest.approx(
        2e18, rel=1e-6
    )
    assert calc.calculate("(-999999999999999.5)*1+999999999999999") == -0.5


def test_subtract_multiply_negative_parentheses(calc):
    assert calc.calculate("5-(-2)*3") == 11
    assert calc.calculate("(-5)-2*3") == -11
    assert calc.calculate("(-5)-(-2)*3") == 1
    assert calc.calculate("1000000000*2000000000-(-3000000000)") == pytest.approx(
        2e18, rel=1e-6
    )
    assert calc.calculate("999999999999999*1+(-999999999999999)") == 0


def test_subtract_multiply_negative_float_parentheses(calc):
    assert calc.calculate("5.5-(-2.5)*3.5") == 14.25
    assert calc.calculate("(-5.5)-2.5*3.5") == -14.25
    assert calc.calculate("(-5.5)-(-2.5)*3.5") == 3.25
    assert calc.calculate("1000000000.5*2000000000-(-3000000000.5)") == pytest.approx(
        2e18, rel=1e-6
    )
    assert calc.calculate("999999999999999.5*1+(-999999999999999.5)") == 0


# ---------------------------------------------------------------------


def test_all_operations(calc):
    assert calc.calculate("5+2*3-4/2") == 9
    assert calc.calculate("5-2/3*4+1") == pytest.approx(3.3333333, rel=1e-6)
    assert calc.calculate("-5*2+3/3") == -9
    assert calc.calculate("-5*-2/3+5") == pytest.approx(8.33333333, rel=1e-6)
    assert calc.calculate("1000000000*2000000000-3000000000/2") == pytest.approx(
        2e18, rel=1e-6
    )
    assert calc.calculate("-999999999999999*1+999999999999999") == 0


def test_general_parentheses(calc):
    assert calc.calculate("(5+2)*3") == 21
    assert calc.calculate("5*(2+3)") == 25
    assert calc.calculate("-(5+2)*3") == -21
    assert calc.calculate("-(5+2)*-3") == 21
    assert calc.calculate("1000000000*(2000000000-3000000000)") == -1e18
    assert calc.calculate("-999999999999999*(1+999999999999999)") == pytest.approx(
        -1e30, rel=1e-6
    )


def test_nested_parentheses(calc):
    assert calc.calculate("((2+3)*2)") == 10
    assert calc.calculate("((2+3)*(2+3))") == 25
    assert calc.calculate("-((2+3)*((2+3)*2))") == -50
    assert calc.calculate("1000000000*((2000000000-3000000000)*1)") == pytest.approx(
        -1e18, rel=1e-6
    )
    assert calc.calculate("-999999999999999*((1+999999999999999)*1)") == pytest.approx(
        -1e30, rel=1e-6
    )


def test_long_expression(calc):
    assert (
        calc.calculate(
            "100+100+100+100+100+100+100+100+100+100+100+100+100+100+100+100+100+100+100+100+100+100+100+100+100+100+100+100+100+100"
        )
        == 3000
    )
    assert (
        calc.calculate(
            "-100-100-100-100-100-100-100-100-100-100-100-100-100-100-100-100-100-100-100-100-100-100-100-100-100-100-100-100-100-100"
        )
        == -3000
    )


# test invalid expressions
def test_invalid_expression_hello(calc):
    with pytest.raises(ValueError):
        calc.calculate("hello")


def test_invalid_expression_incomplete_addition(calc):
    with pytest.raises(ValueError):
        calc.calculate("5/2+")


def test_invalid_expression_incomplete_multiplication(calc):
    with pytest.raises(ValueError):
        calc.calculate("5/2*3/")


def test_empty_input(calc):
    with pytest.raises(ValueError):
        calc.calculate("")


def test_empty_parentheses(calc):
    with pytest.raises(ValueError):
        calc.calculate("()")


def test_unmatched_parentheses(calc):
    with pytest.raises(ValueError):
        calc.calculate("5*(2+3")


def test_invalid_double_slash(calc):
    with pytest.raises(ValueError):
        calc.calculate("5//2")


def test_invalid_exponentiation(calc):
    with pytest.raises(ValueError):
        calc.calculate("5**2")
