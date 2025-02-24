import pandas as pd
import pytextrank
import spacy

nlp = spacy.load('en_core_web_md')
nlp.add_pipe("textrank")

df = pd.read_csv('pol_jan_20_2025.csv')
df.fillna('', inplace=True)

combined_text = " ".join(df["comment"].to_list())

doc = nlp(combined_text)

global_keyphrases = [
    {
        'rank': phrase.rank,
        'text': phrase.text,
    }
    for phrase in doc._.phrases
]

df_rank = pd.DataFrame(global_keyphrases)

df_rank.to_csv('jan_20_elon_phrases.csv', index=False)
