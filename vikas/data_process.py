import config
import pandas as pd
from config import url_path,data_path,aws_access_key,aws_secret_access_key,bucket_name,processed_train,processed_test
import os
import boto3
from sklearn.model_selection import train_test_split
if not os.path.exists('data/processed_data'):
    os.makeirs('data/processed_data')
df=pd.read_csv("data/download_data/data.csv")
train,test=train_test_split(df)
train.to_csv("data/processed_data/train.csv")
test.to_csv("data/processed_data/test.csv")
s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_access_key,
    )
try:
    s3.upload_file(
                    "data/processed_data/train.csv",
                    bucket_name,
                    processed_train,
                )
    s3.upload_file(
                    "data/processed_data/test.csv",
                    bucket_name,
                    processed_test,
                )
    print("processed file uploaded successfully")
except Exception as e:
    print(e)