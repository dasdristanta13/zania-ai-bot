"""
slack_post.py: Manages posting messages to Slack
"""

from slack import WebClient
from slack_sdk.errors import SlackApiError

class SlackManager:
    """
    A class to manage posting messages to Slack channels.
    """

    def __init__(self, slack_token: str):
        """
        Initialize the SlackManager with a Slack API token.

        Args:
            slack_token (str): The Slack API token for authentication.
        """
        # Initialize the Slack Web client with the provided token
        self.slack_client = WebClient(token=slack_token)

    def post_to_slack(self, channel: str, message: str):
        """
        Post a message to a specified Slack channel.

        Args:
            channel (str): The name or ID of the Slack channel to post to.
            message (str): The message to be posted.

        Raises:
            SlackApiError: If there's an error posting the message to Slack.
        """
        try:
            # Attempt to post the message to the specified channel
            response = self.slack_client.chat_postMessage(channel=channel, text=message)
            # Print a confirmation message with the timestamp of the posted message
            print(f"Message posted: {response['ts']}")
        except SlackApiError as e:
            # If there's an error, print the error message
            print(f"Error posting message: {e}")