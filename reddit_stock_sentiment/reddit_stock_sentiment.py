"""Main module."""
import pandas as pd
import praw
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy
from typing import List, Dict

from loguru import logger
# Load English tokenizer, tagger, parser, NER and word vectors

try:
    nlp = spacy.load('en_core_web_trf')
except IOError:
    logger.warning("Downloading language model for the spaCy POS tagger (don't worry, this will only happen once)")
    from spacy.cli import download
    download('en_core_web_trf')
    nlp = spacy.load('en_core_web_trf')


class RedditStockSentiment():
    def __init__(self, client_id, client_secret, user_agent):
        logger.info("Setting up reddit client")
        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  user_agent=user_agent)
        self.reddit.read_only = True

    @staticmethod
    def get_entities(text):
        doc = nlp(text)
        entities = {e.text: e.label_ for e in doc.ents}
        return entities

    def get_all_subreddit_entries(self, subreddit):
        logger.info(f"Retrieving data from {subreddit}")
        return [
            {
                "title": submission.title,
                "date": submission.created_utc,
                "subreddit": subreddit,
            }
            for submission in self.reddit.subreddit(subreddit).new(limit=None)
        ]

    def get_all_reddit_data(self, subreddits: List[str]):
        logger.info("Getting all reddit data")
        submissions = [self.get_all_subreddit_entries(subreddit) for subreddit in subreddits]
        return submissions

    def score_text_sentiment(self, text):
        sia = SentimentIntensityAnalyzer()
        pol_score = sia.polarity_scores(text)
        pol_score['headline'] = text
        return pol_score

    def get_and_score_reddit_data(self, subreddits_to_search):

        submissions = [
            {subreddit: self.get_all_subreddit_entries(subreddit)}
            for subreddit in subreddits_to_search]

        sia = SentimentIntensityAnalyzer()
        for submission in submissions:
            title = submission.get("title")
            pol_score = sia.polarity_scores(title)
            pol_score['headline'] = title
            submission.update(pol_score)
        print("Submission data scored")

        return submissions

    def get_scored_and_idd_df(self, subreddits_to_search: List):
        submissions = self.get_all_reddit_data(subreddits_to_search)
        df = pd.DataFrame.from_records(submissions[0])
        df["sentiment_score"] = df.apply(lambda row: self.score_text_sentiment(row["title"]), axis=1)
        df["entities"] = df.apply(lambda row: self.get_entities(row["title"]), axis=1)
        print("Strings identified")
        return df
