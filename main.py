import pandas as pd
from datetime import date
from flask import Flask, render_template, request, send_file
from werkzeug import secure_filename
import zipfile, os

def zip_file():
    zipf = zipfile.ZipFile("static\\Open_Ticket.zip", 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk('static\\'):
        for file in files:
            zipf.write('static\\' + file)
    zipf.close()



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
        df2 = df2.to_csv(f'static\{i}_OPEN_TICKET_{d1}.csv')
    zip_file()

    return send_file('static\\Open_Ticket.zip',
                     mimetype='zip',
                     attachment_filename='Open_Tickets.zip',
                     as_attachment=True)







app = Flask(__name__)
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

