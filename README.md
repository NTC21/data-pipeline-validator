# data-pipeline-validator
Data used from: https://www.kaggle.com/datasets/carrie1/ecommerce-data?resource=download
## Project Overview
data-pipeline-validator is a full-stack cloud-based application:
- Processes uploaded CSV files through automated validation pipeline
- Identifies and flags malformed, missing, or inconsistent data
- Generates detailed summary reports and normalized database tables
- Packages output into downloadable ZIP file
- Integrated with AWS S3 for file storage and delivery

The pipeline runs server-side, ensuring secure data handling

## Key Features
- CSV Data Upload: UI for uploading CSV files
- Data Validation: Automated checks for missing fields, invalid formats, and logical inconsistencies
- Data Normalization: Splits and cleans data into relational database tables
- Summary Report: Generates summary report in Excel
- Cloud Storage: Uploads and stores input/output files on S3
- Hosted on EC2 server

## Technologies
- Backend: Python, Flask
- Cloud: AWS S3, EC2
- Server Management: Gunicorn, systemd (auto-start on reboot)
- Data Processing: pandas, openpyxl
- Web UI: HTML5, TailwindCSS (basic styling)
- Other Tools: boto3 (AWS SDK for Python)

## Setup Instructions
1. Clone repository
### git clone https://github.com/your-username/data-pipeline-validator.git
### cd data-pipeline-validator

2. Install Python dependencies
### pip install -r requirements.txt

3. Set up AWS credentials if running locally
- And update bucket name in config.py

4. For local testing use Flask development server
### python3 webapp/app.py

5. For production deployments:
Set up Gunicorn with systemd (instructions in DEPLOYMENT.md)

6. Example Input File
An example CSV file (`original-data.csv`) is included under the `/example/` folder of this repository.  
This file shows the expected data format required by the pipeline.
If deploying on your own AWS S3 bucket, you can also upload this file manually under the `example/` prefix if you want the "Download Example File" feature to work.

## Future Improvements
- Implement user authentication for file access control
- Add NGINX reverse proxy and HTTPS
- Extend pipeline to support additional validation checks and data formats
- Implement automatic S3 lifecycle rules for file expiration

