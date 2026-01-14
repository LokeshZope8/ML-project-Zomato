from src.config.configuration import MODEL_FILE_PATH
from src.config.configuration import PREPROCESSING_OBJ_FILE
from src.constants import *
from src.logger import logging
from src.exception import CustomException
import os, sys
from src.config.configuration import * 
from src.utils import load_model
import pandas as pd



class PredictionPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            preprocessor_path = PREPROCESSING_OBJ_FILE
            MODEL_PATH = MODEL_FILE_PATH

            preprocessor = load_model(preprocessor_path)
            model = load_model(MODEL_PATH)

            data_scaled = preprocessor.transform(features)
            
            pred = model.predict(data_scaled)
            return pred
        except Exception as e:
            logging.info("Error occured in prediction pipeline")
            raise CustomException(e, sys)



class CustomData:
    def __init__(self,
                Delivery_person_Age: int,
                Delivery_person_Ratings: float,
                Weather_conditions: str,
                Road_traffic_density: str,
                Festival: str,
                multiple_deliveries: int,
                distance: float,
                Type_of_order: str,
                Type_of_vehicle: str,
                Vehicle_condition: int,
                City: str):
                
        self.delivery_person_age = Delivery_person_Age
        self.delivery_person_ratings = Delivery_person_Ratings
        self.weather_conditions = Weather_conditions
        self.road_traffic_density = Road_traffic_density
        self.festival = Festival
        self.multiple_deliveries = multiple_deliveries
        self.distance = distance
        self.type_of_order = Type_of_order
        self.type_of_vehicle = Type_of_vehicle
        self.vehicle_condition = Vehicle_condition
        self.city = City

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                "Delivery_person_Age": [self.delivery_person_age],
                "Delivery_person_Ratings": [self.delivery_person_ratings],
                "Weather_conditions": [self.weather_conditions],
                "Road_traffic_density": [self.road_traffic_density],
                "Festival": [self.festival],
                "multiple_deliveries": [self.multiple_deliveries],
                "distance": [self.distance],
                "Type_of_order": [self.type_of_order],
                "Type_of_vehicle": [self.type_of_vehicle],
                "Vehicle_condition": [self.vehicle_condition],
                "City": [self.city]
            }
            df = pd.DataFrame(custom_data_input_dict)
            return df
        except Exception as e:
            logging.info("Error occured in custom pipeline dataframe")
            raise CustomException(e, sys)