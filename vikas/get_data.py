import config
import pandas as pd
from config import url_path,data_path,aws_access_key,aws_secret_access_key,bucket_name,processed_train,processed_test
import os
import boto3
df=pd.read_csv(url_path,sep=";")
if not os.path.exists('data'):
    os.makeirs('data/download_data')
df.to_csv('data/download_data/data.csv')
s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_access_key,
    )
try:
    s3.upload_file(
                    "data/download_data/data.csv",
                    bucket_name,
                    data_path,
                )
    print("file uploaded successfully")
except Exception as e:
    print(e)
