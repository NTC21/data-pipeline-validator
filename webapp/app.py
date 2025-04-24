# flask backend that poceesses the csv file
# from flask import Flask, render_template, request
from flask import *
import pandas as pd
import subprocess
import zipfile
import os
import boto3
import logging
from botocore.exceptions import ClientError

global s3_client
s3_client = boto3.client('s3')

app = Flask(__name__)

@app.route('/') # run this function when visitingthe webapp folder
def home():
    return render_template("index.html")

# function for dealing with the input file
@app.route('/process', methods=['POST'])
def handle_data():
    file = request.files['file']
    
    # instead of saving the file to local we will upload to s3
    # file.save('data/raw/data.csv')

    try:
        s3_client.upload_fileobj(file, 'data-pipeline-project-bucket-1252634', 'uploads/data.csv')
        print("File uploaded to S3!")
    except ClientError as e:
        print("Failed to upload:", e)
        sts = boto3.client("sts")
        identity = sts.get_caller_identity()
        print(identity)
        return "Upload failed", 500

    print("Uploaded file:", file.filename)

    subprocess.run("py main.py")
    print("running subproces main.py validator, cleaning, normalizing, load_to_db")

    with zipfile.ZipFile('webapp/output/output.zip', 'w') as myzip:
        myzip.write('webapp/output/cleaned_data.csv', arcname='cleaned_data.csv')
        myzip.write('webapp/output/customers.csv', arcname='customers.csv')
        myzip.write('webapp/output/error_report.csv', arcname='error_report.csv')
        myzip.write('webapp/output/order_items.csv', arcname='order_items.csv')
        myzip.write('webapp/output/orders.csv', arcname='orders.csv')
        myzip.write('webapp/output/products.csv', arcname='products.csv')
        myzip.write('webapp/output/summary_report.xlsx', arcname='summary_report.xlsx')
        myzip.write('webapp/output/db/ecommerce.db', arcname='ecommerce.db')

    try:
        with open('webapp/output/output.zip', 'rb') as f:
            s3_client.upload_fileobj(f, 'data-pipeline-project-bucket-1252634', 'results/output.zip')
    except ClientError as e:
        print("Failed to upload:", e)
        return "Upload Failed", 500 


    return redirect(url_for('give_output'))

@app.route('/download', methods=['GET'])
def give_output():
    expiration = 300  # 5 minutes

    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': 'data-pipeline-project-bucket-1252634', 'Key': 'results/output.zip'},
            ExpiresIn=expiration
        )
        return redirect(response)
    except ClientError as e:
        print("Failed to generate pre-signed URL:", e)
        return "Could not generate download link", 500


@app.route('/example', methods=['GET'])
def example_data():
    expiration = 300  # 5 minutes

    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': 'data-pipeline-project-bucket-1252634', 'Key': 'example/original-data.csv'},
            ExpiresIn=expiration
        )
        return redirect(response)
    except ClientError as e:
        print("Failed to generate pre-signed URL:", e)
        return "Could not generate download link", 500




    # output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'original-data.csv'))
    # return send_file(output_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True) # starts a web server locally
