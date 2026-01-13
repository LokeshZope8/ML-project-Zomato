import os, sys
from datetime import datetime

#to create arifact folder this is directory in which pipeline output like data ingestion, 
# data transformation, model training is stored
#artifact folder-->pipeline folder-->output with timestamp
def get_current_time_stamp():#to get current timestamp
    return f"{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}"

CURRENT_TIME_STAMP = get_current_time_stamp()

#defining dataset
ROOT_DIR_KEY = os.getcwd()     #getcwd is used to find current working directory
DATA_DIR= "dataset"
DATA_DIR_KEY= "finalTrain.csv"

#Create articat directory/artifact folder to store output of pipeline
ARTIFACT_DIR_KEY = "Artifact"

#Difining data ingestion related variable: 
DATA_INGESTION_KEY = "data_ingestion"    #CREATED THIS FOLDER IN ARTIFACT
#creating two folders named DATA_INGESTION_RAW_DATA and DATA_INGESTION_INGESTED_DATA_DIR_KEY 
# in artifact folder

DATA_INGESTION_RAW_DATA_DIR = "raw_data_dir"  
#STORING RAW.CSV DOWNLOADED DATA IN THIS FOLDER

DATA_INGESTION_INGESTED_DATA_DIR_KEY = "ingested_dir"   
#STORING TRAIN (train.csv) AND TEST (test.csv) in their special created folder in ingested_dir

#RAW_DATA_DIR_KEY will be created in DATA_INGESTION_RAW_DATA folder
RAW_DATA_DIR_KEY = "raw.csv"

TRAIN_DATA_DIR_KEY = "train.csv"
TEST_DATA_DIR_KEY = "test.csv"


#Defining Data Transformation Variables:
#artifact folder --> create transformation folder --> processor(Saving .pkl file) & transformation(saving train &test.csv file)
DATA_TRANSFORMATION_ARTIFACT = "data_transformation"
DATA_PREPROCESSED_DIR = "processor"
DATA_TRANSFORMATION_PROCESSING_OBJECT ="processor.pkl"
DATA_TRANSFORM_DIR = "transformation"
TRANSFORM_TRAIN_DIR_KEY = "train.csv"
TRANSFORM_TEST_DIR_KEY = "test.csv"
