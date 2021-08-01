import pandas as pd
import praw
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import spacy

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_trf")


class RedditDataAnalyser():

    def __init__(self, client_id, client_secret, user_agent):

        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  user_agent=user_agent)

    def get_entities(self, text):
        doc = nlp(text)
        entities = {e.text: e.label_ for e in doc.ents}
        return entities

    def get_and_score_reddit_data(self):

        subreddits_to_search = ["finance", "wallstreetbets", "StockMarket", "FinanceNews", "StockNews"]

        print("Retrieving subreddits")

        submissions = []
        for subreddit in subreddits_to_search:
            print(f"Retrieving {subreddit}")
            for submission in self.reddit.subreddit(subreddit).new(limit=None):
                submissions.append({"title": submission.title, "date": submission.created_utc})
            print(f"Retrieved {subreddit}")

        print("Scoring submission data")
        sia = SIA()
        for submission in submissions:
            title = submission.get("title")
            pol_score = sia.polarity_scores(title)
            pol_score['headline'] = title
            submission.update(pol_score)
        print("Submission data scored")

        return submissions

    def get_scored_and_idd_df(self):
        submissions = self.get_and_score_reddit_data()
        df = pd.DataFrame.from_records(submissions)
        print("Identifying entities in strings")
        df["entities"] = df.apply(lambda row: self.get_entities(row["headline"]), axis=1)
        print("Strings identified")
        return df
