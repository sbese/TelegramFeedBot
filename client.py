class Client:


    def __init__(self, api_id, api_hash, phone, logs_name=None):
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
        return self.client.invoke(self.TG.contacts.ResolveUsernameRequest(username))

    def get_enity_type(self, enity):
        if len(enity.chats) != 0:
    		return 'chat'
    	elif len(enity.users) != 0:
    		return 'user'
    	else:
    		return 'unknown'

    def get_InputPeer_by_enity(self, enity):
    	if self.get_enity_type(enity) == 'user':
    		return self.tl.utils.get_input_peer(enity.users[0])
    	elif self.get_enity_type(enity) == 'chat':
    		return self.tl.utils.get_input_peer(enity.chats[0])
    	else:
    		return None

    def get_InputPeer_by_username(self, username):
    	peer = self.client.invoke(self.TG.contacts.ResolveUsernameRequest(username)    				)
    	return self.get_InputPeer_by_enity(peer)

    def get_messages_enity_by_enity(self, enity, messages_count=50):
    	return self.client.invoke(
    				self.TG.messages.GetHistoryRequest(
    					peer = self.get_InputPeer_by_enity(enity),
    					offset_id = 0,
    					offset_date = None,
    					add_offset = 0,
    					limit = messages_count,
    					max_id = 0,
    					min_id = 0)
    				)

    def get_messages_enity_by_username(self, username, messages_count=50):
	       return self.client.invoke(
    				self.TG.messages.GetHistoryRequest(
    					peer = self.get_InputPeer_by_username(username),
    					offset_id = 0,
    					offset_date = None,
    					add_offset = 0,
    					limit = messages_count,
    					max_id = 0,
    					min_id = 0)
    				)

    def forward_messages_by_enities(self, from_enity, to_enity, messages_enity):
        return self.client.invoke(self.TG.messages.ForwardMessagesRequest(
    				from_peer = self.get_InputPeer_by_enity(from_enity)
    				id = [msg.id for msg in messages_enity.messages]
    				to_peer = self.get_InputPeer_by_enity(to_enity)
    				random_id = [self.tl.helpers.generate_random_long() for _ in
    							 range(len(messages_enity.messages)]
    				))

    def forward_messages_by_peernames(self, from_peer_name, to_peer_name, messages_enity):
        return self.client.invoke(self.TG.messages.ForwardMessagesRequest(
    				from_peer = self.get_InputPeer_by_username(from_peer_name)
    				id = [msg.id for msg in messages_enity.messages]
    				to_peer = self.get_InputPeer_by_username(to_peer_name)
    				random_id = [self.tl.helpers.generate_random_long() for _ in
    							 range(len(messages_enity.messages)]
    				))

    def forward_messages_by_InputPeers(self, from_peer, to_peer, messages_enity):
        return self.client.invoke(self.TG.messages.ForwardMessagesRequest(
    				from_peer = from_peer
    				id = [msg.id for msg in messages_enity.messages]
    				to_peer = to_peer
    				random_id = [self.tl.helpers.generate_random_long() for _ in
    							 range(len(messages_enity.messages)]
    				))
