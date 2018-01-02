USERS_LIST_BODY = {
        'cache_ts': 1514895153,
        'members': [
            {'deleted': True,
             'id': 'testmemberid',
             'is_app_user': False,
             'is_bot': False,
             'name': 'testmember',
             'profile': {
                 'avatar_hash': 'g65f09c1049a',
                 'display_name': 'testmember',
                 'display_name_normalized': 'testmember',
                 'email': 'member@test.com',
                 'first_name': 'Test',
                 'image_192': 'https://secure.gravatar.com/avatar/65f09c1049a0b0c11e832faaf679b903.jpg',
                 'image_24': 'https://secure.gravatar.com/avatar/65f09c1049a0b0c11e832faaf679b903.jpg',
                 'image_32': 'https://secure.gravatar.com/avatar/65f09c1049a0b0c11e832faaf679b903.jpg',
                 'image_48': 'https://secure.gravatar.com/avatar/65f09c1049a0b0c11e832faaf679b903.jpg',
                 'image_512': 'https://secure.gravatar.com/avatar/65f09c1049a0b0c11e832faaf679b903.jpg',
                 'image_72': 'https://secure.gravatar.com/avatar/65f09c1049a0b0c11e832faaf679b903.jpg',
                 'last_name': 'Member',
                 'real_name': 'Test Member',
                 'real_name_normalized': 'Test Member',
                 'team': 'testteamid'},
             'team_id': 'testteamid',
             'updated': 1504292197},
            ],
        'ok': True}


CHANNELS_LIST_BODY = {
        'channels': [
            {'created': 1510076280,
             'creator': 'testuserid',
             'id': 'testchannelid',
             'is_archived': True,
             'is_channel': True,
             'is_general': False,
             'is_member': False,
             'is_mpim': False,
             'is_org_shared': False,
             'is_private': False,
             'is_shared': False,
             'members': [],
             'name': 'testchannel',
             'name_normalized': 'testchannel',
             'num_members': 0,
             'previous_names': [],
             'purpose': {'creator': '', 'last_set': 0, 'value': ''},
             'topic': {'creator': '', 'last_set': 0, 'value': ''},
             'unlinked': 0},
            ],
        'ok': True}


IM_OPEN_BODY = {
        'already_open': True,
        'channel': {
            'id': 'testimchannelid'
            },
        'no_op': True,
        'ok': True,
        }


CHAT_POST_MESSAGE_BODY = {'channel': 'testchannelid',
 'message': {'bot_id': 'testbotid',
  'text': 'sam test',
  'ts': '1514896829.000208',
  'type': 'message',
  'user': 'testmemberid'},
 'ok': True,
 'ts': '1514896829.000208'}
