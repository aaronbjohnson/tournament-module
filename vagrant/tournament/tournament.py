#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("DELETE FROM matches")
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("DELETE FROM members")
    DB.commit()
    DB.close()

def deleteTournaments():
    """Remove all the tournament records from the database."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("DELETE FROM tournaments")
    DB.commit()
    DB.close()

def countTournaments():
    """Returns the number of tournaments currently registered."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM tournaments")
    total = c.fetchall()[0][0]
    DB.commit()
    DB.close()
    return total

def countPlayers():
    """Returns the number of players currently registered."""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("SELECT COUNT(*) FROM members")
    total = c.fetchall()[0][0]
    DB.commit()
    DB.close()
    return total

def registerTournament(name):
    """Adds a tournament to the database"""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("INSERT INTO tournaments (name) VALUES (%s)", (name,))
    DB.commit()
    DB.close()

# Add this to be able to reference unique id of each tournament
def getTournamentId(name):
    """Returns unique ID of registered tournament"""
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("SELECT id FROM tournaments WHERE name = (%s)", (name,))
    idNumber = c.fetchall()[0][0]
    DB.commit()
    DB.close()
    return idNumber

def registerPlayer(name, tournament):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("INSERT INTO members (name, tournament) VALUES (%s, %s)", (name, tournament))
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
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("SELECT id, name, wins, wins + losses AS matches FROM members WHERE tournament = %s ORDER BY wins DESC", (tournamentId,))
    standings = c.fetchall()
    DB.commit()
    DB.close()
    return standings

def reportMatch(tournament, winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("INSERT INTO matches (tournament, winner, loser) VALUES (%s, %s, %s)", (tournament, winner, loser))
    DB.commit()

    # Add the win to winner's record
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("UPDATE members SET wins = wins + 1 WHERE id = (%s)", (winner,))
    DB.commit()

    # Add the loss to loser's record
    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("UPDATE members SET losses = losses + 1 WHERE id = (%s)", (loser,))
    DB.commit()

    DB.close()
 
def swissPairings(tournament):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    DB = psycopg2.connect("dbname=tournament")
    c = DB.cursor()
    c.execute("SELECT id, name FROM members WHERE tournament = (%s) ORDER BY wins DESC", (tournament,))

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



