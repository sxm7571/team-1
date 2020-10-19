import boto3
import time

personalize = boto3.client('personalize')


def create_schema(schema_name, path: str) -> str:
    with open(path) as f:
        response = personalize.create_schema(
            name=schema_name,
            schema=f.read()
        )
        return response['schemaArn']


def create_dataset_group(group_name: str) -> str:
    response = personalize.create_dataset_group(
        name=group_name
    )
    dataset_group_arn = response['datasetGroupArn']

    wait_for_creation(
        func=lambda: personalize.describe_dataset_group(
            datasetGroupArn=dataset_group_arn
        )['datasetGroup'],
        name="Dataset Group"
    )

    return dataset_group_arn


def create_dataset(dataset_name: str, schema_arn: str, group_arn: str, dataset_type: str) -> str:
    response = personalize.create_dataset(
        name=dataset_name,
        schemaArn=schema_arn,
        datasetGroupArn=group_arn,
        datasetType=dataset_type
    )
    dataset_arn = response['datasetArn']

    wait_for_creation(
        func=lambda: personalize.describe_dataset(
            datasetArn=dataset_arn
        )['dataset'],
        name="Dataset"
    )

    return dataset_arn


def import_dataset(job_name: str, dataset_arn: str, s3_csv_path: str, role_arn: str):
    response = personalize.create_dataset_import_job(
        jobName=job_name,
        datasetArn=dataset_arn,
        dataSource={
            'dataLocation': s3_csv_path
        },
        roleArn=role_arn
    )
    import_job_arn = response['datasetImportJobArn']

    wait_for_creation(
        func=lambda: personalize.describe_dataset_import_job(
            datasetImportJobArn=import_job_arn
        )['datasetImportJob'],
        name="Dataset Import"
    )


def create_solution(solution_name: str, dataset_group_arn: str) -> str:
    # TODO: we might want to tweak the ML config here
    response = personalize.create_solution(
        name=solution_name,
        performAutoML=True,
        datasetGroupArn=dataset_group_arn,
    )
    solution_arn = response['solutionArn']

    wait_for_creation(
        func=lambda: personalize.describe_solution(
            solutionArn=solution_arn
        )['solution'],
        name="Solution"
    )

    return solution_arn


def create_solution_version(solution_arn: str, mode: str = "FULL") -> str:
    response = personalize.create_solution_version(
        solutionArn=solution_arn,
        trainingMode=mode
    )
    solution_version_arn = response['solutionVersionArn']

    wait_for_creation(
        func=lambda: personalize.describe_solution_version(
            solutionVersionArn=solution_version_arn
        )['solutionVersion'],
        name="Solution Version"
    )

    return solution_version_arn


def create_campaign(campaign_name: str, solution_version_arn: str, min_tps: int = 5) -> str:
    response = personalize.create_campaign(
        name=campaign_name,
        solutionVersionArn=solution_version_arn,
        minProvisionedTPS=min_tps
    )
    campaign_arn = response['campaignArn']

    wait_for_creation(
        func=lambda: personalize.describe_campaign(
            campaignArn=campaign_arn
        )['campaign'],
        name="Campaign"
    )

    return campaign_arn


def wait_for_creation(func, name, refresh_interval=5):
    print(f"Waiting for {name} initialization...")
    while True:
        response = func()
        status = response['status']
        if status == "ACTIVE":
            break
        elif status == "CREATE FAILED":
            failure_reason = response.get("failureReason")
            if failure_reason:
                raise Exception(f"{name} creation failed: {failure_reason}")
            else:
                raise Exception(f"{name} creation failed")
        else:
            time.sleep(refresh_interval)
    print(f"{name} now active!")
