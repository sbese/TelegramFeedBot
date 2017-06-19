

class Bot:

    def __init__(self):

        import info
        import telebot
        from client import Client
        from sql import SQL_helper as SQL_DB

        self.info=info
        self.client=Client(self.info.api,self.info.api_hash,self.info.phone)
        self.db=SQL_DB(self.info.path,self.info.db)
        self.bot=telebot.TeleBot(self.info.token,threaded=False)
        self.to_id=0
        self.client_chat_id=self.info.client_chat_id


        @self.bot.message_handler()
        def nm(message):
            if message.chat.id==self.client_chat_id:
                if message.text.find('forward_to_')!=-1:
                    to_id=int(message.text.partition('forward_to_')[2])

                else: self.bot.forward_message(chat_id=self.to_id,
                                               from_chat_id=self.client_chat_id,
                                               message_id=message.message_id)

            else:
                print(message.text)
                self.db.check_id(message.chat.id,self.info.users_table)
                splited_text=message.text.replace(',',' ').split()

                if splited_text[0]=='/update':
                    self.update_feed(message,splited_text[1:])
                if splited_text[0]=='/add':
                    self.add_channels(message,splited_text[1:])
                if splited_text[0]=='/dell':
                    pass

    def update_feed(message):
        pass
    def add_channels(self,message,channels):
        channels=list(set(channels))
        Current_channels=self.db.get_channels(message.chat.id,self.info.users_table)
        for i in Current_channels:
            if channels.count(i)!=0:
                channels.remove(i)
        present_channels=self.db.get_all_channels(self.info.channels_table)
        added_channels=[]
        for i in channels:
            if present_channels.count(i)!=0:
                added_channels.append(i)
                channels.remove(i)

        for i in channels:
            type_chat=self.client.get_enity_type(self.client.get_enity_by_username(i))
            if type_chat=='unknown' or type_chat=='user':
                channels.remove(i)
            else:
                self.client.join_channel_by_channelname(i)
                self.db.add_channel(i,self.info.channels_table)

        update_list=str(str(channels+added_channels+Current_channels).replace(', ',',').replace("'",'')[1:-1])
        print(update_list)
        self.db.update_channels_list(update_list,self.info.users_table,message.chat.id)




    def del_channels(message):
        pass



    def start(self):
        self.bot.polling(none_stop=True)
