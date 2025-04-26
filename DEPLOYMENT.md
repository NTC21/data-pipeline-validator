# Deployment Instructions

## 1. Server Setup
- EC2 t3.small instance
- Amazon Linux 2
- Security Group opened on port 5000 for inbound traffic

## 2. App Server
- Gunicorn installed via pip
- Flask app located at /home/ec2-user/data-pipeline-validator/webapp

## 3. Gunicorn Run Command
- gunicorn -w 1 -b 0.0.0.0:5000 webapp.app:app
- -w 1: One worker process
- -b 0.0.0.0:5000: Bind to all interfaces on port 5000
- webapp.app:app: Flask application object

## 4. systemd Service. A systemd service was created to automatically manage Gunicorn.
- Service file created at: /etc/systemd/system/data-pipeline-validator.service
### Service File Contents:
[Unit]
Description=Data Pipeline Validator Flask App
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/data-pipeline-validator
ExecStart=/home/ec2-user/.local/bin/gunicorn -w 1 -b 0.0.0.0:5000 webapp.app:app
Restart=always

[Install]
WantedBy=multi-user.target

### Commands Used to Enable Auto-Start

Reload systemd to recognize the new service:
sudo systemctl daemon-reload

Start the service manually the first time:
sudo systemctl start data-pipeline-validator


Enable it to start on boot:
sudo systemctl enable data-pipeline-validator

### Useful service management commands:
- Check status: sudo systemctl status data-pipeline-validator
- Restart service: sudo systemctl restart data-pipeline-validator
- Stop service: sudo systemctl stop data-pipeline-validator
- View logs: sudo journalctl -u data-pipeline-validator


## S3 Integration
- Data files uploaded to S3 bucket: data-pipeline-project-bucket-1252634
- Processed output files saved to the same bucket
- Pre-signed URL generation for download links


## Final Notes
The Flask application is production-stable and self-healing after server reboots.
Deployment matches real-world cloud deployment practices.




