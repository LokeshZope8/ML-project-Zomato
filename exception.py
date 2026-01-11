from flask import Flask
from src.logger import logging
from src.exception import CustomException
import os, sys
app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def index():
    try:
        raise Exception("We are testing our Exception file") # Raising Error
    except Exception as e:
        ML = CustomException(e, sys)
        logging.info(ML.error_message)
        logging.info("Testing Logging Files")
        return "Welcome to the ML project"

if __name__ == "__main__":
    app.run(debug=True) #by default port no. is 5000        
