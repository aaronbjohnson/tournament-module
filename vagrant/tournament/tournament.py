#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database. Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM matches")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM members")
    DB.commit()
    DB.close()

def deleteTournaments():
    """Remove all the tournament records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute("DELETE FROM tournaments")
    DB.commit()
    DB.close()

def countTournaments():
    """Returns the number of tournaments currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM tournaments")
    total = c.fetchone()[0]
    DB.commit()
    DB.close()
    return total

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM members")
    total = c.fetchone()[0]
    DB.commit()
    DB.close()
    return total

def registerTournament(name):
    """Adds a tournament to the database.

    Args:
        name: the name of the tournament (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO tournaments (name) VALUES (%s)", (name,))
    DB.commit()
    DB.close()

# Add this to be able to reference unique id of each tournament
def getTournamentId(name):
    """Returns unique ID of registered tournament.

    Args:
        name: the name of the tournament.
    """
    DB = connect()
    c = DB.cursor()
    c.execute("SELECT id FROM tournaments WHERE name = (%s)", (name,))
    idNumber = c.fetchone()[0]
    DB.commit()
    DB.close()
    return idNumber

def registerPlayer(name, tournamentId):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.
  
    Args:
        name: the player's full name (need not be unique).
        tournamentId: the unique ID (number) of the tournament the player is registering for.
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO members (name, tournament) VALUES (%s, %s)", (name, tournamentId))
    DB.commit()
    DB.close()


def playerStandings(tournamentId):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
        A list of tuples, each of which contains (id, name, wins, matches):
            id: the player's unique id (assigned by the database)
            name: the player's full name (as registered)
            wins: the number of matches the player has won
            matches: the number of matches the player has played

    Args: 
        tournamentId: the unique ID (number) of the tournament.
    """

    DB = connect()
    c = DB.cursor()
    #c.execute("SELECT id, name, wins, wins + losses AS matches FROM members WHERE tournament = %s ORDER BY wins DESC", (tournamentId,))
    c.execute("SELECT * FROM standings WHERE tournament = %s ORDER BY wins DESC", (tournamentId,))
    standings = c.fetchall()
    DB.commit()
    DB.close()
    return standings

def reportMatch(tournamentId, winner, loser):
    """Records the outcome of a single match between two players.

    Args:
        tournamentId: the unique ID of the tournament.
        winner: the ID number of the player who won.
        loser: the ID number of the player who lost.
    """
    DB = connect()
    c = DB.cursor()
    c.execute("INSERT INTO matches (tournament, winner, loser) VALUES (%s, %s, %s)", (tournamentId, winner, loser))

    # Add the win to winner's record
    c.execute("UPDATE members SET wins = wins + 1 WHERE id = (%s)", (winner,))

    # Add the loss to loser's record
    c.execute("UPDATE members SET losses = losses + 1 WHERE id = (%s)", (loser,))
    DB.commit()
    DB.close()
 
def swissPairings(tournamentId):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings. Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name

    Args:
        tournamentId: the unique ID of the tournament.
    """

    DB = connect()
    c = DB.cursor()
    c.execute("SELECT id, name FROM members WHERE tournament = (%s) ORDER BY wins DESC", (tournamentId,))

    pairings = []

    results = c.fetchall()
    result_length = len(results)

    # Add counters that keep track of array positions to append to pairings array
    first = 0
    last = 1

    # Loop through results and extract pairs that are adjacent to each other and
    # append them to the pairings array. Note: the range should be the length of
    # the result divided by two because we're pushing two items at a time.
    for i in range(result_length / 2):
        pair = results[first] + results[last]
        pairings.append(pair)
        first += 2
        last += 2

    DB.commit()
    DB.close()
    return pairings



