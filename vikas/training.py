import config
import numpy as np
import pandas as pd
from config import url_path,data_path,aws_access_key,aws_secret_access_key,bucket_name,processed_train,processed_test
import os
import boto3
from sklearn.metrics import *
import json
from sklearn.ensemble import RandomForestClassifier

df=pd.read_csv("data/processed_data/train.csv")

train_x = df.drop(["quality"], axis=1)
train_y = df[["quality"]]
rf=RandomForestClassifier()
rf.fit(train_x,train_y)

df_pred=pd.read_csv("data/processed_data/test.csv")
x_test=df_pred.iloc[:,:-1].values
y_test=df_pred.iloc[:,-1].values
y_pred=rf.predict(x_test)

acc=accuracy_score(y_test,y_pred)
cm=confusion_matrix(y_test,y_pred)
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
specificity = tn / (tn+fp)
sensitivity = tp / (tp + fn)
vocab=list(np.unique(y_test))
data=[]
for target_index,target_row in enumerate(cm):
    for predicted_index,predicted_row in enumerate(target_row):
        data.append((vocab[predicted_index],vocab[target_index],predicted_row))
        
df_cm = pd.DataFrame(data, columns=['target', 'predicted', 'count'])

if not os.path.exists('artifacts'):
    os.makedirs('artifacts')
    
with open("artifacts/confusion_matrix.csv","w") as f:
    df_cm.to_csv(f, columns=['target', 'predicted', 'count'], header=False, index=False)
    
s3 = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_access_key,
    )
try:
    s3.upload_file(
                    "artifacts/confusion_matrix.csv",
                    bucket_name,
                    "artifacts/confusion_matrix.csv",
                )
    print("confusion matrix uploaded successfully")
except Exception as e:
    print(e)
    
metadata = {
    'outputs' : [{
      'type': 'confusion_matrix',
      'format': 'csv',
      'schema': [
        {"name": "target", "type": "CATEGORY"},
        {"name": "predicted", "type": "CATEGORY"},
        {"name": "count", "type": "NUMBER"},
      ],
      'source': 'artifacts/confusion_matrix.csv',
      # Convert vocab to string because for bealean values we want "True|False" to match csv data.
      'labels': list(map(str, vocab)),
    }
    ]
  }
with open('artifacts/mlpipeline-ui-metadata.json', 'w') as f:
    json.dump(metadata, f)
try:
    s3.upload_file(
                    "artifacts/mlpipeline-ui-metadata.json",
                    bucket_name,
                    "artifacts/mlpipeline-ui-metadata.json",
                )
    print("metadata uploaded successfully")
except Exception as e:
    print(e)

metrics = {
    'metrics': [{
      'name': 'accuracy-score',
      'numberValue':  acc,
      'format': "PERCENTAGE",
    }, 
    {
      'name': 'specificity',
      'numberValue':  specificity,
      'format': "PERCENTAGE",
    }, 
    {
      'name': 'sensitivity',
      'numberValue':  sensitivity,
      'format': "PERCENTAGE",
    },]
  }
with open('artifacts/mlpipeline-metrics.json', 'w') as f:
    json.dump(metrics, f)
try:
    s3.upload_file(
                    "artifacts/mlpipeline-metrics.json",
                    bucket_name,
                    "artifacts/mlpipeline-metrics.json",
                )
    print("metrics file uploaded successfully")
except Exception as e:
    print(e)