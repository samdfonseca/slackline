from json import dumps
from unittest.mock import MagicMock, PropertyMock

from slackline.slack import api
from fixtures import CHANNELS_LIST_BODY, CHAT_POST_MESSAGE_BODY, IM_OPEN_BODY, USERS_LIST_BODY

import pytest



def mock_resp():
    resp = MagicMock()
    type(resp).successful = PropertyMock(return_value=True)
    type(resp).error = PropertyMock(return_value=None)
    return resp


@pytest.fixture
def mock_user_list_resp():
    resp = mock_resp()
    type(resp).body = PropertyMock(return_value=USERS_LIST_BODY)
    type(resp).raw = PropertyMock(return_value=dumps(USERS_LIST_BODY))
    return resp


@pytest.fixture
def mock_channels_list_resp():
    resp = mock_resp()
    type(resp).body = PropertyMock(return_value=CHANNELS_LIST_BODY)
    type(resp).raw = PropertyMock(return_value=dumps(CHANNELS_LIST_BODY))
    return resp


@pytest.fixture
def mock_im_open_resp():
    resp = mock_resp()
    type(resp).body = PropertyMock(return_value=IM_OPEN_BODY)
    type(resp).raw = PropertyMock(return_value=dumps(IM_OPEN_BODY))
    return resp


@pytest.fixture
def mock_chat_post_message_resp():
    resp = mock_resp()
    type(resp).body = PropertyMock(return_value=CHAT_POST_MESSAGE_BODY)
    type(resp).raw = PropertyMock(return_value=dumps(CHAT_POST_MESSAGE_BODY))
    return resp


@pytest.fixture
def slacker(mock_channels_list_resp, mock_user_list_resp, mock_im_open_resp, mock_chat_post_message_resp):
    client = MagicMock()
    type(client).users = PropertyMock()
    client.users.list = MagicMock()
    client.users.list.return_value = mock_user_list_resp
    type(client).channels = PropertyMock()
    client.channels.list = MagicMock()
    client.channels.list.return_value = mock_channels_list_resp
    type(client).im = PropertyMock()
    client.im.open = MagicMock()
    client.im.open.return_value = mock_im_open_resp
    type(client).chat = PropertyMock()
    client.chat.post_message = MagicMock()
    client.chat.post_message.return_value = mock_chat_post_message_resp

    return client


@pytest.fixture
def slack_client(slacker):
    return api.SlackClient(client=slacker)
    

def test_list_channels(slack_client: api.SlackClient):
    channels = slack_client.list_channels()
    slack_client.client.channels.list.assert_called_once_with()
    assert len(channels) == 1
    assert channels[0]['id'] == 'testchannelid'
    assert channels[0]['name'] == 'testchannel'


def test_get_member_by_name_with_at_prefix(slack_client: api.SlackClient):
    member = slack_client.get_member_by_name('@testmember')
    slack_client.client.users.list.assert_called_once_with()
    assert member['id'] == 'testmemberid'
    assert member['name'] == 'testmember'


def test_get_member_by_name_without_at_prefix(slack_client: api.SlackClient):
    member = slack_client.get_member_by_name('testmember')
    slack_client.client.users.list.assert_called_once_with()
    assert member['id'] == 'testmemberid'
    assert member['name'] == 'testmember'


def test_get_channel_by_name_with_pound_prefix(slack_client: api.SlackClient):
    channel = slack_client.get_channel_by_name('#testchannel')
    slack_client.client.channels.list.assert_called_once_with()
    assert channel['id'] == 'testchannelid'
    assert channel['name'] == 'testchannel'


def test_get_channel_by_name_without_pound_prefix(slack_client: api.SlackClient):
    channel = slack_client.get_channel_by_name('testchannel')
    slack_client.client.channels.list.assert_called_once_with()
    assert channel['id'] == 'testchannelid'
    assert channel['name'] == 'testchannel'


def test_send_message_to_channel_with_pound_prefix(slack_client: api.SlackClient):
    resp = slack_client.send_message('#testchannel', 'sam test')
    slack_client.client.chat.post_message.assert_called_once_with(channel='#testchannel', text='sam test')


def test_send_message_to_channel_without_prefix(slack_client: api.SlackClient):
    with pytest.raises(api.InvalidMessageToException):
        slack_client.send_message('testchannel', 'sam test')


def test_send_message_to_user_with_at_prefix(slack_client: api.SlackClient):
    resp = slack_client.send_message('@testmember', 'sam test')
    slack_client.client.users.list.assert_called_once_with()
    slack_client.client.im.open.assert_called_once_with('testmemberid')
    slack_client.client.chat.post_message.assert_called_once_with(channel='testimchannelid', text='sam test',
            as_user=True)
