import pandas as pd
from datetime import date
from flask import Flask, render_template, jsonify, request
from werkzeug import secure_filename
import os

def make_files(working_file):

    # your_directory = input('Give your directory-->')
    # filename = input('Give your file-->')
    df = pd.read_csv(working_file, header=1)
    print(df.head())

    d1 = date.today().strftime("%m-%d-%Y")

    nec_columns = ['CUSTOMER', 'CUSTOMER NAME', 'CUSTOMER REFERENCE NO', 'ORDER DATE', 'ORDER NO', 'CYCLE','ORDER AMOUNT','IN', 'OUT']

    df1 = df[nec_columns]

    types = df1['IN'].unique()

    for i in types:
        df2 = df1.loc[df1['IN'] == i]
        df2['ORDER DATE'] = pd.to_datetime(df2['ORDER DATE'])
        df2 = df2.sort_values(by='ORDER DATE')
        df2 = df2.to_csv(app.config['UPLOAD_FOLDER']+f'{i}_OPEN_TICKET_{d1}.csv')



app = Flask(__name__)


@app.route('/')
def main():
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
   if request.method == 'POST':
      original = request.files['file']
      filename = secure_filename(original.filename)
      original.stream.seek(0)
      print(original)
      return make_files(original)





if __name__ == '__main__':
    app.run(debug=True)

