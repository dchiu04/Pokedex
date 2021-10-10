COMP 3522 - Assignment 3

2020-04-11

Name: Debby Chiu

Student #: A01043914

Set: 3V

Name: Norman Chiu

Student #: A00893016

Set: 3V

What it is: Shows the resulting pokemon(s), specific move(s), or abilitie(s), of the Pokemon world. It allows the user to parse for 3 different modes - pokemon, moves, or abilities - depending on their arguments. Parsed data will be shown in the console by default if output file is not specified. Each mode will show different data. Program uses pokeapi.co data and asyncio and json requests to parse the data.

How to run: Using Pycharm or the command line, run the file pokedex.py with command line arguments in order of:

  {"pokemon" | "ability" | "move"} {--inputfile "filename.txt" |--inputdata "name or id'} [--expanded] [--output "file"]

Note:

{} - mandatory

| - or (one or the other)

[] - optional


Extra notes:
- --expanded mode only changes "pokemon" mode output, do not use it with the other 2 modes
- input and output file must have a .txt extension
- we used pokes.txt as input file and output.txt as output file
- run time for --expanded flag may show lag
