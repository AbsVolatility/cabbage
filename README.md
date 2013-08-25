# Cabbage

Cabbage is an esoteric, object-oriented (and still developing) language.
This implementation is written in Python 3.3 with the help of [PLY](http://www.dabeaz.com/ply/).

A handwritten, unoptimized version of a lexer is available under `cbg_lexer_handwritten.py`, and is around 1/5 slower than the lexer implemented with PLY. It can however be used instead of the other version if you change `from cbg_lexer import tokens` to `from cbg_lexer_handwritten import tokens` in the `cbg_parser.py` file.

## Esoteric?

An [esoteric programming language](http://esolangs.org/wiki/Esoteric_programming_language) (esolang for short) is "designed to experiment with weird ideas, to be hard to program in, or as a joke, rather than for practical use". This particular esolang experiments with mixing a variety of contructs from various other languages, as well as some original ones, to achieve a powerful language.

## Development

As stated above, the language has only begun to spring from the ground, and is far from complete.

## Alright, so how do I use it?

First, make sure you have Python (2.7 or 3.0+) installed. Download the files and run the "interpreter.py" program. At the beginning of each session it will ask whether to enter 'debug' mode. This allows you to see the parse tree and code generation for the input. This is only temporary, and will only be available in the development phase.

To run a complete program, run the "cabbage.py" program, and input `run(<filename>)`, replacing `<filename>` with the name of the file you want to run.

## Documentation

Click [here](docs.md) to view the current documentation.