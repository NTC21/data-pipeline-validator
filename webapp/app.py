# flask backend that poceesses the csv file
from flask import *
import subprocess
import zipfile
import os
import boto3
from botocore.exceptions import ClientError
import sys
import uuid
import shutil
from config import S3_BUCKET_NAME


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
    user_ip = request.remote_addr 

    # create a uuid for the upload
    run_id = uuid.uuid4()

    # upload to s3 
    current_user_upload_file_list = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=f'uploads/{user_ip}/')
    # if 3 or more delete one of the objects
    if 'Contents' in current_user_upload_file_list:
        curr_num_files = len(current_user_upload_file_list['Contents'])
        try:
            if curr_num_files > 2:
                object_list = current_user_upload_file_list['Contents']
                sorted_list = sorted(object_list, key=lambda x: x['LastModified'], reverse=True)
                files_to_delete = sorted_list[2:]
                for obj in files_to_delete:
                    s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=obj['Key'])
        except Exception as e:
            print("Error during file cleanup:", e)

    try:
        s3_client.upload_fileobj(file, S3_BUCKET_NAME, f'uploads/{user_ip}/{run_id}data.csv')
        print("File uploaded to S3!")
    except ClientError as e:
        print("Failed to upload:", e)
        sts = boto3.client("sts")
        identity = sts.get_caller_identity()
        print(identity)
        return "Upload failed", 500

    print("Uploaded file:", file.filename)
    subprocess.run([sys.executable, "main.py"], check=True)
    print("running subproces main.py validator, cleaning, normalizing, load_to_db")
    
    # make directories for the output
    os.makedirs("webapp/output", exist_ok=True)
    os.makedirs("webapp/output/db", exist_ok=True)

    with zipfile.ZipFile('webapp/output/output.zip', 'w') as myzip:
        myzip.write('webapp/output/cleaned_data.csv', arcname='cleaned_data.csv')
        myzip.write('webapp/output/customers.csv', arcname='customers.csv')
        myzip.write('webapp/output/error_report.csv', arcname='error_report.csv')
        myzip.write('webapp/output/order_items.csv', arcname='order_items.csv')
        myzip.write('webapp/output/orders.csv', arcname='orders.csv')
        myzip.write('webapp/output/products.csv', arcname='products.csv')
        myzip.write('webapp/output/summary_report.xlsx', arcname='summary_report.xlsx')
        myzip.write('webapp/output/db/ecommerce.db', arcname='ecommerce.db')

    current_user_results_file_list = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=f'results/{user_ip}/')
    if 'Contents' in current_user_results_file_list:
        curr_num_files = len(current_user_results_file_list['Contents'])

        try:
            if curr_num_files > 2:
                object_list = current_user_results_file_list['Contents']
                sorted_list = sorted(object_list, key=lambda x: x['LastModified'], reverse=True)
                files_to_delete = sorted_list[2:]
                for obj in files_to_delete:
                    s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=obj['Key'])
        except Exception as e:
            print("Error during file cleanup:", e)

    try:
        with open('webapp/output/output.zip', 'rb') as f:
            s3_client.upload_fileobj(f, S3_BUCKET_NAME, f'results/{user_ip}/{run_id}output.zip')
    except ClientError as e:
        print("Failed to upload:", e)
        return "Upload Failed", 500 

    # Delete the local output files after uploading
    try:
        if os.path.exists('webapp/output'):
            shutil.rmtree('webapp/output')
            print("Local output files deleted successfully.")
    except Exception as e:
        print("Error deleting local output files:", e)

    expiration = 300  # 5 minutes
    try:
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET_NAME, 'Key': f'results/{user_ip}/{run_id}output.zip', 'ResponseContentDisposition': 'attachment; filename="output.zip"'},
            ExpiresIn=expiration
        )
        return render_template('success.html', download_url=presigned_url)
    except ClientError as e:
        print("Failed to generate pre-signed URL:", e)
        return "Could not generate download link", 500


@app.route('/example', methods=['GET'])
def example_data():
    expiration = 300  # 5 minutes
    try:
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': S3_BUCKET_NAME, 'Key': 'example/original-data.csv'},
            ExpiresIn=expiration
        )
        return redirect(response)
    except ClientError as e:
        print("Failed to generate pre-signed URL:", e)
        return "Could not generate download link", 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True) # starts a web server open to the internet 
