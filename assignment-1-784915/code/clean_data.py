import pandas as pd
from datetime import datetime
pd.options.mode.chained_assignment = None


def convert_to_number(x):
    """
    Convert string numbers to int.
    """
    convert_nb = 0
    if 'k' in x:
        convert_nb = float(x.replace('k', '')) * 10**3 # convert k to a thousand
    elif 'M' in x:
        convert_nb = float(x.replace('M', '')) * 10**6 # convert M to a million
    elif 'B' in x:
        convert_nb = float(x.replace('B', '')) * 10**9 # convert B to a Billion
    else:
        convert_nb = int(x)
    return int(convert_nb)


def clean(df):
    """
    Clean the original dataset.
    """
    # Remove rows where two last columns are null to deal with missing values in previous columns (resulting in a shift)
    df = df[pd.notnull(df['Current Ver'])]
    df = df[pd.notnull(df['Android Ver'])]

    # Convert Rating column to float
    df['Rating'] = df['Rating'].astype(float)

    # Convert Reviews column to int
    df['Reviews'] = df['Reviews'].apply(lambda x: convert_to_number(x))

    # Convert Type column to boolean
    df['Type'] = df['Type'].apply(lambda x: True if x=='free' else False)
    df.rename(columns={"Type": "Free"}, inplace=True)

    # Clean Price column by removing dollar sign
    df['Price'] = df['Price'].apply(lambda x: float(x[1:]) if x.startswith('$') else 0.0)
    df.rename(columns={"Price": "Price_dollars"}, inplace=True)

    # Convert Last Updated column to date type
    df['Last Updated'] = df['Last Updated'].apply(lambda x: datetime.strptime(x, "%B %d, %Y").date())

    return df



if __name__ == "__main__":
    path = '../data/googleplaystore.csv'

    # Read csv
    df = pd.read_csv(path, sep=',')
    
    # Clean dataframe
    df = clean(df)

    # Save dataframe in csv
    df.to_csv('../data/googleplaystore_clean.csv', sep=',', encoding='utf-8', float_format='%.1f', decimal='.')
