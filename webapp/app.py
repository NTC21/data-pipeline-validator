# flask backend that poceesses the csv file
from flask import Flask

app = Flask(__name__)

@app.route('/') # run this function when visitingthe webapp folder
def home():
    return "Hello, world!"

if __name__ == "__main__":
    app.run(debug=True) # starts a web server locally
