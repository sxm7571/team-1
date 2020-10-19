import boto3

s3 = boto3.resource('s3')


def create_bucket(bucket_name: str):
    s3.create_bucket(Bucket=bucket_name)


def set_bucket_policy(bucket_name: str, policy_document: str):
    s3.BucketPolicy(bucket_name).put(
        Policy=policy_document
    )


def upload_file(bucket_name: str, key: str, data: str):
    s3.Bucket(bucket_name).put_object(Key=key, Body=data)
