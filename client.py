class Client:
    """
    Class that represent all functions that can be used for conectiong to telegram,
    recieving messages and fordwarding them
    """

    def __init__(self, api_id, api_hash, phone, logs_name=None):
        """
        Constructor of client class

        api_id - id of app that placed on your telegram app page
        api_hash - hash code of app that placed on your telegram app page
        phone - your phone that used in your telegram page
        logs_name - name of file that will contain logs. Can be outmitted.
        """

        import telethon

        self.tl = telethon
        self.TG = telethon.tl.functions
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.logs_name = logs_name

        self.client = telethon.TelegramClient(logs_name, api_id, api_hash)
        self.client.connect()
        if not self.client.is_user_authorized():
            self.client.send_code_request(phone)
            self.client.sign_in(phone, input('Enter code here: '))

    def get_enity_by_username(self, username):
        """
        Return enity object by username of chat in telegram. Enity contains list of chats and list of users object

        username - string of user, chat or channel in telegram
        """

        return self.client.invoke(self.TG.contacts.ResolveUsernameRequest(username))

    def get_enity_type(self, enity):
        """
        Return type of enity that can be recieved from method get_enity_by_username of other ways

        enity - object that can be recieved from method get_enity_by_username or other manual ways, but use them(ways) by your own risk
        """

        if len(enity.chats) != 0:
            return 'chat'
        elif len(enity.users) != 0:
            return 'user'
        else:
            return 'unknown'

    def get_InputPeer_by_enity(self, enity):
        """
        Return InputPeer by enity that can be recieved from method get_enity_by_username

        enity - object that can be recieved from method get_enity_by_username or other manual ways, but use them(ways) by your own risk
        """

        if self.get_enity_type(enity) == 'user':
            return self.tl.utils.get_input_peer(enity.users[0])
        elif self.get_enity_type(enity) == 'chat':
            return self.tl.utils.get_input_peer(enity.chats[0])
        else:
            return None

    def get_InputPeer_by_username(self, username):
        """
        Return InputPeer by username

        username - string of user, chat or channel in telegram
        """

        return self.get_InputPeer_by_enity(
                    self.client.invoke(
                        self.TG.contacts.ResolveUsernameRequest(username)
                    )
                )

    def get_messages_enity_by_enity(self, enity, messages_count=50):
        """
        Return messages enity by enity that can e recieved from method get_enity_by_username
        Messages enity contains list of messages, list of chats and list of users that are in dialog

        enity - object that can be recieved from method get_enity_by_username or other manual ways, but use them(ways) by your own risk
        messages_count - count of messages that will be in messages enity
        """

        return self.client.invoke(
                    self.TG.messages.GetHistoryRequest(
                        peer = self.get_InputPeer_by_enity(enity),
                        offset_id = 0,
                        offset_date = None,
                        add_offset = 0,
                        limit = messages_count,
                        max_id = 0,
                        min_id = 0
                    )
                )

    def get_messages_enity_by_username(self, username, messages_count=50):
        """
        Return messages enity by enity that can e recieved from method get_enity_by_username
        Messages enity contains list of messages, list of chats and list of users that are in dialog

        username - string of user, chat or channel in telegram
        messages_count - count of messages that will be in messages enity
        """

        return self.client.invoke(
                    self.TG.messages.GetHistoryRequest(
                        peer = self.get_InputPeer_by_username(username),
                        offset_id = 0,
                        offset_date = None,
                        add_offset = 0,
                        limit = messages_count,
                        max_id = 0,
                        min_id = 0
                    )
                )

    def forward_messages_by_enities(self, from_enity, to_enity, messages_enity):
        """
        Forward messages from one person to other

        from_enity - enity that is original owner of messages
                        object that can be recieved from method get_InputPeer_by_enity or get_InputPeer_by_username or other manual ways,
                        but use them(ways) by your own risk
        to_enity - enity that is user, channel or chat that must become messages
                        object that can be recieved from method get_InputPeer_by_enity or get_InputPeer_by_username or other manual ways,
                        but use them(ways) by your own risk
        messages_enity - enity of messages that can be recieved from get_messages_enity_by_username method or get_messages_enity_by_enity method
        """

        return self.client.invoke(
                    self.TG.messages.ForwardMessagesRequest(
                        from_peer = self.get_InputPeer_by_enity(from_enity),
                        id = [msg.id for msg in messages_enity.messages],
                        to_peer = self.get_InputPeer_by_enity(to_enity),
                        random_id = [self.tl.helpers.generate_random_long() for _ in
                                    range(len(messages_enity.messages))]
                    )
                )

    def forward_messages_by_peernames(self, from_peer_name, to_peer_name, messages_enity):
        """
        Forward messages from one person to other

        from_peer_name - string that is original name owner of messages(chat, channel or user)
        to_peer_name - string that is user, channel or chat name that must become messages
        messages_enity - enity of messages that can be recieved from get_messages_enity_by_username method or get_messages_enity_by_enity method
        """

        return self.client.invoke(
                    self.TG.messages.ForwardMessagesRequest(
                        from_peer = self.get_InputPeer_by_username(from_peer_name),
                        id = [msg.id for msg in messages_enity.messages],
                        to_peer = self.get_InputPeer_by_username(to_peer_name),
                        random_id = [self.tl.helpers.generate_random_long() for _ in
                                    range(len(messages_enity.messages))]
                    )
                )

    def forward_messages_by_InputPeers(self, from_peer, to_peer, messages_enity):
        """
        Forward messages from one person to other

        from_peer - InputPeer user, channel or user that is owner of messages
        object that can be recieved from method get_enity_by_username or other manual ways, but use them(ways) by your own risk
        to_peer - InputPeer user, channel or user that must become messages
        object that can be recieved from method get_enity_by_username or other manual ways, but use them(ways) by your own risk
        messages_enity - enity of messages that can be recieved from get_messages_enity_by_username method or get_messages_enity_by_enity method
        """

        return self.client.invoke(
                    self.TG.messages.ForwardMessagesRequest(
                        from_peer = from_peer,
                        id = [msg.id for msg in messages_enity.messages],
                        to_peer = to_peer,
                        random_id = [self.tl.helpers.generate_random_long() for _ in
                                    range(len(messages_enity.messages))]
                    )
                )

    def join_channel_by_channelname(self, channelname):
        """
        Join this client to channel with name given as parametr

        channelname - string name of channel that must be added to user
        """

        self.client.invoke(
                self.TG.channels.JoinChannelRequest(
                    self.get_InputPeer_by_username(channelname))
            )

    def close_connection(self):
        self.client.disconnect()
