import unittest
from unittest.mock import patch, MagicMock

# Import your target script as a module, e.g., create_user
import create_user

class TestCreateUserScript(unittest.TestCase):
    @patch('create_user.boto3.client')
    def test_create_user_flow(self, mock_boto_client):
        # Setup mock AWS Connect client
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client

        # Mock list_users return value
        mock_client.list_users.side_effect = [
            {'UserSummaryList': [{'Username': 'kb', 'Id': 'kb-id'}], 'NextToken': None}
        ]

        # Mock describe_user to return a full set of user details
        kb_user_details = {
            'SecurityProfileIds': ['sec-id'],
            'RoutingProfileId': 'route-id',
            'PhoneConfig': {'PhoneType': 'SOFT_PHONE'},
            'HierarchyGroupId': 'hier-group-id'
        }
        mock_client.describe_user.return_value = {'User': kb_user_details}

        # Mock create_user return
        mock_client.create_user.return_value = {'UserId': 'new-user-id'}

        # Patch pprint so it doesn't print during tests
        with patch('create_user.pprint'):
            # Run the script, expecting the prints
            with patch('builtins.print') as mock_print:
                create_user.main() # If script code is wrapped in main()

                # Validate that print was called for found user and new user creation
                mock_print.assert_any_call("Found kb user with ID: kb-id")
                mock_print.assert_any_call("New user created with ID: new-user-id")

    @patch('create_user.boto3.client')
    def test_kb_user_not_found(self, mock_boto_client):
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client

        mock_client.list_users.return_value = {'UserSummaryList': [], 'NextToken': None}

        with patch('builtins.print') as mock_print:
            create_user.main()
            mock_print.assert_any_call("User with username 'kb' not found.")

if __name__ == "__main__":
    unittest.main()
