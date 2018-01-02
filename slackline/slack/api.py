import os
import typing

import slacker
from slacker import Slacker


ResponseItems = typing.Union[typing.List, typing.Dict]


class InvalidMessageToException(Exception):
    pass

def _get_api_token(token_file_path: str = None) -> str:
    default_token_file_path = os.path.expanduser('~/.slack_token')
    if token_file_path is None:
        if os.path.isfile(os.path.expanduser(default_token_file_path)):
            # `token_file_path` is None and `default_token_file_path` exists, return SLACK_API_TOKEN if defined, else
            # return contents of `default_token_file_path`
            return os.environ.get('SLACK_API_TOKEN') or _get_api_token(default_token_file_path)
        # `token_file_path` is None and `default_token_file_path` does not exist, return SLACK_API_TOKEN or None
        return os.environ.get('SLACK_API_TOKEN')
    if token_file_path is not None:
        if os.path.isfile(os.path.expanduser(token_file_path)):
            # `token_file_path` is not None and `token_file_path` exists, return SLACK_API_TOKEN if defined, else
            # return contents of `token_file_path`
            with open(os.path.expanduser(token_file_path)) as f:
                return os.environ.get('SLACK_API_TOKEN') or f.readline().strip()
        # `token_file_path` is not None and `token_file_path` does not exist, return SLACK_API_TOKEN or None
        return os.environ.get('SLACK_API_TOKEN')


class SlackClient(object):
    client: Slacker = None

    def __init__(self, api_token: str = None, token_file_path: str = None, client: Slacker = None):
        self.client = client
        api_token = api_token or _get_api_token(token_file_path)
        if api_token is not None and self.client is None:
            self.client = Slacker(api_token)

    @staticmethod
    def _guess_key(body: dict) -> str:
        ignore_keys = ('ok', 'cache_ts')
        filtered_keys = [k for k in list(body.keys()) if k not in ignore_keys]
        if len(filtered_keys) == 1:
            return filtered_keys[0]

    @staticmethod
    def _resp_item(resp: slacker.Response, key: str = None) -> ResponseItems:
        if resp.successful:
            if key is not None and key in resp.body:
                return resp.body[key]
            if key is None:
                key = SlackClient._guess_key(resp.body)
                if key is not None:
                    return SlackClient._resp_item(resp, key=key)

    def list_members(self) -> list:
        return self._resp_item(self.client.users.list(), 'members')

    def get_member_by_name(self, member_name: str) -> dict:
        member_name = member_name[1:] if member_name.startswith('@') else member_name
        members = self.list_members()
        for member in members:
            if member['name'] == member_name:
                return member

    def list_channels(self) -> list:
        return self._resp_item(self.client.channels.list(), 'channels')

    def get_channel_by_name(self, channel_name: str) -> dict:
        channel_name = channel_name[1:] if channel_name.startswith('#') else channel_name
        channels = self.list_channels()
        for channel in channels:
            if channel['name'] == channel_name:
                return channel

    def send_message_to_channel(self, channel: str, msg: str, **kwargs) -> dict:
        return self.client.chat.post_message(channel=channel, text=msg, **kwargs)

    def send_message_to_user(self, user: str, msg: str, **kwargs) -> dict:
        user_id = self.get_member_by_name(user)['id']
        channel_id = self.client.im.open(user_id).body['channel']['id']
        return self.send_message_to_channel(channel_id, msg, as_user=True, **kwargs)
        
    def send_message(self, to: str, msg: str, **kwargs) -> dict:
        if to.startswith('#'):
            return self.send_message_to_channel(to, msg, **kwargs)
        if to.startswith('@'):
            return self.send_message_to_user(to, msg, **kwargs)
        raise InvalidMessageToException('Message to value must start with either "@" for users or "#" for channels')
