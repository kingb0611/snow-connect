import pytest
from unittest.mock import patch, MagicMock
from aws_connect import create_user

@pytest.fixture
def mock_boto_client():
    with patch('aws_connect.create_user.boto3.client') as mock_client:
        yield mock_client

def test_create_user_flow(mock_boto_client):
    mock_client_instance = MagicMock()
    mock_boto_client.return_value = mock_client_instance

    mock_client_instance.list_users.side_effect = [
        {'UserSummaryList': [{'Username': 'kb', 'Id': 'kb-id'}], 'NextToken': None}
    ]

    kb_user_details = {
        'SecurityProfileIds': ['sec-id'],
        'RoutingProfileId': 'route-id',
        'PhoneConfig': {'PhoneType': 'SOFT_PHONE'},
        'HierarchyGroupId': 'hier-group-id'
    }

    mock_client_instance.describe_user.return_value = {'User': kb_user_details}
    mock_client_instance.create_user.return_value = {'UserId': 'new-user-id'}

    with patch('aws_connect.create_user.pprint'), patch('builtins.print') as mock_print:
        create_user.main()
        mock_print.assert_any_call("Found kb user with ID: kb-id")
        mock_print.assert_any_call("New user created with ID: new-user-id")

def test_kb_user_not_found(mock_boto_client):
    mock_client_instance = MagicMock()
    mock_boto_client.return_value = mock_client_instance
    mock_client_instance.list_users.return_value = {'UserSummaryList': [], 'NextToken': None}

    with patch('builtins.print') as mock_print:
        create_user.main()
        mock_print.assert_any_call("User with username 'kb' not found.")
