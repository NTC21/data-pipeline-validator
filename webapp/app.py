# flask backend that poceesses the csv file
# from flask import Flask, render_template, request
from flask import *
import pandas as pd
import subprocess
import zipfile
import os

app = Flask(__name__)

@app.route('/') # run this function when visitingthe webapp folder
def home():
    return render_template("index.html")

# function for dealing with the input file
@app.route('/process', methods=['POST'])
def handle_data():
    file = request.files['file']
    file.save('data/raw/data.csv')
    print("Uploaded file:", file.filename)

    subprocess.run("py main.py")
    print("running subproces main.py validator, cleaning, normalizing, load_to_db")

    with zipfile.ZipFile('output/output.zip', 'w') as myzip:
        myzip.write('output/cleaned_data.csv')
        myzip.write('output/customers.csv')
        myzip.write('output/error_report.csv')
        myzip.write('output/order_items.csv')
        myzip.write('output/orders.csv')
        myzip.write('output/products.csv')
        myzip.write('output/summary_report.xlsx')
        myzip.write('db/ecommerce.db')

    return redirect(url_for('give_output'))

@app.route('/download', methods=['GET'])
def give_output():
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'output', 'output.zip'))
    return send_file(output_path, as_attachment=True)

@app.route('/example', methods=['GET'])
def example_data():
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'original-data.csv'))
    return send_file(output_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True) # starts a web server locally
