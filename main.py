import pandas as pd
from datetime import date

your_directory = input('Give your directory-->')
filename = input('Give your file-->')

def make_files(your_directory, filename):

    df = pd.read_csv(your_directory+ "\\" + filename, header=1)

    d1 = date.today().strftime("%m-%d-%Y")

    nec_columns = ['CUSTOMER', 'CUSTOMER NAME', 'CUSTOMER REFERENCE NO', 'ORDER DATE', 'ORDER NO', 'CYCLE','ORDER AMOUNT','IN', 'OUT']

    df1 = df[nec_columns]

    types = df1['IN'].unique()

    for i in types:
        df2 = df1.loc[df1['IN'] == i]
        df2['ORDER DATE'] = pd.to_datetime(df2['ORDER DATE'])
        df2 = df2.sort_values(by='ORDER DATE')
        df2 = df2.to_csv(your_directory + '\\' + f'{i}_OPEN_TICKET_{d1}.csv')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    make_files(your_directory, filename)

