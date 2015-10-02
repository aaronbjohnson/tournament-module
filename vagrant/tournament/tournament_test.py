#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."


def testDelete():
    deleteMatches()
    deletePlayers()
    print "2. Player records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "3. After deleting, countPlayers() returns zero."

def testRegisterTournament():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerTournament("Noob Tourney")
    c = countTournaments()
    if c != 1:
        raise ValueError(
            "After one tournament registers, countTournaments() should be 1.")
    print "4. After registering a tournament, countTournaments() returns 1."

def testRegisterPlayer():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    test = "Test Tournament"
    registerTournament(test)
    tournamentId = getTournamentId(test)
    registerPlayer("Chandra Nalaar", tournamentId)
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "5. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    test = "Test Tournament"
    registerTournament(test)
    tournamentId = getTournamentId(test)
    registerPlayer("Markov Chaney", tournamentId)
    registerPlayer("Joe Malik", tournamentId)
    registerPlayer("Mao Tsu-hsi", tournamentId)
    registerPlayer("Atlanta Hope", tournamentId)
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "6. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    test = "Test Tournament"
    registerTournament(test)
    tournamentId = getTournamentId(test)
    registerPlayer("Melpomene Murray", tournamentId)
    registerPlayer("Randy Schwartz", tournamentId)
    standings = playerStandings(tournamentId)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "7. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    test = "Test Tournament"
    registerTournament(test)
    tournamentId = getTournamentId(test)
    registerPlayer("Bruno Walton", tournamentId)
    registerPlayer("Boots O'Neal", tournamentId)
    registerPlayer("Cathy Burton", tournamentId)
    registerPlayer("Diane Grant", tournamentId)
    standings = playerStandings(tournamentId)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(tournamentId, id1, id2)
    reportMatch(tournamentId, id3, id4)
    standings = playerStandings(tournamentId)
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "8. After a match, players have updated standings."

def tempPairtest():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    test = "Test Tournament"
    registerTournament(test)
    tournamentId = getTournamentId(test)
    registerPlayer("Twilight Sparkle", tournamentId)
    registerPlayer("Fluttershy", tournamentId)
    registerPlayer("Applejack", tournamentId)
    registerPlayer("Pinkie Pie", tournamentId)
    standings = playerStandings(tournamentId)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(tournamentId, id1, id2)
    reportMatch(tournamentId, id3, id4)
    pairings = swissPairings(tournamentId)


def testPairings():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    test = "Test Tournament"
    registerTournament(test)
    tournamentId = getTournamentId(test)
    registerPlayer("Twilight Sparkle", tournamentId)
    registerPlayer("Fluttershy", tournamentId)
    registerPlayer("Applejack", tournamentId)
    registerPlayer("Pinkie Pie", tournamentId)
    standings = playerStandings(tournamentId)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(tournamentId, id1, id2)
    reportMatch(tournamentId, id3, id4)
    pairings = swissPairings(tournamentId)
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "9. After one match, players with one win are paired."


if __name__ == '__main__':
    testDeleteMatches()
    testDelete()
    testCount()
    testRegisterTournament()
    testRegisterPlayer()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    tempPairtest()
    testPairings()
    print "Success!  All tests pass!"


