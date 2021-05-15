import pandas as pd
import numpy as np
import logging


def add_month_day(x):
    if '-' not in x:
        return x+'-01-01'
    else:
        return x


def check_range(lower, upper, x):
    if x < lower:
        x = lower
    elif x > upper:
        x = upper

    return x


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s: %(message)s')
logging.info('Loading data...')
data = pd.read_csv('data.csv', engine='python', encoding='utf-8')
data_columns_type = dict(data.dtypes)
print(data['artists'].isna())
# CHECK IF EXIST NAN VALUES
for column in data.columns:
    logging.info(f'Cleaning column {column}, dtype: {data_columns_type[column]}')
    if True in data[column].isna().tolist():
        logging.info('NaN values')
        if data_columns_type[column] in [np.float64, np.int64]:
            # Numeric column, fill NaN with interpolated value
            logging.info('Fill NaN with polynomial interpolation')
            data[column].interpolate(method='polynomial', order=2, inplace=True)
        else:
            # String values
            logging.info('Fill NaN with the below value')
            data[column].fillna(method='bfill', inplace=True)

    else:
        logging.info(f'No NaN values')

# CHECK DUPLICATED ROWS
logging.info(f'Rows before drop duplicates rows: {len(data)}')
# We use the artist, name and release_date to determine a duplicated row
data = data.drop_duplicates(['artists', 'name', 'release_date'], keep='first')
logging.info(f'Rows after drop duplicates rows: {len(data)}')

# TRANSFORM DATA
# Adding month and day to missing values
data['release_date'] = data['release_date'].astype(str).apply(add_month_day)
# Normalize popularity
logging.info('Popularity before transform')
print(data['popularity'].describe())
# Popularity value must be in range [0,100]
data['popularity'] = data['popularity'].apply(lambda x: check_range(0, 100, x))
# Normalize to get values in range [0, 1] with 4 decimals
data['popularity'] = data['popularity'] / 100
data['popularity'] = data['popularity'].round(4)
logging.info('Popularity after transform')
print(data['popularity'].describe())
# Normalize features song that are in [0,1] range
logging.info('Transforming song features')
for column in ['acousticness', 'danceability', 'energy', 'instrumentalness', 'valence', 'liveness', 'speechiness']:
    data[column] = data[column].apply(lambda x: check_range(0, 1, x))
    data[column] = data[column].round(4)

for column in ['tempo', 'loudness', 'duration_ms']:
    data[column] = data[column].round(4)

logging.info('CLEANING finished')
logging.info('Saving data...')
data.to_csv('clean_data.csv', index=False)
