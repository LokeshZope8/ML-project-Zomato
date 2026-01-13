
from src.constants import *
from src.config.configuration import * 
import os, sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.logger import logging
from src.exception import CustomException
from src.components.data_transformation import DataTransformation, DataTransformationConfig

#Difining configuartion
@dataclass
class DataIngestionConfig:
    train_data_path:str = TRAIN_FILE_PATH
    test_data_path:str = TEST_FILE_PATH
    raw_data_path:str = RAW_FILE_PATH

#in this class data extract and split will happen
class DataIngestion:
    def __init__(self):#defining constructor
        self.data_ingestion_config = DataIngestionConfig()#creating data_ingestion_confif to call class DataIngestionConfig
    
    def initiate_data_ingestion(self):
        try:
            df= pd.read_csv(DATASET_PATH)#reading dataset from DATASET_PATH
            #creating raw data folder
            os.makedirs(os.path.dirname(self.data_ingestion_config.raw_data_path),exist_ok=True)

            #saving raw data in csv format in raw data folder
            df.to_csv(self.data_ingestion_config.raw_data_path,index=False)

            #splitting data into train and test 
            train_set, test_set = train_test_split(df, test_size=0.20, random_state=42)

            #creating folder to store splitted train data
            os.makedirs(os.path.dirname(self.data_ingestion_config.train_data_path),exist_ok=True)
            #saving train data in csv format
            train_set.to_csv(self.data_ingestion_config.train_data_path,header=True,)

            #creating folder to store splitted test data
            os.makedirs(os.path.dirname(self.data_ingestion_config.test_data_path),exist_ok=True)
            #saving test data in csv format
            test_set.to_csv(self.data_ingestion_config.test_data_path,header=True,)

            return(
                self.data_ingestion_config.train_data_path,
                self.data_ingestion_config.test_data_path,
            )

            
        except Exception as e:
            raise CustomException(e, sys)




if __name__ == "__main__":
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data)

    