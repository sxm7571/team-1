#!/usr/bin/env python

from aws import iam, personalize, s3
from util import generate_name


# Setup IAM
print("Setting up IAM role...")

role_name = generate_name("role")
role_arn = iam.create_role(
    role_name=generate_name("role"),
    policy_document=open("config/template/iam_trust.json").read()
)
print(f"Role ARN: {role_arn}")

policy_arns = iam.get_policy_arns({'AmazonS3FullAccess', 'AmazonPersonalizeFullAccess'})
for policy_arn in policy_arns.values():
    iam.attach_policy_to_role(
        role_name=role_name,
        policy_arn=policy_arn
    )


# Setup S3
print("Setting up S3 bucket...")
bucket_name = generate_name("bucket")
s3.create_bucket(bucket_name)
print(f"Bucket name: {bucket_name}")
s3.set_bucket_policy(
    bucket_name=bucket_name,
    policy_document=open("config/template/s3_policy.json").read().replace("bucket-name", bucket_name)
)
s3_csv_name = "ratings.csv"
s3.upload_file(bucket_name, s3_csv_name, open("data/ratings.csv").read())


# Setup Personalize
print("Setting up Personalize...")

schema_arn = personalize.create_schema(
    schema_name=generate_name("schema"),
    path="config/template/personalize_schema.json"
)
print(f"Schema ARN: {schema_arn}")

dataset_group_arn = personalize.create_dataset_group(generate_name("dataset-group"))
print(f"Dataset Group ARN: {dataset_group_arn}")

dataset_arn = personalize.create_dataset(
    dataset_name=generate_name("dataset"),
    schema_arn=schema_arn,
    group_arn=dataset_group_arn,
    dataset_type='Interactions'  # TODO: might need to change for our dataset
)
print(f"Dataset ARN: {dataset_arn}")

# TODO: there is a bug here where the bucket policy or IAM is somehow not always fully setup when this is executed
personalize.import_dataset(
    job_name=generate_name("import-job"),
    dataset_arn=dataset_arn,
    s3_csv_path=f"s3://{bucket_name}/{s3_csv_name}",
    role_arn=role_arn
)

solution_arn = personalize.create_solution(
    solution_name=generate_name("solution"),
    dataset_group_arn=dataset_group_arn
)
print(f"Solution ARN: {solution_arn}")

# TODO: it seems a solution version is already, created with the solution so just need to poll for that creation
solution_version_arn = personalize.create_solution_version(
    solution_arn=solution_arn,
)
print(f"Solution Version ARN: {solution_version_arn}")

campaign_arn = personalize.create_campaign(
    campaign_name=generate_name("campaign"),
    solution_version_arn=solution_version_arn
)
print(f"Campaign ARN: {campaign_arn}")

print("Setup complete!")
