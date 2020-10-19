import boto3

from typing import Dict, Set

iam = boto3.client('iam')


def create_role(role_name: str, policy_document: str) -> str:
    response = iam.create_role(
        RoleName=role_name,
        AssumeRolePolicyDocument=policy_document
    )
    return response['Role']['Arn']


def get_policy_arns(policy_names: Set[str]) -> Dict[str, str]:
    remaining_policy_names = policy_names.copy()
    policy_arns = {}

    marker = None
    has_policies = True
    while has_policies and len(remaining_policy_names) > 0:
        # Pagination
        if marker:
            response = iam.list_policies(Marker=marker)
        else:
            response = iam.list_policies()

        if response['IsTruncated']:
            marker = response['Marker']
            has_policies = True
        else:
            has_policies = False

        # Check if any returned policy names match search
        for policy in response['Policies']:
            policy_name = policy['PolicyName']
            if policy_name in remaining_policy_names:
                policy_arns[policy_name] = policy['Arn']
                remaining_policy_names.remove(policy_name)

                if len(remaining_policy_names) == 0:
                    break

    if len(remaining_policy_names) > 0:
        raise Exception(f"Failed to find policy ARNs: {''.join(remaining_policy_names)}")

    return policy_arns


def attach_policy_to_role(role_name: str, policy_arn: str):
    iam.attach_role_policy(
        RoleName=role_name,
        PolicyArn=policy_arn
    )
