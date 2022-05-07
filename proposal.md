#Building a board game recmomender
##Ryan Solava

### Question/Need

Board games are a popular and growing hobby. Hundreds of new board games
are released every month. Board Game Geek is a very popular website among
board game enthusiasts, as it catalogs every board game, and
show which games are popular and well liked by users. However, with
such a variety of games being released,
it is difficult to know how to find the ones that meet a particular player's interests.
This project seeks to use natural language processing and other data science
tools to build a recommender system for board games, matching players to games
that will be specifically of interest to them.


### Data Description

The data will be straped from the Board Game Geek website ([here](https://boardgamegeek.com/browse/boardgame/)).
Each row of data will be one board game, of which there are approximately 136,000
on the site. Some numeric and categorical data will
be collected for each game such as play time, age recommendation,
number of players, user ratings, year published, game complexity, category, genre.
Also, longer text data will be collected in the form of the game description
(which is several paragraphs long, typically).

Users will recieve recommendations in one of two ways.  If they enter a game
description, they will recieve a list of games with a similar description to
the one entered. Alternatively, if the may select one or more games, in which
case they will recieve a list of games most similar to those games based on description
and other factors. For either method, the user may select various filters
that restrict the results. For example, they may require that the game
came out in 2019, and can be played with two players.

### Tools

* Beautiful Soup for web straping
* SQL for data storage and access
* NLTK for NLP methods
* Scikitlearn for building models
* Streamlit for an app

### MVP Goals

There are a few goals for the MVP:
* Collect most of the data
* Set up the database
* Have a simple Streamlit app that will show a few board games based on a few
simple filters.
