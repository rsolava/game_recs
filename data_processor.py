import pandas as pd
import numpy as np
import sqlalchemy as db

from sklearn.decomposition import LatentDirichletAllocation as LDA

from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.stem.lancaster import LancasterStemmer

from nltk import sent_tokenize


import string

import spacy
import pickle

def clean_text(s):
    if s is None:
        return ""
    s = s.lower()
    s = s.replace("check-ins","")
    s = s.replace("check-in","")
    s = re.sub('[%s]' % re.escape(string.punctuation), ' ', s)
    s = re.sub('[%s]' % re.escape(string.digits), ' ', s)
    return s

def lemmatize_document(text):
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc])

#Load current data
engine = db.create_engine("sqlite:///game.db")

connection = engine.connect()
metadata = db.MetaData()
game_table = db.Table('GAMES', metadata, autoload=True, autoload_with=engine)

query = db.select([game_table])
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
curr_df = pd.DataFrame(ResultSet)
curr_df.columns = ResultSet[0].keys()


nlp = spacy.load("en_core_web_sm")

#Clean and lemmatize desciptions
curr_df["LEMDESC"] = curr_df.DESCRIPTION.apply(clean_text).apply(lemmatize_document)

#Make DTM and fit LDA
tfidf_cv = TfidfVectorizer(ngram_range = (1,2), stop_words = "english", min_df = 5, max_df = .9)
X = tfidf_cv.fit_transform(curr_df.LEMDESC)
dtm = pd.DataFrame(X.toarray(), columns=tfidf_cv.get_feature_names())

lda = LDA(n_components = 15, random_state = 42)
lda.fit(dtm)

topics_df = lda.transform(X)
topics_df = pd.DataFrame(topics_df)

#Pickle topics matrix and lda model
pickle.dump(topics_df,open("topics_df.p","wb"))
pickle.dump(lda,open("lda.p","wb"))
