"""
slack_post.py: A module for managing and posting messages to Slack.

This module provides a simple interface to post messages to Slack channels
using the Slack WebClient API.
"""

from slack import WebClient
from slack_sdk.errors import SlackApiError

class SlackManager:
    """
    A class for managing Slack message posting operations.
    """

    def __init__(self, slack_token: str):
        """
        Initialize the SlackManager with a Slack API token.

        Args:
            slack_token (str): The Slack API token for authentication.
        """
        self.slack_client = WebClient(token=slack_token)

    def post_to_slack(self, channel: str, message: str):
        """
        Post a message to a specified Slack channel.

        Args:
            channel (str): The name or ID of the Slack channel to post to.
            message (str): The message content to be posted.

        Raises:
            SlackApiError: If there's an error posting the message to Slack.
        """
        try:
            # Attempt to post the message to the specified channel
            response = self.slack_client.chat_postMessage(channel=channel, text=message)
            print(f"Message posted: {response['ts']}")
        except SlackApiError as e:
            # Log the error if the message posting fails
            print(f"Error posting message: {e}")