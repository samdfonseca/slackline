import os
import typing

import slacker
from slacker import Slacker


ResponseItems = typing.Union[typing.List, typing.Dict]


def _get_api_token(token_file_path: str = None) -> str:
    if token_file_path is None or not os.path.isfile(os.path.expanduser(token_file_path)):
        return os.environ.get('SLACK_API_TOKEN') or _get_api_token('~/.slack_token')
    with open(os.path.expanduser(token_file_path)) as f:
        return f.readline().strip()


class SlackClient(object):
    client: Slacker = None

    def __init__(self, api_token: str = None, token_file_path: str = None):
        api_token = api_token or _get_api_token(token_file_path)
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

