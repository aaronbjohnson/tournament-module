# Tournament Module

**Tournament Module** is a Python module that uses a PostgreSQL database to 
keep track of players and matches in a [Swiss-style](https://en.wikipedia.org/wiki/Swiss-system_tournament) game tournament.

The two main parts to this project are: 

 1. Defining the database schema (SQL table definitions) in tournament.sql
 2. Writing code that will use the database schema to track a Swiss tournament in tournament.py

## Contents

**tournament.sql** will create a database schema and the tables to hold 
information about the players and tournaments.

**tournament.py** contains functions that can be used to access the data in the
tournament database. See the function Docstrings in tournament.py to see a brief
description of the various functions.

**tournament_test.py** is a client program that can be used to test the 
functionality of the tournament.py functions.

## Installation

Make sure you have both [Python 2.7.10](https://www.python.org/downloads/) 
and PostgreSQL installed.

Fork this repo or download the zip folder for the repository.

## Running the program

Navigate to the tournament folder of the repository and use psql to run the
tournament.sql file:

```console
\i tournament.sql
```
This will remove any previous databases named "tournament" and will create a new
one with the tables defined in the tournament.sql file. With the database and 
tables set up, you can now write code that uses tournament.py to access and
manipulate the information in the tournament database. You can also run the 
tournament_test.py file to test the functionality of tournament.py:

```console
python tournament_test.py
```

## Bug reports

If you discover any bugs, feel free to create an issue on GitHub. I also
encourage you to help even more by forking and sending me a pull request.

https://github.com/aaronbjohnson/tournament-module/issues

## Maintainers

* Aaron Johnson (https://github.com/aaronbjohnson)

## License

MIT License

