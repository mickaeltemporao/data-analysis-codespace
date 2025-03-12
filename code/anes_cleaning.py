import pandas as pd
import numpy as np

# Load the data
data_url = "https://raw.githubusercontent.com/datamisc/ts-2020/main/data.csv"
anes_data = pd.read_csv(data_url, compression='gzip')

# Select and rename variables
vars = {
    "V201033": "vote_intention",
    "V201507x": "age",
    "V201600": "sex",
    "V201511x": "education",
    "V201617x": "income",
    "V201228": "party_id",
    "V201231x": "party_id_str",
    "V201232": "party_id_imp",
    "V201200": "ideology",
    "V201156": "feeling_democrat", 
    "V201157": "feeling_republican",
    "V201641": "political_knowledge_intro",
    "V201642": "political_knowledge_catch1",
    "V201643": "political_knowledge_catch_feedback",
    "V201644": "political_knowledge_senate_term",
    "V201645": "political_knowledge_least_spending",
    "V201646": "political_knowledge_house_majority",
    "V201647": "political_knowledge_senate_majority",
    "V202406": "political_interest",
    "V202407": "follow_politics_media",
    "V202408": "understand_issues"
}

df = anes_data[vars.keys()]
df = df.rename(columns=vars)

# Define a function to clean and recode political knowledge responses
def clean_knowledge_variable(series, correct_values):
    # Replace invalid codes with NaN
    series_cleaned = series.replace([-9, -5, -4, -1], np.nan)
    # Recode correct answers as 1, others as 0
    series_cleaned = series_cleaned.apply(lambda x: 1 if x in correct_values else 0)
    return series_cleaned

df['political_knowledge_senate_term'] = clean_knowledge_variable(df['political_knowledge_senate_term'], [6])
df['political_knowledge_least_spending'] = clean_knowledge_variable(df['political_knowledge_least_spending'], [1])
df['political_knowledge_house_majority'] = clean_knowledge_variable(df['political_knowledge_house_majority'], [1])
df['political_knowledge_senate_majority'] = clean_knowledge_variable(df['political_knowledge_senate_majority'], [2])

# Apply an Awareness filter
df = df[df["political_knowledge_catch1"].between(1000, 2000)]

# Quick Data Cleaning
df = df[df['age'] >= 18]
df = df[df['sex'].between(1, 2)]
df['sex'] = df['sex'].apply(lambda x: 1 if x == 1 else 0)
df = df[df['education'] > 0]
df = df[df['income'] > 0]
df = df[df['ideology'].between(1, 7)]
df = df[df['party_id'].between(1, 3)]
df = df[df['party_id_str'].between(1, 7)]
df = df[df['party_id_imp'].between(1, 5)]
df = df[df['vote_intention'].between(1, 2)]
df = df[df['political_interest'] > 0]
df = df[df['follow_politics_media'] > 0]
df = df[df['understand_issues'] > 0]


file_path = "data/clean_anes.csv"
df.to_csv(file_path, index=False)

