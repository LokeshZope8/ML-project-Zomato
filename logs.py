from flask import Flask
from src.logger import logging

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    logging.info("Testing Logging Files")
    return "Welcome to the ML project"

if __name__ == "__main__":
    app.run(debug=True) #by default port no. is 5000        
