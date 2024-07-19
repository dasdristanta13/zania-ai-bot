"""
slack_post.py: Manages posting messages to Slack
"""

from slack import WebClient
from slack_sdk.errors import SlackApiError

class SlackManager:
    def __init__(self, slack_token):
        self.slack_client = WebClient(token=slack_token)

    def post_to_slack(self, channel, message):
        try:
            response = self.slack_client.chat_postMessage(channel=channel, text=message)
            print(f"Message posted: {response['ts']}")
        except SlackApiError as e:
            print(f"Error posting message: {e}")