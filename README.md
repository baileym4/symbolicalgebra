# Symbolic Algebra

This project allows you to work with mathematical expressions symbolically. The user can write out a math equation how they normally would, and the Symbolic Algebra library will parse and solve the equation.

## Overview
The main portion of this code is contained in the lab.py file. Many of the functions utilize recursion to simplify and solve complex algebraic expressions and equations. 

This library defines classes and functions for symbolic algebraic operations, enabling you to represent and manipulate mathematical expressions. The primary classes include:

- `Symbol`: Represents a symbol object for mathematical operations.
- `Var`: Represents variable symbols for mathematical expressions.
- `Num`: Represents numbers in symbolic algebra.
- `BinOp`: Represents binary operations for symbolic algebra (e.g., addition, subtraction, multiplication, division, and exponentiation).
- Subclasses (`Add`, `Sub`, `Mul`, `Div`, `Pow`): Implement specific binary operations.

## Features

- Create symbolic algebraic expressions using variables, numbers, and basic operations.
- Evaluate expressions with variable mappings.
- Find derivatives of expressions with respect to variables.
- Simplify expressions to their minimal form.
- Support for addition, subtraction, multiplication, division, and exponentiation.

## Testing

The test.py file contains test cases created by MIT 6.101 course staff and me. testing_data contains the necessary info to run the test cases. 
