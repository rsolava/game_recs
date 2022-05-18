## **Developing a pipeline for a board game recommender**

### Ryan Solava

#### Abstract
In this project, we develop a recommendation system for board games that shows
users games that meet their criteria and are similar to other games. To do so
we develop an entire pipeline that goes from obtaining the data, to
processing the data, and ends with a web application to do the recommendations.


#### Design
The pipeline for this project is as follows:

* Scrap the data from board game geek using Selenium and Beautiful Soup
* Store the data in an SQL database using SQLalchemy
* Process the data (especially cleaning up the text data) and create the NLP model
* Upload the resulting database to GitHub (since that is where Streamlit hosts from)
* The Streamlit app is a user facing web app that uses the data to give recommendations


#### Data
I scraped the data from the site [Board Game Geek](https://www.boardgamegeek.com).
Each row of data is a single board game. The features for each game include
name, year published, rating, complexity, player age, play time, publishers,
designers, mechanics, and a long text description. There are approximately 126,000 rows of data.


#### Algorithms

* Jaccard similarity to compare set data such as publishers and mechanics.
* TFIDF to form the document term matrix for the description
* LDA for topic creation
* Cosine similarity for comparing topic vectors of descriptions

#### Tools

* **Python, Pandas, and Numpy**  standard data science tools
* **Selenium** and **Beautiful Soup** for webscraping
* **sklearn** for TFIDF and LDA
* **spaCy** for text preprocessing
* SQL for database creation
* SQLalchemy for database handling in Python
* Streamlit for web app creation


#### Communication

The best way to see the results of the project is by trying out the web app
[here](https://share.streamlit.io/rsolava/game_recs/main). You can also find my
code here [personal GitHub](https://github.com/rsolava/game_recs). The results
were also communicated through a presentation with slides that can be found
at the GitHub repo above.
