# Documentation for Cabbage v0.2

## Table of Contents

 - Modes
 - Types
 - Keywords
 - Operators
 - Functions

## Modes

Perhaps the most important concept of this language (apart from cabbage, of course!) is the different "modes". Each mode provides a different syntax, but also present different advantages and disadvantages.

At the beginning of each program, a sort of "declaration" must be made to determine which mode the code will be written in. If this declaration is not present, the code is assumed to be written in the defualt mode. It is important to note that the declaration applies for the whole program, and cannot be changed mid-code.

### Full Support

This mode is the default mode. The "full support" mode provides the most condensed syntax of all three modes, but is also the most confusing to read. This mode provides powerful support for numbers, however does not provide much functionality with strings.

### Support

The "support" mode can be seen as a lesser version of the "full support" mode. It uses words instead of symbols for keywords, and is much more readable. It does, however, have less powerful support for numbers, but more for strings.

In support mode, variable names must begin with either `cabbage` or the shorter `cbg`.

### Rebel

The "rebel" mode is entirely opposite to the "full support" mode. It provides powerful support with strings, but can't do much with numbers. The syntax is much more similar to mainstream languages than the other modes.

### The Interpreter

The Interpreter starts in full support mode, but the mode can be changed with these commands:

    fully support!
    support!
    rebel!

Each command changes the interpreter to their respective mode. If the interpreter is already in the mode specified, the command is a no-op. Do note, however, that each mode has its own namespace, and variables declared in one mode won't be accessible in the others.

## Types

There are four types that can be used in Cabbage: integers, floats, strings, and lists. Currently, every type is support by every mode, with the exception that rebel mode does not support float values.

Strings must be enclosed with single quotes (`'`).

## Keywords

To simplify the documentation, keywords will be stated in the form:

    <full-suppport-keyword>
    <support-keyword>
    <rebel-keyword>

### To declare a new variable:

    + @ <id>
    new cabbage <id>
    var <id>

Variables need to be declared before they can be used. If a variable has already been declared with the same name, it will be overwritten. To initiate a variable with a value:

    + @ <id> <@ <value>
    new cabbage <id> <@ value
    var <id> <- <value

### To assign a variable a new value:

    <id> <@ <value>
    <id> <@ <value>
    <id> <- <value>

### The print statement:

    \@/ <value>
    plant <value>
    print <value>

In support mode, `'All Hail Brassica Prime!'` will always be prepended to output, while in rebel mode `'Death to Cabbage!'` will be prepended. In full support mode, nothing will be prepended.

## Operators

### Arithmetic

These operators can currently only be used with numbers.

    ## a + b, a - b, a * b, a / b
    # Not implemented in full support mode
    a + b, a - b, a * b, a / b
    a + b, a - b, a * b, a / b

### Comparisons

These operators can also currently only be used with numbers.

    ## a < b, a <= b, a == b, a >= b, a > b
    a .@ b, a =@ b, a @ b, a @= b, a @. b
    a < b, a <= b, a = b, a >= b, a > b
    a < b, a <= b, a = b, a >= b, a > b

## Functions

Functions are called using this global syntax:

    `<func_name>(<param_list>)`

The `<param_list>` is a list of values separated by commas (`,`).

### Builtins

There is currently only one builtin function in Cabbage - `_` in full support mode, `base` in the others.

In rebel mode, this function takes a string, and a base to convert it from, and converts the string from that base, to an integer. The alphabet is fixed as the digits 0 - 9 plus all lower-cased letter in order.

The `base` function in support mode supports custom alphabets, but otherwise the functionality is the same and in rebel mode.

In full support mode, the `_` can also take an integer, and convert it to a given base according to an alphabet.