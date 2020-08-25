import pandas as pd
from datetime import date
from flask import Flask, render_template, request, send_file
from werkzeug import secure_filename

def make_files(working_file):

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
        df2 = df2.to_csv(f'{i}_OPEN_TICKET_{d1}.csv')
        send_file(f'{i}_OPEN_TICKET_{d1}.csv', as_attachment=True)
    return ('Files split hopefully')

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

