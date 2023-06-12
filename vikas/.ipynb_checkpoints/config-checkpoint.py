bucket_name=""
bucket_uri="s3:"+"//"+bucket_name
version=1
artifact_uri=bucket_uri+str(version)
data_path=bucket_uri+"/"+"data/data.csv"
processed_train=bucket_uri+"/"+"processed/train.csv"
processed_test=bucket_uri+"/"+"processed/test.csv"
