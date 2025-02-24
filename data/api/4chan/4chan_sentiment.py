import spacy
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nlp = spacy.load('en_core_web_md')
sia = SentimentIntensityAnalyzer()

target = 'elon'
target_sentiments = []

df = pd.read_csv('pol_jan_20_2025.csv')
df.fillna('', inplace=True)

for text in df["comment"]:
    doc = nlp(text)
    for sent in doc.sents:
        if target.lower() in sent.text.lower():
            score = sia.polarity_scores(sent.text)["compound"]
            target_sentiments.append(score)


avg_target_sentiment = sum(target_sentiments) / len(target_sentiments)
print(f"Average Sentiment for '{target}':", avg_target_sentiment)
