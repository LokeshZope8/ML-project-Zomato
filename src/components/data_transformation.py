from src.constants import *
from src.logger import logging
from src.exception import CustomException
import os, sys
from src.config.configuration import * 
from dataclasses import dataclass
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder
from sklearn.pipeline import Pipeline
from src.utils import save_obj

class Feature_Engineering(BaseEstimator, TransformerMixin):
    def __init__(self):
        logging.info("***************Feature Engineering Started******************")

    def fit(self, X, y=None):
        """
        Sklearn requires fit() even if nothing is learned.
        """
        return self

    def distance_numpy(self, df, lat1, lon1, lat2, lon2):#calculating distance
        p = np.pi/180
        a = 0.5 - np.cos((df[lat2]-df[lat1])*p)/2 + np.cos(df[lat1]*p)*np.cos(df[lat2]*p)*(1-np.cos((df[lon2])))
        df['distance'] = 12734 * np.arccos(np.sort(a))

    def transform_data(self, df):#removing unnecessary columns from original dataset
        try:
            df.drop(['ID'], axis=1, inplace= True, errors='ignore')
            self.distance_numpy(df, 'Restaurant_latitude', 
                                'Restaurant_longitude',
                                'Delivery_location_latitude',
                                'Delivery_location_longitude')
            df.drop(['Delivery_person_ID','Restaurant_latitude', 
                                'Restaurant_longitude',
                                'Delivery_location_latitude',
                                'Delivery_location_longitude',
                                'Order_Date', 'Time_Orderd',
                                'Time_Order_picked'], axis=1, errors='ignore')
            logging.info("dropping columns from our original dataset")
            return df
        except Exception as e:
            raise CustomException(e, sys)

    def transform(self, X:pd.DataFrame, y=None):
        try:
            transformed_df = self.transform_data(X)
            return transformed_df
        except Exception as e:
            raise CustomException(e, sys)

class DataTransformationConfig(): #calling data transformation steps from configuration.py
    processed_obj_file_path = PREPROCESSING_OBJ_FILE
    transform_train_path = TRANSFORM_TRAIN_FILE_PATH
    transform_test_path = TRANSFORM_TEST_FILE_PATH
    feature_engg_obj_path = FEATURE_ENGG_OBJ_FILE_PATH

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig() #creating variable to define class DataTransformationConfig

    def get_data_tranformation_obj(self): #creating variable to call columns --> categorical, numerical, ordinal,etc...
        try:
            Road_traffic_density = ['Low', 'Medium', 'High', 'Jam']
            Weather_conditions = ['Sunny', 'Cloudy', 'Fog', 'Sandstorms', 'Windy', 'Stormy']

            categorical_columns = ['Type_of_order', 'Type_of_vehicle', 'Festival', 'City']
            ordinal_columns = ['Road_traffic_density', 'Weather_conditions']
            numerical_columns = ['Delivery_person_Age', 'Delivery_person_Ratings', 'Vehicle_condition',
                                'multiple_deliveries', 'distance']

            #defining pipeline to call numerical, categorical, and ordinal data columns
            numerical_pipeline = Pipeline(steps=[ 
                ('impute', SimpleImputer(strategy ='constant', fill_value = 0)),#filling missing values in numerical data by filling 0 (fill value =0)
                ('scaler', StandardScaler(with_mean=False))#scaling data in one scale in numeric al columns
            ])
            categorical_pipeline = Pipeline(steps=[
                ('impute', SimpleImputer(strategy ='most_frequent')),#filling missing value in catogorical columns by most frequent value in columns
                ('onehot', OneHotEncoder(handle_unknown='ignore')),#encoding categorical data using onehotencoder
                ('scaler', StandardScaler(with_mean=False))#scaling categorical data
            ])
            ordinal_pipeline = Pipeline(steps=[
                ('impute', SimpleImputer(strategy ='most_frequent')),#filling missing value in ordinal columns low,medium,high
                ('ordinal', OrdinalEncoder(categories=[Road_traffic_density, Weather_conditions])),#encoding data in columns like low=0, medium=1,high=2
                ('scaler', StandardScaler(with_mean=False))#scaling data 
            ])

            preprocessor = ColumnTransformer([#creating variable named preprocessor and passing pipelines created above--> num,cat,ordinal
                ('numerical_pipeline', numerical_pipeline,numerical_columns),#applying numerical pipeline on numerical columns
                ('categorical_pipeline', categorical_pipeline,categorical_columns),#applying categorical pipeline on categorical columns
                ('ordinal_pipeline', ordinal_pipeline,ordinal_columns)#applying ordinal pipeline on ordinal columns
            ])
            return preprocessor
            logging.info("Pipeline Steps Comleted")
        except Exception as e:
            raise CustomException(e,sys)           
    
    def get_feature_engineering_object(self):
        try:#passing Feature_Engineering class here created above
            feature_engineering = Pipeline(steps=[('fe', Feature_Engineering())])
            return feature_engineering

        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self, train_path, test_path):#to initiate data transformation process
        try:
            train_df = pd.read_csv(train_path)#reading data from path
            test_df = pd.read_csv(test_path)#reading test data from path

            logging.info("Obtaining FE steps object")
            fe_obj = self.get_feature_engineering_object()#calling getfeature engg object

            train_df = fe_obj.fit_transform(train_df)#fit_transform on train data
            test_df = fe_obj.transform(test_df)#transform on test data

            train_df.to_csv("train_data.csv")#saving fit_transform data in transform_train_dir_key as train_data csv
            test_df.to_csv("test_data.csv")#saving transform data in transform_test_dir_key as test_data csv

            processing_obj = self.get_data_tranformation_obj()#calling get_data_transformation_obj created above

            target_columns_name = "Time_taken (min)"#initiate target column

            X_train = train_df.drop(columns = target_columns_name, axis=1)#removing target cloumn from X_train data
            y_train = train_df[target_columns_name]#adding target column in y_train

            X_test = test_df.drop(columns = target_columns_name, axis=1)#removing target cloumn from X_test data
            y_test = test_df[target_columns_name]#adding target column in y_test

            X_train = processing_obj.fit_transform(X_train)
            X_test = processing_obj.transform(X_test)

        #c_ -->concat
            train_arr = np.c_[X_train, np.array(y_train)]#connecting X_train data with y_train data in array
            test_arr = np.c_[X_test, np.array(y_test)]#connecting X_test data with y_test data in array

            df_train = pd.DataFrame(train_arr)#converting array in dataframe format -->  transform data into csv
            df_test = pd.DataFrame(test_arr)#converting array in dataframe format-->  transform data into csv

            os.makedirs(os.path.dirname(self.data_transformation_config.transform_train_path), exist_ok=True)#creating folder to save train data
            df_train.to_csv(self.data_transformation_config.transform_train_path, index=False, header=True)#saving train csv file in folder

            os.makedirs(os.path.dirname(self.data_transformation_config.transform_test_path), exist_ok=True)#creating folder to save test data
            df_test.to_csv(self.data_transformation_config.transform_test_path, index=False, header=True)#savaing test csv file in folder
            
            save_obj(file_path = self.data_transformation_config.processed_obj_file_path,
                    obj=fe_obj)
            save_obj(file_path = self.data_transformation_config.feature_engg_obj_path,
                    obj=fe_obj)
            return (train_arr,
                    test_arr,
                    self.data_transformation_config.processed_obj_file_path)

        except Exception as e:
            raise CustomException(e,sys)