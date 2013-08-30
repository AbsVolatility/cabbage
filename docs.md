# Documentation for Cabbage v0.3.0

Warning: this document is by no means complete.

## Table of Contents

 - Types
 - Keywords
 - Operators
 - Functions
 - Loops and Conditionals

## Types

There are six types in Cabbage: integers, floats, strings, lists, booleans and functions.

Strings must be enclosed with single quotes (`'`).

Lists are contained inside square brackets (`[]`) and elements are separated by commas. Lists (and strings) can be indexed\sliced with this syntax:

    <sequence>[<index>]
    <sequence>[<start>:<stop>:<step>]

List comprehensions are written like so:

    [ <expr> | <id> <- <list> (, <id> <- <list>)* (: <cond>)? ]

Functions can be defined as such:

    +@ <name> : <params>
    { <stmts> };

To set a return value for the function (other than the default `None`), you add this in the function definition where you want it to return:

    ~ <return-value>;

Note that the function stops execution once it hits a return statement. There can however be multiple return statements, usually used with conditional blocks.

Lambdas are simply one-statement functions. They return an expression evaluated given some parameters. The syntax is this:

    {<params>: <expression>};

---
Each statment must end in a semicolon (`;`).

## Keywords

### Assignment:

    <id> <- <value>;

### Augmented Assignment

    <id> <op>< <value>;

`<op>` should be replaced by one of these operators:

    +, -, *, /, ^, %, .&, .|, .^

There is also "right augmented assignment", where the syntax is as such:

    <value> <op>> <id>

So for example, `2 ^> i;` is equivalent to `i <- 2^i;`

There is also support for a sort of "unary augmented assignment":

    <op(s)><id> <;

Where `<op(s)>` should be replaced by one or more unary operators. For example, `-a<;` is equivalent to `a <- -a;`

## Operators

### Arithmetic

    # a + b, a - b, a * b, a / b, a ** b, a % b
    a + b, a - b, a * b, a / b, a ^ b, a % b

The `+` and `*` operators can also be used with strings and list. A string plus another string concatenates the two and returns the result. A string multiplied by a integer repeats the string the given number of times and concatenates the result. The same applies with lists. All other operators can only be used with numbers.

### Bitwise

    # a & b, a | b, a ^ b
    a .& b, a .| b, a .^ b

### Boolean

    # a and b, a or b
    a && b, a || b

### Comparisons

    # a < b, a <= b, a == b, a >= b, a > b, a != b
    a < b, a <= b, a = b, a >= b, a > b, a != b

The `<`, `<=`, `>=` and `>` operators can currently only be used with numbers.

### Range

The range operator can take two integers and return a list of all integers between the two values, including those values. The syntax is:

    a .. b

### Map

This is the map function:

    <function> # <list>

### Unary

These are the unary operators:

 - `+` - identity
 - `-` - unary minus / reverse sequence
 - `*` - sign function
 - `|` - absolute value / length
 - `.~` - bitwise not
 - `!` - boolean not

## Functions

Functions are called using this syntax:

    <func_name>(<param_list>);

The `<param_list>` is a list of values separated by commas (`,`).

### Builtins

There are currently two builtin functions in Cabbage - `base` and `type`

`base` can either take a string and convert it from a given base to an integer, or take an integer and convert it to a given base to a string. A custom alphabet can be supplied if you don't want to use the default (the digits 0 - 9 plus all lower-cased letter in order).

`type` determines the type of an object.

### Special Functions

Special functions are prefixed with the `@` character.

 - `@<` takes one line of input from stdin
 - `@>` prints an object to stdout

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

There can also be `elif` blocks - any number of them:

    :<cond> { <if-block> }
    :<cond> { <elif-block> }
    ...
    { <else-block> };

### Switch/Case

    -: <expr>
    : <val> { <block> }
    ...
    { <block> };  # default block

### Ternary

The ternary operator is written as such:

    <cond> ? <if-stmt> : <else-stmt>