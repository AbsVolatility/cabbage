# Documentation for Cabbage v0.5

## Table of Contents

 - Types
 - Keywords
 - Operators
 - Functions
 - Loops and Conditionals

## Types

There are six types in Cabbage: integers, floats, strings, lists, booleans and functions.

Strings must be enclosed with single quotes (`'`).

Lists are contained inside square brackets (`[]`) and elements are separated by commas.

Functions can be defined as such:

    {<params>: <stmts>};

To set a return value for the function (other than the default `None`), you add this in the function definition where you want it to return:

    ~ <return-value>;

Note that the function stops execution once it hits a return statement. There can however be multiple return statements, usually used with conditional blocks.

---
Each statment must end in a semicolon (`;`).

## Keywords

### To assign a variable a value:

    <id> <- <value>;

### The print statement:

    \@/ <value>;

## Operators

### Arithmetic

    # a + b, a - b, a * b, a / b, a ** b, a % b
    a + b, a - b, a * b, a / b, a ^ b, a % b

The `+` and `*` operators can also be used with strings and list. A string plus another string concatenates the two and returns the result. A string multiplied by a integer repeats the string the given number of times and concatenates the result. The same applies with lists. All other operators can only be used with numbers.

### Bitwise

    # a & b, a | b, a ^ b, ~a
    a .& b, a .| b, a .^ b, .~a

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

### For

The `for` loop is written as such:

    @  <var> : <iterable> { <code> };

### While

The `while` loop is written as such:

    @ <cond> { <code> };

### If/Else

The `if/else` block is written as such:

    :<cond> { <if-block> };

Or with an additional else block:

    :<cond> { <if-block> }{ <else-block> };

### Ternary

The ternary operator is written as such:

    <cond> ? <if-stmt> : <else-stmt>