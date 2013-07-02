# Documentation for Cabbage v0.4

## Table of Contents

 - Types
 - Keywords
 - Operators
 - Functions
 - Loops and Conditionals

## Types

There are four types that can be used in Cabbage: integers, floats, strings, and lists. Currently, every type is support by every mode, with the exception that rebel mode does not support float values.

Strings must be enclosed with single quotes (`'`).

---
Each statment must end in a semicolon (`;`).

## Keywords

### To declare a new variable:

    + @ <id>;

Variables need to be declared before they can be used. If a variable has already been declared with the same name, it yields an error. To initiate a variable with a value:

    + @ <id> <@ <value>;

### To assign a variable a new value:

    <id> <@ <value>;

### The print statement:

    \@/ <value>;

## Operators

### Arithmetic

    # a + b, a - b, a * b, a / b, a ** b
    a + b, a - b, a * b, a / b, a ^ b

The `+` and `*` operators can also be used with strings and list. A string plus another string concatenates the two and returns the result. A string multiplied by a integer repeats the string the given number of times and concatenates the result. The same applies with lists.

### Bitwise

    # a & b, a | b, a ^ b, ~a
    a .& b, a .| b, a .^ b, ~a

### Comparisons

    # a < b, a <= b, a == b, a >= b, a > b, a != b
    a < b, a <= b, a = b, a >= b, a > b, a != b

The `<`, `<=`, `>=` and `>` operators can currently only be used with numbers.

### Range

The range operator can take two integers and return a list of all integers between the two values, including those values. The syntax is:

    a .. b

## Functions

Functions are called using this syntax:

    <func_name>(<param_list>);

The `<param_list>` is a list of values separated by commas (`,`).

### Builtins

There are currently two builtin functions in Cabbage - `base`, and `input`

`base` can either take a string and convert it from a given base to an integer, or take an integer and convert it to a given base to a string. A custom alphabet can be supplied if you don't want to use the default (the digits 0 - 9 plus all lower-cased letter in order).

`input` simply takes input from standard in.

## Loops and Conditionals

There are currently no looping contructs available in Cabbage

### If/Else

The `if/else` block is written as such:

    :<cond> { <if-block> };

Or with an additional else block:

    :<cond> { <if-block> }{ <else-block> };

### Ternary

The ternary operator is written as such:

    <cond> ? <if-stmt> : <else-stmt>