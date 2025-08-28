import boto3

from pprint import pprint

INSTANCE_ID = '394168b7-6fe9-4b77-9fcf-2bddc3a1b03c'

client = boto3.client('connect', region_name='us-east-1')

users = []

next_token = None

# List all users in the instance
while True:
    if next_token:
        response = client.list_users(
            InstanceId=INSTANCE_ID,
            MaxResults=100,
            NextToken=next_token
        )
    else:
        response = client.list_users(
            InstanceId=INSTANCE_ID,
            MaxResults=100
        )
    users.extend(response.get('UserSummaryList', []))
    next_token = response.get('NextToken')
    if not next_token:
        break

# Find user with username "kb"
kb_user_id = None
for user in users:
    if user['Username'] == 'kb':
        kb_user_id = user['Id']
        break

if kb_user_id:
    print(f"Found kb user with ID: {kb_user_id}")

    kb_user_details = client.describe_user(
        InstanceId=INSTANCE_ID,
        UserId=kb_user_id
    )['User']
    pprint(kb_user_details)

    # New user details
    new_username = "John-Doe"
    new_password = "Kbkn@1106"

    # Dynamically extract FirstName and LastName from hyphenated username
    name_parts = new_username.split("-")
    first_name = name_parts
    last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

    # Check if 'John-Doe' already exists
    existing_user_id = None
    for user in users:
        if user['Username'] == new_username:
            existing_user_id = user['Id']
            break

    if existing_user_id:
        print(f"User '{new_username}' is already present in the instance with ID: {existing_user_id}")
    else:
        # Prepare payload including mandatory IdentityInfo
        create_user_payload = {
            'InstanceId': INSTANCE_ID,
            'Username': new_username,
            'Password': new_password,
            'IdentityInfo': {
                'FirstName': first_name,
                'LastName': last_name,
            },
            'SecurityProfileIds': kb_user_details['SecurityProfileIds'],
            'RoutingProfileId': kb_user_details['RoutingProfileId'],
            'PhoneConfig': kb_user_details['PhoneConfig'],
        }

        if 'HierarchyGroupId' in kb_user_details:
            create_user_payload['HierarchyGroupId'] = kb_user_details['HierarchyGroupId']

        # Create new user
        response = client.create_user(**create_user_payload)
        print(f"New user created with ID: {response['UserId']}")

else:
    print("User with username 'kb' not found.")
