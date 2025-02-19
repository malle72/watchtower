import csv
import json
from datetime import datetime
import html
import re

# DO NOT PUT ANY COMMENTS IN A POSITION TO BE USED AS EXECUTABLE CODE
# COMMENTS WILL BE SANITIZED TO ENSURE SAFETY WITH SQL AND HTML


# Remove annoying and possibly dangerous content from comment text
url_pattern = re.compile(r'https?:\/\/[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)')
username_pattern = re.compile(r'>>\d+')                # remove the double arrows & user number references
greentext_pattern = re.compile(r'>')                   # remove the arrows due to greentext posts
newline_pattern = re.compile(r'\n')                    # remove newline calls
safetext_pattern = re.compile(r'[^a-zA-Z0-9\s.,!?-]')  # anything else that isn't relevant to the comment.
def sanitize_and_format(text):
    text = text.lower()
    text = url_pattern.sub('', text)
    text = username_pattern.sub('', text)
    text = greentext_pattern.sub('', text)
    text = newline_pattern.sub('', text)
    text = re.sub(safetext_pattern, '', text)
    text = html.escape(text)
    return text

# iterate over a collection of raw 4chan posts in JSON format
# create a dataframe of only the date and post text.

with open('4plebs_2025-01-20.json', 'r', encoding='utf-8') as in_file:
    data = json.load(in_file)


times = [datetime.fromtimestamp(x['timestamp']) for x in data]
comments = [sanitize_and_format(t['comment']) for t in data]

with open('pol_jan_20_2025.csv', 'w', newline='', encoding='utf-8') as out_file:
    writer = csv.writer(out_file)
    writer.writerow(['timestamp', 'comment'])
    for ts, comment in zip(times, comments):
        ts_str = ts.strftime("%Y-%m-%d %H:%M:%S")  # for example
        writer.writerow([ts_str, comment])