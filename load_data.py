import pandas as pd
import json
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s: %(message)s')
logging.info('Loading data...')
data = pd.read_csv('clean_data.csv', engine='python')
logging.info('Iterating through rows')
data_json = []
for index, row in data.iterrows():
    logging.info(f'Transforming row {index}')
    row_json = {
        "Artists": row['artists'].replace('[\'', '').replace('\']', '').replace('[\"', '').replace('\"]', '').replace(' \'', '').replace(' \"', '').replace('\',', ',').replace('\",', ',').split(','),
        "Title": row['name'],
        "ReleaseDate": row['release_date'],
        "Year": row['year'],
        "Key": row['key'],
        "Mode": row['mode'],
        "Popularity": row['popularity'],
        "Duration": row['duration_ms'],
        "Explicit": row['explicit'],
        "Features": {
            "Acousticness": row['acousticness'],
            "Danceability": row['danceability'],
            "Energy": row['energy'],
            "Instrumentalness": row['instrumentalness'],
            "Liveness": row['liveness'],
            "Loudness": row['loudness'],
            "Speechiness": row['speechiness'],
            "Tempo": row['tempo'],
            "Valence": row['valence']
        }
    }
    data_json.append(row_json)

logging.info('Saving data to JSON file...')
with open('data.json', 'w') as output:
    json.dump(data_json, output)
