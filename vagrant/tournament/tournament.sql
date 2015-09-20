-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE tournaments (
    id serial primary key,
    name text
);

CREATE TABLE members (
    id serial primary key,
    name text,
    wins integer default 0,
    losses integer default 0,
    tournament integer references tournaments(id)
);

CREATE TABLE matches (
    id serial primary key,
    tournament integer references tournaments(id),
    winner integer references members(id),
    loser integer references members(id)
);